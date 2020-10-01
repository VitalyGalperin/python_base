from unittest import TestCase
from unittest.mock import patch, Mock
import settings
from vk_api.bot_longpoll import VkBotMessageEvent
from copy import deepcopy
import ya_rasp
import requests_answers
import datetime
from pony.orm import db_session, rollback

from bot import Bot

from generate_ticket import generate_ticket


def isilate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1587198847, 'from_id': 184926257, 'id': 308, 'out': 0, 'peer_id': 184926257,
                            'text': 'Тест', 'conversation_message_id': 307, 'fwd_messages': [], 'important': False,
                            'random_id': 0, 'attachments': [], 'is_hidden': False}, 'group_id': 194114072,
                 'event_id': '42aff60c0a9e7fd9f563ca8b6231b15ab8f3045c'}

    BOT_ANSWERS = ['Принято:\nНижний Новгород (GOJ)\n',
                   'Принято:\nМосква (MOW)\n',
                   'Невозможно найти билет на прошедшую дату',
                   'Не можем искать билет более, чем на год вперёд',
                   '1 : SU 1223: Нижний Новгород — Москва \n2020-12-01 04:40:00+03:00\n'
                   '2 : S7 1094: Нижний Новгород — Москва \n2020-12-01 10:05:00+03:00\n'
                   '3 : SU 1221: Нижний Новгород — Москва \n2020-12-01 11:40:00+03:00\n'
                   '4 : S7 1096: Нижний Новгород — Москва \n2020-12-01 14:55:00+03:00\n'
                   '5 : SU 1227: Нижний Новгород — Москва \n2020-12-01 15:20:00+03:00\n',
                   ]

    REQUESTS_ANSWERS = requests_answers.REQUESTS_ANSWERS

    def request_answer(self, *args, **kwargs):
        for request in self.REQUESTS_ANSWERS:
            yield request

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot()
                bot.on_event = Mock()

                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    INPUTS = [
        'Привет',
        'Хочу заказать билет',
        'GOJ',
        'в москву',
        datetime.datetime.now().strftime("%d%m%Y"),
        (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%d-%m-%Y"),
        (datetime.datetime.now() + datetime.timedelta(days=366)).strftime("%d-%m-%Y"),
        (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y"),
        '6',
        '4',
        '3',
        'с обедом',
        'Виталий',
        'Гальперин',
        'vitalygl@yandex.ru',
        '+7972507678975',
        'принято',
        'да',
    ]

    EXPECTED_OUTPUTS = [
        settings.INTENTS[0]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        BOT_ANSWERS[0] + settings.SCENARIOS['registration']['steps']['step2']['text'],
        BOT_ANSWERS[1] + settings.SCENARIOS['registration']['steps']['step3']['text'],
        settings.SCENARIOS['registration']['steps']['step3']['failure_text'],
        BOT_ANSWERS[2],
        BOT_ANSWERS[3],
        BOT_ANSWERS[4] + settings.SCENARIOS['registration']['steps']['step4']['text'],
        settings.SCENARIOS['registration']['steps']['step4']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step5']['text'],
        settings.SCENARIOS['registration']['steps']['step6']['text'],
        settings.SCENARIOS['registration']['steps']['step7']['text'],
        settings.SCENARIOS['registration']['steps']['step8']['text'],
        settings.SCENARIOS['registration']['steps']['step9']['text'],
        settings.SCENARIOS['registration']['steps']['step10']['text'],
        settings.SCENARIOS['registration']['steps']['step11']['text'],
        settings.SCENARIOS['registration']['steps']['step11']['failure_text'],
        settings.SCENARIOS['registration']['steps']['last_step']['text'].format(phone='+7972507678975',
                                                                                email='vitalygl@yandex.ru'),
    ]

    @isilate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock
        ya_mock = Mock()
        ya_request_mock = Mock(return_value=next(self.request_answer()))
        ya_mock.request_ya_rasp = ya_request_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot()
            bot.api = api_mock
            bot.send_image = Mock()
            ya_rasp.request_ya_rasp = ya_request_mock
            bot.run()

            assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])

        for c, i in enumerate(real_outputs):
            if real_outputs[c] != self.EXPECTED_OUTPUTS[c]:
                print(real_outputs[c], ' real')
                print(self.EXPECTED_OUTPUTS[c], ' expected')

        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        with open("sourсes/avatar.png", "rb") as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()

        with patch('requests.get', return_value=avatar_mock):
            ticket_file = generate_ticket('Виталий', 'Гальперин', 'Нижний Новгород (GOJ)', '01-12-2020', '14:55+03:00',
                                          'Москва (MOW)', 'S7 1096')
        with open('sourсes/ticket_to_test.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file.read() == expected_bytes


if __name__ == '__main__':
    unittest.main()
