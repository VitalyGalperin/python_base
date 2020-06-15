# -*- coding: utf-8 -*-
try:
    from settings import TOKEN, GROUP_ID, YA_TOKEN, YA_URL, HELLO_MESSAGE, DEFAULT_ANSWER, INTENTS, SCENARIOS
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
import json
import requests
import handlers

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

        self.cities_json = self.ya_answer = self.city_code = None
        self.user_states = dict()
        self.first_event = True

    def run(self):
        """
        Запуск бота
        """
        self.get_cities_json(self.cities_file)

        request = requests.get(YA_URL + 'apikey=' + YA_TOKEN +
                               '&format=json&transport_types=plane&system=iata&transfers=false&lang=ru_RU&limit=5' +
                               '&from=' + 'MOW' + '&to=' + 'LED' + '&date=' + '2020-07-07')
        self.ya_answer = json.loads(request.text)


        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка обработки')

    def on_event(self, event):
        """
        Обработка события:
        :param event: VkBotMessageEvent
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info('Сообщения такого типа не обрабатываются %s', event.type)
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

        self.send_vk_meesage(event, text_to_send)

    def send_vk_meesage(self, event, text_to_send):
        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=event.object.peer_id, )

    def hello_message(self, event):
        self.send_vk_meesage(event, HELLO_MESSAGE)
        self.first_event = False

    def start_scenario(self, user_id, scenario_name):
        scenario = SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            text_to_send = self.check_city(handler, step, text, state)
            if text_to_send:
                return text_to_send
            if state.context.get('date') and not state.context.get('flight'):
                if not self.get_flights(state):
                    print('2')
                else:
                    print('1')
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # swith to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                self.user_states.pop(user_id)
                log.info('зарегистрирован: {name} {email}'.format(**state.context))
        else:
            # retry current step
            text_to_send = step['failure_text']
        return text_to_send

    def check_city(self, handler, step, text, state):
        if str(handler).find('city') > -1:
            cities = self.get_city(text)
            if len(cities) < 1:
                text_to_send = step['failure_text']
                return text_to_send
            elif len(cities) > 1:
                text_to_send = 'Найдены следующие города:\n'
                for city, code in cities.items():
                    text_to_send += city + ' (' + code + ')\n'
                text_to_send += step['failure_text']
                return text_to_send
            else:
                handler(text=cities, context=state.context)
        return False

    def get_cities_json(self, cities_file):
        with open(cities_file, "r", encoding="utf-8") as read_file:
            self.cities_json = json.load(read_file)

    def get_city(self, search_str):
        self.city_code = False
        search_str = search_str.lower()
        cities = {}
        for city in self.cities_json:
            if (city['name'] and city['name'].lower().find(search_str) > -1) or \
                    (city['cases']['vi'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                    (city['cases']['tv'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                    (city['cases']['ro'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                    (city['cases']['pr'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                    (city['cases']['da'] and city['cases']['vi'].lower().find(search_str) > -1) or \
                    city['code'].lower() == search_str:
                cities[city['name']] = city['code']
        return cities

    def get_flights(self, state):
        from_station = list(state.context['departure_city'].values())[0]
        to_station = list(state.context['arrival_city'].values())[0]
        date = state.context['date']

        request = requests.get(YA_URL + 'apikey=' + YA_TOKEN +
                               '&format=json&transport_types=plane&system=iata&transfers=false&lang=ru_RU&limit=5' +
                               '&from=' + from_station + '&to=' + to_station + '&date=' + '2020-07-07')
        self.ya_answer = json.loads(request.text)

        return True


if __name__ == "__main__":
    config_log()
    bot = Bot()
    bot.run()
