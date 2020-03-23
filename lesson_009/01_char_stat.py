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


class Chatterer:

    def __init__(self, file_name):
        self.file_name = file_name
        self.stat = {}  # TODO удобнее defaultdict from collections
        self.printing_stat = ()

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
        self.printing_stat = list(self.stat.items())  # TODO self.stat.items() можно сортировать напрямую

    def _collect_for_line(self, line):
        for char in line:
            if char.isalpha():
                if char in self.stat:
                    self.stat[char] += 1
                else:
                    self.stat[char] = 1

    def sort_statistic(self, key='alphabet', reverse=False):
        # TODO сделали почти правильно, хотелось бы увидеть паттерн шаблонный метод с базовым классом
        #  и 4 наследниками
        if key == 'quantity' and not reverse:
            self.printing_stat = sorted(self.stat.items(), key=lambda item: -item[1])  # TODO параметр reverse
            # более информативен
        elif key == 'quantity' and reverse:
            self.printing_stat = sorted(self.stat.items(), key=lambda item: item[1])
        elif key == 'alphabet' and not reverse:
            self.printing_stat = sorted(self.stat.items(), key=lambda item: item[0])
        elif key == 'alphabet' and reverse:
            self.printing_stat = sorted(self.stat.items(), key=lambda item: -ord(item[0]))  # TODO параметр reverse
            # более информативен
        self._print_statistic()

    def _print_statistic(self):
        global char
        statistic_sum = 0
        print('+---------+----------+')
        print('|  буква  | частота  |')
        print('+---------+----------+')
        for char, quantity in self.printing_stat:
            statistic_sum += quantity
            print(f'|    {char}    | {quantity:8d} |')
        print('+---------+----------+')
        print(f'|  Итого  | {statistic_sum:8d} |')
        print('+---------+----------+')


chatterer = Chatterer(file_name='voyna-i-mir.txt.zip')
chatterer.collect()
chatterer.sort_statistic(key='alphabet')
chatterer.sort_statistic(key='alphabet', reverse=True)
chatterer.sort_statistic(key='quantity')
chatterer.sort_statistic(key='quantity', reverse=True)
