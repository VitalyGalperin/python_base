# -*- coding: utf-8 -*-

# На основе своего кода из lesson_009/02_log_parser.py напишите итератор (или генератор)
# котрый читает исходный файл events.txt и выдает число событий NOK за каждую минуту
# <время> <число повторений>
#
# пример использования:
#
# grouped_events = <создание итератора/генератора>
# for group_time, event_count in grouped_events:
#     print(f'[{group_time}] {event_count}')
#
# на консоли должно появится что-то вроде
#
# [2018-05-17 01:57] 1234


def file_group_events(log_file):
    with open(log_file, mode='r', encoding='utf8') as file:
        nok_count = 0
        log_datetime = []
        for line in file:
            if log_datetime == line[1:17]:
                if line[29] == 'N':
                    nok_count += 1
            else:
                if nok_count > 0:
                    yield log_datetime, nok_count
                log_datetime = line[1:17]
                if line[29] == 'N':
                    nok_count = 1
                else:
                    nok_count = 0
        if nok_count > 0:
            yield log_datetime, nok_count

# TODO если переформатировать
# код то line[29] == 'N' и line[1:date_slice] можно вызывать один раз.
# Постарайтесь избегать дублирования логики

grouped_events = file_group_events(log_file='events.txt')
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')
