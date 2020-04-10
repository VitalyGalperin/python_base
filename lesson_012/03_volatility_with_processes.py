# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
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
from multiprocessing import Process, Queue, cpu_count
import os


class FileHandler(Process):
    def __init__(self, full_path, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.full_path = full_path
        self.queue = queue
        self.tickers = {}

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
            self.tickers[ticker] = volatility
            self.queue.put(self.tickers)


class VolatilityMeter:

    def __init__(self):
        self.path = self._make_path()
        self.dirpath = self.dirnames = self.filenames = ''
        self.file_processes = []
        self.tickers = {}
        self.queue = Queue(maxsize=cpu_count())

    def process(self):
        for self.dirpath, self.dirnames, self.filenames in os.walk(self.path):
            for filename in self.filenames:
                self.file_processes.append(FileHandler(os.path.join(self.dirpath, filename), queue=self.queue))
            for process in self.file_processes:
                process.start()
            for process in self.file_processes:
                self.tickers.update(self.queue.get())
            for process in self.file_processes:
                process.join()
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
        sorted_tickers = list(filtered_tickers.keys())
        sorted_tickers.sort()
        print(' '.join(sorted_tickers))


if __name__ == '__main__':
    volatility_handler = VolatilityMeter()
    volatility_handler.process()
