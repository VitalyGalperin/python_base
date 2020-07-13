from unittest import TestCase
from unittest.mock import patch, Mock
import settings
from vk_api.bot_longpoll import VkBotMessageEvent
from copy import deepcopy
import ya_rasp
import requests_answers

from bot import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1587198847, 'from_id': 184926257, 'id': 308, 'out': 0, 'peer_id': 184926257,
                            'text': 'Тест', 'conversation_message_id': 307, 'fwd_messages': [], 'important': False,
                            'random_id': 0, 'attachments': [], 'is_hidden': False}, 'group_id': 194114072,
                 'event_id': '42aff60c0a9e7fd9f563ca8b6231b15ab8f3045c'}

    BOT_ANSWERS = ['Принято:\nНижний Новгород (GOJ)\n',
                   'Принято:\nАнталья (AYT)\n',
                   'Невозможно найти билет на прошедшую дату',
                   'Не можем искать билет более, чем на год вперёд',
                   '1 : N4 1879: Нижний Новгород — Анталья \n2020-08-31 06:20:00+03:00\n'
                   '2 : N4 1879: Нижний Новгород — Анталья \n2020-09-02 06:20:00+03:00\n'
                   '3 : N4 1879: Нижний Новгород — Анталья \n2020-09-02 06:20:00+03:00\n'
                   '4 : N4 1879: Нижний Новгород — Анталья \n2020-09-04 06:20:00+03:00\n'
                   '5 : N4 1879: Нижний Новгород — Анталья \n2020-09-04 06:20:00+03:00\n',
                   'Найдены следующие города:\nЛондон (LOZ)\nИст-Лондон (ELS)\nНью Лондон (GON)\nУточните выбор',
                   'Принято:\nЛондон (LOZ)\n',
                   'Принято:\nЭйлат (VDA)\n',
                   'Рейсы не найдены',
                   'Принято:\nРостов-на-Дону (ROV)\n',
                   'Принято:\nНорильск (NSK)\n',
                   '1 : Y7 918: Ростов-на-Дону — Норильск \n2020-07-22 06:30:00+07:00\n'
                   '2 : Y7 918: Ростов-на-Дону — Норильск \n2020-07-24 06:30:00+07:00\n'
                   ]

    REQUESTS_ANSWERS = requests_answers.REQUESTS_ANSWERS

    def request_answer(self):
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
        'нижний',
        'в анталью',
        '31082020',
        '31-08-2019',
        '31-08-2023',
        '31-08-2020',
        '5',
        '3',
        'с обедом',
        'принято',
        'да',
        '+972-50-77-777-77',
        'дальше',
        '/ticket',
        'лондон',
        'loz',
        'Эйлат',
        '01-09-2020',
        'Продолжаем',
        '/help',
        'закажи место',
        'ростов',
        'НОРИЛЬСК',
        '20-07-2020',
        '5',
        '2',
        '3',
        '2 багажных места',
        'yes',
        '89200101010'
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
        settings.SCENARIOS['registration']['steps']['step5']['text'],
        settings.SCENARIOS['registration']['steps']['step6']['text'],
        settings.SCENARIOS['registration']['steps']['step7']['text'],
        settings.SCENARIOS['registration']['steps']['step7']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step8']['text'],
        settings.SCENARIOS['registration']['steps']['last_step']['text'].format(phone='+972-50-77-777-77'),
        settings.INTENTS[0]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        BOT_ANSWERS[5],
        BOT_ANSWERS[6] + settings.SCENARIOS['registration']['steps']['step2']['text'],
        BOT_ANSWERS[7] + settings.SCENARIOS['registration']['steps']['step3']['text'],
        BOT_ANSWERS[8],
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        BOT_ANSWERS[9] + settings.SCENARIOS['registration']['steps']['step2']['text'],
        BOT_ANSWERS[10] + settings.SCENARIOS['registration']['steps']['step3']['text'],
        BOT_ANSWERS[11] + settings.SCENARIOS['registration']['steps']['step4']['text'],
        settings.SCENARIOS['registration']['steps']['step4']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step5']['text'],
        settings.SCENARIOS['registration']['steps']['step6']['text'],
        settings.SCENARIOS['registration']['steps']['step7']['text'],
        settings.SCENARIOS['registration']['steps']['step8']['text'],
        settings.SCENARIOS['registration']['steps']['last_step']['text'].format(phone='89200101010'),
    ]

    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock
        ya_mock = Mock()
        # ya_request_mock = Mock(return_value=next(self.request_answer()))
        ya_request_mock = Mock(return_value=self.request_answer())
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

            ya_rasp.request_ya_rasp = ya_request_mock
            bot.run()

            assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        # for c, i in enumerate(real_outputs[7]):
        #     # print(i, self.EXPECTED_OUTPUTS[7][i], i == self.EXPECTED_OUTPUTS[7][i])
        #     print(ord(i), i, '|', ord(self.EXPECTED_OUTPUTS[7][c]), self.EXPECTED_OUTPUTS[7][c], i == self.EXPECTED_OUTPUTS[7][c])
        # print(len(real_outputs[7]), len(self.EXPECTED_OUTPUTS[7]), real_outputs[7] == self.EXPECTED_OUTPUTS[7])

        for c, i in enumerate(real_outputs):
            if real_outputs[c] != self.EXPECTED_OUTPUTS[c]:
                print(real_outputs[c])
                print(self.EXPECTED_OUTPUTS[c])

        assert real_outputs == self.EXPECTED_OUTPUTS


if __name__ == '__main__':
    unittest.main()
