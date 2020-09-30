# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
import json
import datetime
import requests
import settings
import ya_rasp
import handlers
from pony.orm import db_session
from models import UserState, Registration

try:
    from settings import TOKEN, GROUP_ID, YA_TOKEN, YA_URL, HELLO_MESSAGE, DEFAULT_ANSWER, INTENTS, SCENARIOS, \
        FLIGHTS_DAYS, FLIGHTS_NUMBERS
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')
log = logging.getLogger('bot')


def config_log():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M'))
    file_handler = logging.FileHandler('bot.log')
    file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M'))
    log.addHandler(handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class Bot:
    """
    Бот поиска авиабилетов VK
    Python version 3.7
    """

    def __init__(self):
        """
        :param GROUP_ID: ID группы VK
        :param TOKEN VK: секретный токен
        """
        self.group_id = GROUP_ID
        self.token = TOKEN
        self.ya_token = YA_TOKEN
        self.cities_file = 'cities.json'
        self.vk = vk_api.VkApi(token=TOKEN)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()
        self.cities_json = self.ya_answer = None
        self.user_states = dict()
        self.request_error = False
        self.first_event = True
        self.flights_found = 0

    def run(self):
        """
        Запуск бота
        """
        self.get_cities_json(self.cities_file)
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка обработки')

    def get_cities_json(self, cities_file):
        with open(cities_file, "r", encoding="utf-8") as read_file:
            self.cities_json = json.load(read_file)

    @db_session
    def on_event(self, event):
        """
        Обработка события:
        :param event: VkBotMessageEvent
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info('Сообщения такого типа не обрабатываются %s', event.type)
            return
        user_id = event.object.peer_id
        text = event.object.text
        state = UserState.get(user_id=str(user_id))

        if self.first_event:
            self.send_text(HELLO_MESSAGE, user_id)
            self.first_event = False
            return
        if state is not None:
            self.continue_scenario(text, state, user_id)
        else:
            for intent in INTENTS:
                log.debug(f'user get {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        self.send_text(intent['answer'], user_id)
                    else:
                        self.start_scenario(user_id, intent['scenario'], text)
                    break
            else:
                self.send_text(settings.DEFAULT_ANSWER, user_id)

    def send_text(self, text_to_send, user_id):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id, )

    def send_image(self, image, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('image.png', image, 'image/png')}).json()
        image_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = image_data[0]['owner_id']
        media_id = image_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.api.messages.send(
            attachment=attachment,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id, )

    def send_step(self, step, user_id, text, context):
        if 'text' in step and text:
            self.send_text(text, user_id)
        if 'image' in step:
            handler = getattr(handlers, step['image'])
            image = handler(text, context)
            self.send_image(image, user_id)

    def start_scenario(self, user_id, scenario_name, text):
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.send_step(step, user_id, text_to_send, context={})
        self.flights_found = 0
        self.request_error = False
        UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step,
                  context=self.get_empty_context())

    def continue_scenario(self, text, state, user_id):
        state.context['cities_json'] = self.cities_json
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        text_to_send = ''
        if handler(text=text, context=state.context):
            next_step = steps[step['next_step']]
            if state.context.get('city_message'):
                text_to_send = state.context['city_message']
                state.context.pop('city_message')
            if state.context.get('date') and not state.context.get('flight_to_print'):
                text_to_send = self.get_flights(state)
                if self.request_error:
                    log.error('Ошибка запроса Яндекс-Расписания')
                    text_to_send = 'Ошибка запроса Яндекс-Расписания'
                    self.send_step(step, user_id, text_to_send, state.context)
                    self.end_scenario(state)
                    return
                if self.flights_found < 1:
                    log.info('Рейсы не найдены')
                    text_to_send = 'Рейсы не найдены'
                    self.send_step(step, user_id, text_to_send, state.context)
                    self.end_scenario(state)
                    return
            if str(handler).find('flight') > -1:
                if not handler(text=text, context=state.context):
                    self.send_step(step, user_id, text_to_send, state.context)
                    return
            if next_step['next_step']:
                state.step_name = step['next_step']
                text_to_send += next_step['text'].format(**state.context)
            elif next_step == steps['last_step']:
                log.info('Заказ принят, с Вами свяжутся по телефону {phone} или e-mail {email}'.format(**state.context))
                text_to_send = steps['last_step']['text'].format(**state.context)
                self.send_step(next_step, user_id, text_to_send, state.context)
                text_to_send = ''
                self.end_scenario(state)
        else:
            if str(handler).find('confirm') > -1 and text.lower().find('no') > -1 or text.lower().find('нет') > -1:
                log.info('Заказ не подтверждён')
                text_to_send = 'Заказ не подтверждён\n\n'
                self.end_scenario(state)
                return text_to_send
            # retry current step
            if state.context.get('search_warning'):
                text_to_send = state.context['search_warning']
                state.context.pop('search_warning')
            else:
                text_to_send = step['failure_text']
        self.send_step(step, user_id, text_to_send, state.context)

    def end_scenario(self, state):
        if self.check_state(state):
            Registration(departure_city_to_print=state.context['departure_city_to_print'],
                         arrival_city_to_print=state.context['arrival_city_to_print'],
                         departure_date=state.context['date_flight_to_print'],
                         departure_time=state.context['time_flight_to_print'],
                         first_name=state.context['first_name'],
                         last_name=state.context['last_name'],
                         phone=state.context['phone'],
                         flight=state.context['flight_to_print'],
                         email=state.context['email'],
                         number_of_seats=state.context['seats'],
                         comment=state.context['comment'])
        state.delete()
        self.first_event = True

    @staticmethod
    def check_state(state):
        if state.context['first_name'] == '' or state.context['last_name'] == '' or \
                state.context['departure_city_to_print'] == '' or state.context['date_flight_to_print'] == '' or \
                state.context['time_flight_to_print'] == '' or state.context['arrival_city_to_print'] == '' or \
                state.context['phone'] == '' or state.context['flight_to_print'] == '' or \
                state.context['email'] == '' or state.context['first_name'] == '':
            return False
        else:
            return True

    def get_empty_context(self):
        context = {'first_name': '', 'last_name': '', 'departure_city_to_print': '', 'date_flight_to_print': '',
                   'time_flight_to_print': '', 'arrival_city_to_print': '', 'phone': '', 'flight_to_print': '',
                   'email': ''}
        return context

    def get_flights(self, state):
        self.flights_found = 0
        text_to_send = ''
        request = None
        from_station = list(state.context['departure_city'].values())[0]
        to_station = list(state.context['arrival_city'].values())[0]
        date_flight = datetime.date(day=int(state.context['date'][:2]), month=int(state.context['date'][3:5]),
                                    year=int(state.context['date'][6:10]))
        last_iso_date = date_flight + datetime.timedelta(days=FLIGHTS_DAYS)
        while self.flights_found < FLIGHTS_NUMBERS and date_flight < last_iso_date:
            date_flight_str = date_flight.strftime("%Y-%m-%d")
            request_flights = str(FLIGHTS_NUMBERS - self.flights_found)
            request = ya_rasp.request_ya_rasp(date_flight_str, from_station, request, to_station, request_flights)
            if not request:
                self.request_error = True
                return 'Ошибка запроса Яндекс-Расписания'
            self.ya_answer = json.loads(request)
            if self.ya_answer.get('error'):
                text_to_send = self.ya_answer['error']['text']
            else:
                for i, flight in enumerate(self.ya_answer['segments']):
                    text_to_send += str(self.flights_found + 1) + ' : ' + self.ya_answer['segments'][i]['thread'][
                        'number'] + ': ' + self.ya_answer['segments'][i]['thread']['title'] + ' ' + '\n' + (
                                        self.ya_answer['segments'][i]['departure']).replace('T', ' ') + '\n'
                    get_date = self.ya_answer['segments'][i]['departure']
                    state.context['date_flight' + str(self.flights_found + 1)] = get_date[8:10] + \
                                                                                 get_date[4:7] + '-' + get_date[0:4]
                    state.context['time_flight' + str(self.flights_found + 1)] = get_date[11:16] + get_date[19:]
                    state.context['thread' + str(self.flights_found + 1)] = \
                        self.ya_answer['segments'][i]['thread']['number']
                    self.flights_found += 1
            date_flight += datetime.timedelta(days=1)
        state.context['flights_found'] = self.flights_found
        return text_to_send


if __name__ == "__main__":
    config_log()
    bot = Bot()
    bot.run()
