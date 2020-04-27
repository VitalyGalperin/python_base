from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot


class Test1(TestCase):
    SEND_EVENT = {'type': 'message_new',
                  'object': {'date': 1587198847, 'from_id': 184926257, 'id': 308, 'out': 0, 'peer_id': 184926257,
                             'text': 'Тест', 'conversation_message_id': 307, 'fwd_messages': [], 'important': False,
                             'random_id': 0, 'attachments': [], 'is_hidden': False}, 'group_id': 194114072,
                  'event_id': '42aff60c0a9e7fd9f563ca8b6231b15ab8f3045c'}

    GET_EVENT = {'type': 'message_new',
                 'object': {'date': 1587198847, 'from_id': 184926257, 'id': 308, 'out': 0, 'peer_id': 184926257,
                            'text': 'Test', 'conversation_message_id': 307, 'fwd_messages': [], 'important': False,
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
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.SEND_EVENT)
        send_mock = Mock()
        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.on_translate = Mock(return_value=self.GET_EVENT['object']['text'])
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)
        send_mock.assert_called_once_with(message=self.GET_EVENT['object']['text'],
                                          random_id=ANY,
                                          peer_id=self.GET_EVENT['object']['peer_id']
                                          )


if __name__ == '__main__':
    unittest.main()
