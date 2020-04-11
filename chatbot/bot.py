# -*- coding: utf-8 -*-

from _token import token
import vk_api
import vk_api.bot_longpoll

group_id = 194114072


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

    def run(self):
        for event in self.long_poller.listen():
            print('1')
            self.on_event(event)
            print('2')

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            print(event.object.text)
        else:
            print(event)


if __name__ == "__main__":
    bot = Bot(group_id, token)
    bot.run()
