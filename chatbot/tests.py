from unittest import TestCase
from unittest.mock import patch, Mock
import settings
from vk_api.bot_longpoll import VkBotMessageEvent
from copy import deepcopy

from bot import Bot


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1587198847, 'from_id': 184926257, 'id': 308, 'out': 0, 'peer_id': 184926257,
                            'text': 'Тест', 'conversation_message_id': 307, 'fwd_messages': [], 'important': False,
                            'random_id': 0, 'attachments': [], 'is_hidden': False}, 'group_id': 194114072,
                 'event_id': '42aff60c0a9e7fd9f563ca8b6231b15ab8f3045c'}

    BOT_ANSWERS = ['Принято:\nНижний Новгород (GOJ)\nВведите название или код города прибытия:',
                   'Принято:\nАнталья (AYT)\nВедите дату выдета (DD-MM-YYYY):',
                   'Невозможно найти билет на прошедшую дату',
                   'Не можем искать билет более, чем на год вперёд',
                   ]

    REQUESTS_ANSWERS = ['{"interval_segments":[],"pagination":{"total":1,"limit":5,"offset":0},"segments":[{"arrival":"2020-08-31T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-08-31&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-08-31T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-08-31","arrival_platform":""}],"search":{"date":"2020-08-31","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":4,"offset":0},"segments":[{"arrival":"2020-09-02T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-02&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-02T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-02","arrival_platform":""}],"search":{"date":"2020-09-01","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":3,"offset":0},"segments":[{"arrival":"2020-09-02T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-02&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-02T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-02","arrival_platform":""}],"search":{"date":"2020-09-02","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":2,"offset":0},"segments":[{"arrival":"2020-09-04T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-04&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-04T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-04","arrival_platform":""}],"search":{"date":"2020-09-03","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":1,"offset":0},"segments":[{"arrival":"2020-09-04T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-04&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-04T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-04","arrival_platform":""}],"search":{"date":"2020-09-04","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}']

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
        # '31-08-2020',


        # '5',
        # '3',
        # 'с обедом',
        # 'принято',
        # 'да',
        # '+972-50-77-777-77',
        # 'дальше'
        # '/ticket',
        # 'лондон',
        # 'loz',
        # 'Эйлат',
        # '01-09-2020',
        # 'Продолжаем',
        # '/help',
        # 'закажи место',
        # 'ростов',
        # 'НОРИЛЬСК',
        # '20-07-2020',
        # '5',
        # '2',
        # '3',
        # '2 багажных места',
        # 'yes',
        # '89200101010'
    ]

    EXPECTED_OUTPUTS = [
        # settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        # settings.INTENTS[1]['answer'],
        settings.SCENARIOS['registration']['steps']['step1']['text'],
        BOT_ANSWERS[0],
        BOT_ANSWERS[1],
        settings.SCENARIOS['registration']['steps']['step3']['failure_text'],
        BOT_ANSWERS[2],
        BOT_ANSWERS[3]
        # settings.SCENARIOS['registration']['steps']['step2']['failure_text'],
        # settings.SCENARIOS['registration']['steps']['step3']['text'].format(name='Вася', email='asddf@jeee.ru')
    ]

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
            bot = Bot()
            bot.api = api_mock
            bot.run()

            assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])
        assert real_outputs == self.EXPECTED_OUTPUTS


if __name__ == '__main__':
    unittest.main()
