# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
# Требования к коду: он должен быть готовым к расширению функциональности. Делать сразу на классах.

# После выполнения первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  - по алфавиту по возрастанию
#  - по алфавиту по убыванию
# Для этого пригодится шаблон проектирование "Шаблонный метод" см https://goo.gl/Vz4828

import zipfile
from collections import defaultdict, Counter


class Chatterer:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = defaultdict(lambda: 1)
        self.stat_dic = {}
        self.statistic_sum = 0

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for filename in zfile.namelist():
            zfile.extract(filename)
        self.file_name = filename

    def collect(self):
        if self.file_name.endswith('.zip'):
            self.unzip()
        with open(self.file_name, 'r', encoding='cp1251') as file:
            for line in file:
                self._collect_for_line(line=line[:-1])

    def _collect_for_line(self, line):
        for char in line:
            if char.isalpha():
                self.stat[char] += 1

    def sort_statistic(self, key='alphabet', reverse=False):
        self.statistic_sum = 0
        print('+---------+----------+')
        print('|  буква  | частота  |')
        print('+---------+----------+')
        if key == 'quantity' and not reverse:
            self._quantity_direct_sort()
        elif key == 'quantity' and reverse:
            self._quantity_revers_sort()
        elif key == 'alphabet' and not reverse:
            self._alphabet_direct_sort()
        elif key == 'alphabet' and reverse:
            self._alphabet_reverse_sort()
        print('+---------+----------+')
        print(f'|  Итого  | {self.statistic_sum:8d} |')
        print('+---------+----------+')

    def _alphabet_direct_sort(self):
        for char, quantity in sorted(self.stat.items()):
            self.statistic_sum += quantity
            print(f'|    {char}    | {quantity:8d} |')

    def _alphabet_reverse_sort(self):
        for char, quantity in sorted(self.stat.items(), reverse=True):
            self.statistic_sum += quantity
            print(f'|    {char}    | {quantity:8d} |')

    def _quantity_direct_sort(self):
        for char, quantity in Counter(self.stat).most_common():
            self.statistic_sum += quantity
            print(f'|    {char}    | {quantity:8d} |')

    def _quantity_revers_sort(self):
        for char, quantity in Counter(self.stat).most_common()[::-1]:
            self.statistic_sum += quantity
            print(f'|    {char}    | {quantity:8d} |')


chatterer = Chatterer(file_name='voyna-i-mir.txt.zip')
chatterer.collect()
chatterer.sort_statistic(key='alphabet')
chatterer.sort_statistic(key='alphabet', reverse=True)
chatterer.sort_statistic(key='quantity')
chatterer.sort_statistic(key='quantity', reverse=True)
