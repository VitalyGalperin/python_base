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

    BOT_ANSWERS = ['Принято:\nНижний Новгород (GOJ)\n',
                   'Принято:\nАнталья (AYT)\n',
                   'Невозможно найти билет на прошедшую дату',
                   'Не можем искать билет более, чем на год вперёд',
                   '1 : N4 1879: Нижний Новгород — Анталья\n2020-08-31 06:20:00+03:00\n2 : N4 1879: Нижний Новгород — Анталья\n2020-09-02 06:20:00+03:00\n3 : N4 1879: Нижний Новгород — Анталья\n2020-09-02 06:20:00+03:00\n4 : N4 1879: Нижний Новгород — Анталья\n2020-09-04 06:20:00+03:00\n5 : N4 1879: Нижний Новгород — Анталья\n2020-09-04 06:20:00+03:00\n',
                   'Найдены следующие города:\nЛондон (LOZ)\nИст-Лондон (ELS)\nНью Лондон (GON)\nУточните выбор',
                   'Принято:\nЛондон (LOZ)',
                   'Принято:\nЭйлат (VDA)',
                   'Рейсы не найдены',
                   'Принято:\nРостов-на-Дону (ROV)',
                   'Принято:\nНорильск (NSK)',
                   '1 : Y7 918: Ростов-на-Дону — Норильск\n2020-07-22 06:30:00+07:00\n2 : Y7 918: Ростов-на-Дону — Норильск\n2020-07-24 06:30:00+07:00\n'
                   ]

    REQUESTS_ANSWERS = ['{"interval_segments":[],"pagination":{"total":1,"limit":5,"offset":0},"segments":[{"arrival":"2020-08-31T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-08-31&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-08-31T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-08-31","arrival_platform":""}],"search":{"date":"2020-08-31","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":4,"offset":0},"segments":[{"arrival":"2020-09-02T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-02&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-02T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-02","arrival_platform":""}],"search":{"date":"2020-09-01","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":3,"offset":0},"segments":[{"arrival":"2020-09-02T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-02&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-02T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-02","arrival_platform":""}],"search":{"date":"2020-09-02","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":2,"offset":0},"segments":[{"arrival":"2020-09-04T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-04&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-04T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-04","arrival_platform":""}],"search":{"date":"2020-09-03","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":1,"offset":0},"segments":[{"arrival":"2020-09-04T06:20:00+03:00","from":{"code":"s9623052","title":"Стригино","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"N4-1879_2_c2543_547","title":"Нижний Новгород — Анталья","number":"N4 1879","short_title":"Нижний Новгород — Анталья","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-09-04&uid=N4-1879_2_c2543_547","carrier":{"code":2543,"contacts":"Телефон: +7 (495) 730-43-30; факс: +7 (495) 730-25-93.","url":"http://www.nordwindairlines.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordwind.svg","title":"Северный ветер (Nordwind)","phone":"","codes":{"icao":"NWS","sirena":"КЛ","iata":"N4"},"address":"141426, Московская обл., Химкинский р-н, аэропорт \"Шереметьево-1\", а/я 44","logo":null,"email":"nws@nordwindairlines.ru"},"transport_type":"plane","vehicle":"Airbus А321","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-09-04T02:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":13200.0,"arrival_terminal":null,"start_date":"2020-09-04","arrival_platform":""}],"search":{"date":"2020-09-04","to":{"code":"s9623581","title":"Анталья","station_type":"airport","popular_title":null,"short_title":null,"transport_type":"plane","station_type_name":"аэропорт","type":"station"},"from":{"code":"c23243","type":"settlement","popular_title":"Нижний Новгород","short_title":"Нижний Новгород","title":"Нижний Новгород"}}}',

                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-01","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-02","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-03","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-04","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-05","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-06","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-09-07","to":{"code":"c40051","type":"settlement","popular_title":"Овда","short_title":"Овда","title":"Овда"},"from":{"code":"s9634992","title":"Лондон","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"}}}'
                        
                        '{"interval_segments":[],"pagination":{"total":0,"limit":5,"offset":0},"segments":[],"search":{"date":"2020-07-20","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":5,"offset":0},"segments":[{"arrival":"2020-07-22T06:30:00+07:00","from":{"code":"s9866615","title":"Платов","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"Y7-918_1_c1364_547","title":"Ростов-на-Дону — Норильск","number":"Y7 918","short_title":"Ростов-на-Дону — Норильск","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-07-21&uid=Y7-918_1_c1364_547","carrier":{"code":1364,"contacts":"","url":"https://www.nordstar.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordstar2.svg","title":"Нордстар","phone":"8-800-700-8-007","codes":{"icao":null,"sirena":"ТИ","iata":"Y7"},"address":null,"logo":null,"email":null},"transport_type":"plane","vehicle":"Boeing 737-800","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-07-21T18:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9600385","title":"Норильск","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":28200.0,"arrival_terminal":null,"start_date":"2020-07-21","arrival_platform":""}],"search":{"date":"2020-07-21","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":4,"offset":0},"segments":[],"search":{"date":"2020-07-22","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}',
                        '{"interval_segments":[],"pagination":{"total":1,"limit":4,"offset":0},"segments":[{"arrival":"2020-07-24T06:30:00+07:00","from":{"code":"s9866615","title":"Платов","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"},"thread":{"uid":"Y7-918_1_c1364_547","title":"Ростов-на-Дону — Норильск","number":"Y7 918","short_title":"Ростов-на-Дону — Норильск","thread_method_link":"api.rasp.yandex.net/v3/thread/?date=2020-07-23&uid=Y7-918_1_c1364_547","carrier":{"code":1364,"contacts":"","url":"https://www.nordstar.ru/","logo_svg":"//yastat.net/s3/rasp/media/data/company/svg/nordstar2.svg","title":"Нордстар","phone":"8-800-700-8-007","codes":{"icao":null,"sirena":"ТИ","iata":"Y7"},"address":null,"logo":null,"email":null},"transport_type":"plane","vehicle":"Boeing 737-800","transport_subtype":{"color":null,"code":null,"title":null},"express_type":null},"departure_platform":"","departure":"2020-07-23T18:40:00+03:00","stops":"","departure_terminal":null,"to":{"code":"s9600385","title":"Норильск","station_type":"airport","popular_title":"","short_title":"","transport_type":"plane","station_type_name":"аэропорт","type":"station"},"has_transfers":false,"tickets_info":{"et_marker":false,"places":[]},"duration":28200.0,"arrival_terminal":null,"start_date":"2020-07-23","arrival_platform":""}],"search":{"date":"2020-07-23","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":3,"offset":0},"segments":[],"search":{"date":"2020-07-24","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":3,"offset":0},"segments":[],"search":{"date":"2020-07-25","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}',
                        '{"interval_segments":[],"pagination":{"total":0,"limit":3,"offset":0},"segments":[],"search":{"date":"2020-07-26","to":{"code":"c11311","type":"settlement","popular_title":"Норильск","short_title":"Норильск","title":"Норильск"},"from":{"code":"c39","type":"settlement","popular_title":"Ростов-на-Дону","short_title":"Ростов-на-Дону","title":"Ростов-на-Дону"}}}'
                        ]

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
