# -*- coding: utf-8 -*-
try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging
import random
from translate import Translator

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
        self.translator = Translator(to_lang, from_lang)

    def run(self):
        """
        Запуск бота
        """
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('Ошибка обработки')

    def on_event(self, event):
        """
        Обработка события: принтмат сообжение, переводит и отправляет сообщение назад
        :param event: VkBotMessageEvent
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info('Обработка сообщения')
            try:
                if not event.object.text:
                    send_message = 'В сообщении отсутствует текст'
                elif len(event.object.text) > 500:
                    send_message = 'Максимальная длина текста для перевода: 500 знаков'
                else:
                    send_message = self.on_translate(event)
                self.api.messages.send(message=send_message,
                                       random_id=random.randint(0, 2 ** 20),
                                       peer_id=event.object.peer_id, )
            except Exception:
                log.exception('Ошибка сообщения')
        else:
            log.debug('Сообщения такого типа не обрабатываются %s', event.type)

    def on_translate(self, event):
        """
        Перевод переданного сообщения
        :param event: VkBotMessageEvent
        :return: str, переведённый текст
        """
        try:
            translation = self.translator.translate(event.object.text)
        except Exception as err:
            translation = 'Перевод не удался'
        return translation


if __name__ == "__main__":
    config_log()
    bot = Bot(GROUP_ID, TOKEN)
    bot.run()
