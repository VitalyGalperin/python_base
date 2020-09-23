# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
import json
import datetime

import ya_rasp
import handlers
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


class UserState:

    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


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
        if self.first_event:
            self.send_vk_message(event, HELLO_MESSAGE)
            self.first_event = False
            return
        if user_id in self.user_states:
            text_to_send = self.continue_scenario(user_id, text)
        else:
            # search intevt
            for intent in INTENTS:
                log.debug(f'user get {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])
                    break
            else:
                text_to_send = DEFAULT_ANSWER

        self.send_vk_message(event, text_to_send)

    def send_vk_message(self, event, text_to_send):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=event.object.peer_id, )

    def start_scenario(self, user_id, scenario_name):
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.flights_found = 0
        self.request_error = False
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
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
            if state.context.get('date') and not state.context.get('flight'):
                text_to_send = self.get_flights(state, user_id)
                if self.request_error:
                    log.error('Ошибка запроса Яндекс-Расписания')
                    text_to_send = 'Ошибка запроса Яндекс-Расписания'
                    self.end_scenario(user_id)
                    self.send_text(text_to_send, user_id)
                    return
                if self.flights_found < 1:
                    log.info('Рейсы не найдены')
                    text_to_send = 'Рейсы не найдены'
                    self.end_scenario(user_id)
                    self.send_text(text_to_send, user_id)
                    return
            if str(handler).find('flight') > -1:
                if not handler(text=text, context=state.context, flights_found=self.flights_found):
                    self.send_text(step['failure_text'], user_id)
                    return
            if next_step['next_step']:
                state.step_name = step['next_step']
                text_to_send += next_step['text'].format(**state.context)
            elif next_step == steps['last_step']:
                log.info('Заказ принят, с Вами свяжутся по телефону {phone}'.format(**state.context))
                text_to_send = steps['last_step']['text'].format(**state.context)
                self.end_scenario(user_id)
        else:
            if str(handler).find('confirm') > -1 and text.lower().find('no') > -1 or text.lower().find('нет') > -1:
                log.info('Заказ не подтверждён')
                text_to_send = 'Заказ не подтверждён\n\n'
                self.end_scenario(user_id)
                return text_to_send
            # retry current step
            if state.context.get('search_warning'):
                text_to_send = state.context['search_warning']
                state.context.pop('search_warning')
            else:
                text_to_send = step['failure_text']
        return text_to_send

    def end_scenario(self, user_id):
        self.user_states.pop(user_id)
        self.first_event = True

    def get_flights(self, state, user_id):
        self.flights_found = 0
        text_to_send = ''
        request = None
        from_station = list(state.context['departure_city'].values())[0]
        to_station = list(state.context['arrival_city'].values())[0]
        date_flight = state.context['date']
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
                        'number'] + ': ' + \
                                    self.ya_answer['segments'][i]['thread']['title'] + ' ' + '\n' + \
                                    (self.ya_answer['segments'][i]['arrival']).replace('T', ' ') + '\n'
                    self.flights_found += 1
            date_flight += datetime.timedelta(days=1)
        return text_to_send


if __name__ == "__main__":
    config_log()
    bot = Bot()
    bot.run()
