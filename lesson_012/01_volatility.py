# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от средней цены за торговую сессию:
#   средняя цена = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / средняя цена) * 100%
# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
#   average_price = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / average_price) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base_source/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
import os


class FileHandler:
    def __init__(self, full_path):
        self.full_path = full_path

    def processing(self):
        with open(self.full_path, mode='r', encoding='utf8') as file:
            min_price = max_price = 0
            for line in file:
                ticker, time, price, volume = line.split(',')
                try:
                    price = float(price)
                except ValueError:
                    continue
                if not min_price or price < min_price:
                    min_price = price
                if price > max_price:
                    max_price = price
            average_price = (max_price + min_price) / 2
            try:
                volatility = ((max_price - min_price) / average_price) * 100
            except ZeroDivisionError:
                volatility = 0
            return ticker, volatility


class VolatilityMeter:

    def __init__(self):
        self.path = self._make_path()
        self.dirpath = self.dirnames = self.filenames = ''
        self.tickers = {}

    def run(self):
        for self.dirpath, self.dirnames, self.filenames in os.walk(self.path):
            for filename in self.filenames:
                full_path = os.path.join(self.dirpath, filename)
                file = FileHandler(full_path)
                ticker, volatility = file.processing()
                self.tickers[ticker] = volatility
            self._print_max_tickers(tickers_number=3)
            self._print_min_tickers(tickers_number=3)
            self._print_zero_tickers()

    def _make_path(self):
        return os.path.join(os.getcwd(), 'trades')

    def _print_max_tickers(self, tickers_number=0):
        print('Максимальная волатильность:')
        for ticker, volatility in sorted(self.tickers.items(), key=lambda x: x[1], reverse=True)[:tickers_number]:
            print(f'    {ticker} -{volatility:6.2f} %')

    def _print_min_tickers(self, tickers_number=0):
        print('Минимальная волатильность:')
        filtered_tickers = filter(lambda x: x[1] != 0, self.tickers.items())
        for ticker, volatility in sorted(filtered_tickers, key=lambda x: x[1])[:tickers_number]:
            print(f'    {ticker} -{volatility:6.2f} %')

    def _print_zero_tickers(self):
        print('Нулевая волатильность:')
        filtered_tickers = dict(filter(lambda x: x[1] == 0, self.tickers.items()))
        print(' '.join(filtered_tickers.keys()))


volatility_handler = VolatilityMeter()
volatility_handler.run()


# Зачет
