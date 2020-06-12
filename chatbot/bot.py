# -*- coding: utf-8 -*-
try:
    from settings import TOKEN, GROUP_ID, YA_TOKEN, YA_URL
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
import settings
import handlers
import json
import requests

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
        self.airports_file = 'airports.json'

        self.vk = vk_api.VkApi(token=TOKEN)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

        self.cities_json = self.airports_json = self.ya_answer = None
        self.user_states = dict()
        self.cities = []
        self.first_event = True

    def run(self):
        """
        Запуск бота
        """
        self.get_cities_json(self.cities_file)
        self.get_airports_json(self.airports_file)
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
            return
        user_id = event.object.peer_id
        text = event.object.text
        if self.first_event:
            self.hello_massage(event)
            self.first_event = False
            return
        if user_id in self.user_states:
            text_to_send = self.continue_scenario(user_id, text)
        else:
            # search intevt
            for intent in settings.INTENTS:
                log.debug(f'user get {intent}')
                if any(token in text.lower() for token in intent['tokens']):
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])
                    break
            else:
                text_to_send = settings.DEFAULT_ANSWER

        self.api.messages.send(
            message=text_to_send,
            random_id=random.randint(0, 2 ** 20),
            peer_id=event.object.peer_id, )

        # self.ya_answer = requests.get(YA_URL + 'apikey=' + YA_TOKEN + '&system=iata&station=' + 'LED')
        # a = json.loads(self.ya_answer)

        # self.ya_answer = requests.get(YA_URL + 'apikey=' + YA_TOKEN + '&system=iata&station=' + 'MOW')
        # print(self.ya_answer)
        # a = json.loads(self.ya_answer)

        a = requests.get(
            'http://api.travelpayouts.com/v1/prices/direct?origin=MOW&destination=LED&depart_date=2020-06&token=7ef952b2fa4b61f0439c0cc5a24c6fac',
            {
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip,deflate,sdch',
                'Content-Type': 'application/json',
                'X-Access-Token': '7ef952b2fa4b61f0439c0cc5a24c6fac'
            })
        print(a)

    def start_scenario(self, user_id, scenario_name):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=first_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            self.get_city('ква')
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

    def get_cities_json(self, cities_file):
        with open(cities_file, "r", encoding="utf-8") as read_file:
            self.cities_json = json.load(read_file)

    def get_airports_json(self, airports_file):
        with open(airports_file, "r", encoding="utf-8") as read_file:
            self.airports_json = json.load(read_file)

    def get_city(self, search_str):
        search_str = search_str.upper()
        print(search_str)
        for city in self.cities_json:
            upper_ru_name = ''
            if city['name']:
                upper_ru_name = city['name'].upper()
            upper_en_name = city['name_translations']['en'].upper()
            if upper_ru_name.find(search_str) > -1 or upper_en_name.find(search_str) > -1:
                self.cities.append(city['code'])

    def hello_massage(self, event):
        self.api.messages.send(
            message= 'Здравствуйте!!!\nВас приветствует Бот по заказу Авиабилетов!\n'
                  'Для начала заказа билета:     наберите /ticket\n'
                  'Для получения подробной справки:     наберите /help',
            random_id=random.randint(0, 2 ** 20),
            peer_id=event.object.peer_id, )


if __name__ == "__main__":
    config_log()
    bot = Bot()
    bot.run()
