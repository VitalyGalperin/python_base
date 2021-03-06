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
        log_datetime, nok_count = None, 0
        for line in file:
            new_log_datetime = line[1:17]
            if log_datetime and new_log_datetime != log_datetime and nok_count:
                yield log_datetime, nok_count
                nok_count = 0

            log_datetime = new_log_datetime
            nok_count += line[29] == 'N'

        if log_datetime:
            yield log_datetime, nok_count


grouped_events = file_group_events(log_file='events.txt')
for group_time, event_count in grouped_events:
    print(f'[{group_time}] {event_count}')

# Зачет