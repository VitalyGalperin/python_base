# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

import time


# После выполнения первого этапа нужно сделать группировку событий
#  - по часам
#  - по месяцу
#  - по году
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828


class Parser:

    def __init__(self, log_file, result_file, group_interval='minute', ):
        self.log_file = log_file
        self.result_file = result_file
        self.group_interval = group_interval

    def log_parsing(self):
        group_file = open(self.result_file, mode='w', encoding='utf8')
        with open(self.log_file, mode='r', encoding='utf8') as file:
            log_datetime = []
            event_count = 0
            date_slice = self._time_interval_choice()
            for line in file:
                if log_datetime == line[1:date_slice]:
                    if line[29] == 'N':
                        event_count += 1
                else:
                    if event_count > 0:
                        group_file.write(f'[{log_datetime}] {event_count}\n')
                    log_datetime = line[1:date_slice]
                    if line[29] == 'N':
                        event_count = 1
                    else:
                        event_count = 0
            group_file.write(f'[{log_datetime}] {event_count}\n')
        group_file.close()

    def _time_interval_choice(self):
        if self.group_interval == 'minute':
            date_slice = self._minute_slice()
        elif self.group_interval == 'hour':
            date_slice = self._hour_slice()
        elif self.group_interval == 'day':
            date_slice = self._day_slice()
        elif self.group_interval == 'month':
            date_slice = self._month_slice()
        elif self.group_interval == 'year':
            date_slice = self._year_slice()
        else:
            date_slice = self._withot_slice()
        return date_slice

    def _withot_slice(self):
        date_slice = 20
        return date_slice

    def _year_slice(self):
        date_slice = 5
        return date_slice

    def _month_slice(self):
        date_slice = 8
        return date_slice

    def _day_slice(self):
        date_slice = 11
        return date_slice

    def _hour_slice(self):
        date_slice = 14
        return date_slice

    def _minute_slice(self):
        date_slice = 17
        return date_slice


log_minute = Parser(log_file='events.txt', result_file='statistics_minute.txt', group_interval='minute')
log_minute.log_parsing()
log_hour = Parser(log_file='events.txt', result_file='statistics_hour.txt', group_interval='hour')
log_hour.log_parsing()
log_day = Parser(log_file='events.txt', result_file='statistics_day.txt', group_interval='day')
log_day.log_parsing()
log_month = Parser(log_file='events.txt', result_file='statistics_month.txt', group_interval='month')
log_month.log_parsing()
log_year = Parser(log_file='events.txt', result_file='statistics_year.txt', group_interval='year')
log_year.log_parsing()
