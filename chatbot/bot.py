# -*- coding: utf-8 -*-
try:
    from settings import TOKEN, GROUP_ID, YA_TOKEN, YA_URL, HELLO_MESSAGE, DEFAULT_ANSWER, INTENTS, SCENARIOS, \
        FLIGHTS_DAYS, FLIGHTS_NUMBERS
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
import json
import requests
import handlers
import datetime

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
        self.city_code = self.is_get_date = self.request_error = False
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
            self.hello_message(event)
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

    def hello_message(self, event):
        self.send_vk_message(event, HELLO_MESSAGE)
        self.first_event = self.request_error = False

    def start_scenario(self, user_id, scenario_name):
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.flights_found = 0
        self.city_code = self.is_get_date = self.request_error = False
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        handler = getattr(handlers, step['handler'])
        text_to_send = ''
        if handler(text=text, context=state.context):
            next_step = steps[step['next_step']]
            if str(handler).find('city') > -1:
                text_to_send = self.check_city(handler, step, text, state)
                if not self.city_code:
                    return text_to_send
            if str(handler).find('date') > -1:
                text_to_send = self.check_date(handler, state, text)
                if not self.is_get_date:
                    return text_to_send
            if state.context.get('date') and not state.context.get('flight'):
                text_to_send = self.get_flights(state)
                if self.request_error:
                    log.error('Ошибка запроса Яндекс-Расписания')
                    text_to_send = 'Ошибка запроса Яндекс-Расписания\n\n' + HELLO_MESSAGE
                    self.user_states.pop(user_id)
                if self.flights_found < 1:
                    log.info('Рейсы не найдены')
                    text_to_send = 'Рейсы не найдены\n\n' + HELLO_MESSAGE
                    self.user_states.pop(user_id)
            if str(handler).find('flight') > -1:
                if not handler(text=text, context=state.context, flights_found=self.flights_found):
                    return step['failure_text']
            if next_step['next_step']:
                state.step_name = step['next_step']
                text_to_send += next_step['text'].format(**state.context)
            elif next_step == steps['last_step']:
                log.info('Заказ принят, с Вами свяжутся по телефону {phone}'.format(**state.context))
                text_to_send = 'Заказ принят, с Вами свяжутся по телефону {phone}\n\n'.format(**state.context) \
                               + HELLO_MESSAGE
                self.user_states.pop(user_id)
        else:
            if str(handler).find('confirm') > -1 and text.lower().find('no') > -1 or text.lower().find('нет') > -1:
                log.info('Заказ не подтверждён')
                text_to_send = 'Заказ не подтверждён\n\n' + HELLO_MESSAGE
                self.user_states.pop(user_id)
                return text_to_send
            # retry current step
            text_to_send = step['failure_text']
        return text_to_send
    # TODO Эти проверки (эта и ниже) можно же вынести в Handler-ы, разве нет?
    # TODO Зачем всё это собирать в теле самого бота?
    def check_date(self, handler, state, text):
        self.is_get_date = False
        arrival_date = datetime.date(day=int(text[:2]), month=int(text[3:5]), year=int(text[6:10]))
        if arrival_date < datetime.date.today():
            return 'Невозможно найти билет на прошедшую дату'
        if arrival_date > datetime.date.today() + datetime.timedelta(365):
            return 'Не можем искать билет более, чем на год вперёд'
        handler(text=arrival_date.strftime("%Y-%m-%d"), context=state.context, ymd_format=True)
        self.is_get_date = True
        return 'Принято'

    def check_city(self, handler, step, text, state):
        self.city_code = False
        cities = self.get_city(text)
        if len(cities) < 1:
            text_to_send = step['failure_text']
        elif len(cities) > 1:
            text_to_send = 'Найдены следующие города:\n'
            for city, code in cities.items():
                text_to_send += city + ' (' + code + ')\n'
            text_to_send += step['failure_text']
        else:
            handler(text=cities, context=state.context)
            text_to_send = 'Принято:\n'
            for city, code in cities.items():
                text_to_send += city + ' (' + code + ')\n'
            self.city_code = True
        return text_to_send

    def get_city(self, search_str):
        search_str = search_str.lower()
        cities = {}
        for city in self.cities_json:
            if (city['name'] and city['name'].lower().find(search_str) > -1) or \
                    (city['cases']['vi'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                    (city['cases']['tv'] and city['cases']['tv'].lower().find(search_str) > -1) or \
                    (city['cases']['ro'] and city['cases']['ro'].lower().find(search_str) > -1) or \
                    (city['cases']['pr'] and city['cases']['pr'].lower().find(search_str) > -1) or \
                    (city['cases']['da'] and city['cases']['da'].lower().find(search_str) > -1) or \
                    city['code'].lower() == search_str:
                cities[city['name']] = city['code']
        return cities

    def get_flights(self, state):
        self.flights_found = 0
        text_to_send = ''
        request = None
        from_station = list(state.context['departure_city'].values())[0]
        to_station = list(state.context['arrival_city'].values())[0]
        date_flight = state.context['date']
        current_iso_date = datetime.date(day=int(date_flight[8:10]), month=int(date_flight[5:7]),
                                         year=int(date_flight[:4]))
        last_iso_date = current_iso_date + datetime.timedelta(days=FLIGHTS_DAYS)
        while self.flights_found < FLIGHTS_NUMBERS and current_iso_date < last_iso_date:
            request_flights = str(FLIGHTS_NUMBERS - self.flights_found)
            request = self.request_ya_rasp(date_flight, from_station, request, to_station, request_flights)
            if not request:
                self.request_error = True
                return 'Ошибка запроса Яндекс-Расписания'
            self.ya_answer = json.loads(request.text)
            if self.ya_answer.get('error'):
                text_to_send = self.ya_answer['error']['text']
            else:
                for i, flight in enumerate(self.ya_answer['segments']):
                    text_to_send += str(self.flights_found + 1) + ' : ' + self.ya_answer['segments'][i]['thread'][
                        'number'] + ': ' + \
                                    self.ya_answer['segments'][i]['thread']['title'] + ' ' + '\n' + \
                                    (self.ya_answer['segments'][i]['arrival']).replace('T', ' ') + '\n'
                    self.flights_found += 1
            current_iso_date += datetime.timedelta(days=1)
            date_flight = current_iso_date.strftime("%Y-%m-%d")
        return text_to_send

    def request_ya_rasp(self, date, from_station, request, to_station, request_flights):
        try:
            request = requests.get(YA_URL + 'apikey=' + YA_TOKEN +
                                   '&format=json&transport_types=plane&system=iata&transfers=false&lang=ru_RU&limit='
                                   + request_flights + '&from=' + from_station + '&to=' + to_station + '&date=' + date)
        except Exception:
            log.exception('Ошибка запроса Яндекс-Расписания')
        return request


if __name__ == "__main__":
    config_log()
    bot = Bot()
    bot.run()
