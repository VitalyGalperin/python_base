from unittest import TestCase
from unittest.mock import patch, Mock
import bot_example_16.settings as settings
from vk_api.bot_longpoll import VkBotMessageEvent
from copy import deepcopy
from pony.orm import db_session, rollback


from bot import Bot
from generate_ticket import generate_ticket


def isilate_db(test_func):
    def wrapper(*args, ** kwargs):
        with db_session:
            test_func(*args, ** kwargs)
            rollback()
    return wrapper


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                  'object': {'date': 1587198847, 'from_id': 184926257, 'id': 308, 'out': 0, 'peer_id': 184926257,
                             'text': 'Тест', 'conversation_message_id': 307, 'fwd_messages': [], 'important': False,
                             'random_id': 0, 'attachments': [], 'is_hidden': False}, 'group_id': 194114072,
                  'event_id': '42aff60c0a9e7fd9f563ca8b6231b15ab8f3045c'}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()
                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count
    INPUTS = [
        'Привет',
        'А когда?',
        'Где будет конференция?',
        'Зарегистрируйте меня',
        'Вася',
        'мой адрес asddf@jeee',
        'asddf@jeee.ru'
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['text'],
        settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Вася', email='asddf@jeee.ru')
    ]

    @isilate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

            assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        with open("files/avatar.png", "rb") as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()

        with patch('requests.get', return_value=avatar_mock):
            ticket_file = generate_ticket('Vasily', 'vasily@ghj.kjn')

        with open('files/ticket_example.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file.read() == expected_bytes


if __name__ == '__main__':
    unittest.main()
