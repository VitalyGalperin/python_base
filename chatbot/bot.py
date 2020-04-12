# -*- coding: utf-8 -*-

from _token import token
import vk_api
import vk_api.bot_longpoll
import random
from translate import Translator

group_id = 194114072


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                print(event)
                self.on_event(event)
            except Exception as err:
                print(err)

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            if not event.object.text:
                a = 'В сообщении отсутствует текст'
                self.on_send(event, a)
            elif len(event.object.text) > 499:
                a = 'Максимальная длина текста для перевода: 500 знаков'
                self.on_send(event, a)
            else:
                a = self.on_translate(event)
                self.on_send(event, a)

    def on_translate(self, event, from_lang='ru', to_lang='en'):
        translator = Translator(to_lang, from_lang)
        try:
            translation = translator.translate(event.object.text)
        except Exception as err:
            translation = 'Перевод не удался'
        return translation

    def on_send(self, event, a):
        self.api.messages.send(message=a,
                               random_id=random.randint(0, 2 ** 20),
                               peer_id=event.object.peer_id, )


if __name__ == "__main__":
    bot = Bot(group_id, token)
    bot.run()
