# -*- coding: utf-8 -*-
import bot_example_16.settings as settings
try:
    from bot_example_16.settings import TOKEN, GROUP_ID
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

import vk_api
from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
from bot_example_16 import handlers
from models import UserState, Registration

log = logging.getLogger('bot')


def config_log():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M'))

    file_handler = logging.FileHandler('../bot.log')
    file_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M'))

    log.addHandler(handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class Bot:
    """
    Бот-переводчик VK
    Python version 3.7
    """

    def __init__(self, GROUP_ID, TOKEN, to_lang='en', from_lang='ru'):
        """

        :param GROUP_ID: ID группы VK
        :param TOKEN: секретный токен
        :param from_lang: исходный язык, по умолчанию RU
        :param to_lang: язык перевода, по умолчанию EN
        """
        self.group_id = GROUP_ID
        self.token = TOKEN
        self.vk = vk_api.VkApi(token=TOKEN)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        """
        Запуск бота
        """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка обработки')

    @db_session
    def on_event(self, event):
        """
        Обработка события: принтмат сообжение, переводит и отправляет сообщение назад
        :param event: VkBotMessageEvent
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info('Сообщения такого типа не обрабатываются %s', event.type)
            return
        user_id = event.object.peer_id
        text = event.object.text
        state = UserState.get(user_id=str(user_id))

        if state is not None:
            text_to_send = self.continue_scenario(text, state)
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

    def start_scenario(self, user_id, scenario_name):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        text_to_send = step['text']
        UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step, context={})
        return text_to_send

    def continue_scenario(self, text, state):
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]

        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # swith to next step
                state.step_name = step['next_step']
            else:
                # finish scenario
                log.info('зарегистрирован: {name} {email}'.format(**state.context))
                Registration(name=state.context['name'], email=state.context['email'])
                state.delete()
        else:
            # retry current step
            text_to_send = step['failure_text']

        return text_to_send


if __name__ == "__main__":
    config_log()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
