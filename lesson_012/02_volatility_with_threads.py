# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
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

from threading import Thread
import os


class FileHandler(Thread):
    def __init__(self, full_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_path = full_path
        self.ticker = ''
        self.volatility = 0

    def run(self):
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
            self.ticker, self.volatility = ticker, volatility


class VolatilityMeter:

    def __init__(self):
        self.path = self._make_path()
        self.dirpath = self.dirnames = self.filenames = ''
        self.tickers = {}
        self.file_treads = []

    def process(self):

        for self.dirpath, self.dirnames, self.filenames in os.walk(self.path):
            file_list = []
            for filename in self.filenames:
                file_list.append(os.path.join(self.dirpath, filename))
            for file in file_list:
                self.file_treads.append(FileHandler(file))
            for tread in self.file_treads:
                tread.start()
            for tread in self.file_treads:
                tread.join()
            for tread in self.file_treads:
                self.tickers[tread.ticker] = tread.volatility
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
volatility_handler.process()

