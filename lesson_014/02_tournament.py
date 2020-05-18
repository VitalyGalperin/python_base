# -*- coding: utf-8 -*-

# Прибежал менеджер и сказал что нужно срочно просчитать протокол турнира по боулингу в файле tournament.txt
#
# Пример записи из лога турнира
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/
#   Татьяна	62334/6/4/44X361/X
#   Давид	--8/--8/4/8/-224----
#   Павел	----15623113-95/7/26
#   Роман	7/428/--4-533/34811/
#   winner is .........
#
# Нужно сформировать выходной файл tournament_result.txt c записями вида
#   ### Tour 1
#   Алексей	35612/----2/8-6/3/4/    98
#   Татьяна	62334/6/4/44X361/X      131
#   Давид	--8/--8/4/8/-224----    68
#   Павел	----15623113-95/7/26    69
#   Роман	7/428/--4-533/34811/    94
#   winner is Татьяна

# Код обаботки файла расположить отдельном модуле, модуль bowling использовать для получения количества очков
# одного участника. Если захочется изменить содержимое модуля bowling - тесты должны помочь.
#
# Из текущего файла сделать консольный скрипт для формирования файла с результатами турнира.
# Параметры скрипта: --input <файл протокола турнира> и --output <файл результатов турнира>
# Усложненное задание (делать по желанию)
#
# После обработки протокола турнира вывести на консоль рейтинг игроков в виде таблицы:
#
# +----------+------------------+--------------+
# | Игрок    |  сыграно матчей  |  всего побед |
# +----------+------------------+--------------+
# | Татьяна  |        99        |      23      |
# ...
# | Алексей  |        20        |       5      |
# +----------+------------------+--------------+
import argparse
from collections import defaultdict, Counter
from bowling import get_score


class TournamentHandler:

    def __init__(self, input_file, output_file, international=True):
        print(international, 'init')
        self.input_file = input_file
        self.output_file = output_file
        self.tour_stat = defaultdict()
        self.tournament_stat = defaultdict(lambda: {'name': set(), 'tours': 0, 'wins': 0, 'fault': 0})
        self.international = international

    def calculate(self):
        with open(self.input_file, mode='r', encoding='utf8') as file:
            with open(self.output_file, mode='w', encoding='utf8') as out_file:
                for line in file:
                    if line[0:9] == '### Tour ':
                        out_file.write(line)
                        continue
                    line = line.rstrip('\n')
                    if line[0:19] == 'winner is .........':
                        tour_max_score = max(self.tour_stat.values())
                        for name, tour_score in self.tour_stat.items():
                            self.tournament_stat[name]['name'] = name
                            self.tournament_stat[name]['tours'] += 1
                            if tour_score == -1:
                                self.tournament_stat[name]['fault'] += 1
                            if tour_score == tour_max_score:
                                winner_name = name
                                self.tournament_stat[name]['wins'] += 1
                        out_file.write(f'{line} {winner_name}\n')
                        self.tour_stat.clear()
                        continue
                    try:
                        name, game_result = line.split('\t')
                    except ValueError:
                        out_file.write(f'{line}\n')
                        continue
                    try:
                        score = get_score(game_result, international=self.international)
                        self.tour_stat[name] = score
                    except Exception as exc:
                        score = exc
                        self.tour_stat[name] = -1
                    out_file.write(f'{name:7} {game_result:20} {score}\n')
        self.rating_print()

    def rating_print(self):
        print('+----------+------------------+----------------------------+')
        print('| Игрок    |  сыграно матчей  |  всего побед |ошибок записи|')
        print('+----------+------------------+----------------------------+')
        sorted_stat = sorted(self.tournament_stat.values(), key=lambda x: x['wins'], reverse=True)
        for stat_row in sorted_stat:
            print(
                f'| {stat_row["name"]:7}  |       {stat_row["tours"]:2}         '
                f'|       {stat_row["wins"]:2}     |      {stat_row["fault"]:2}     |')
        print('+----------+------------------+----------------------------+')


# Для запуска в файле
# tournament = TournamentHandler(input_file='tournament.txt', output_file='tournament_result.txt', international=True)
# tournament.calculate()
# tournament = TournamentHandler(input_file='tournament.txt', output_file='tournament_result.txt', international=False)
# tournament.calculate()


if __name__ == '__main__':
    tournament_calc = argparse.ArgumentParser()
    tournament_calc.add_argument('--input', required=True, help='файл протокола турнира', dest='input_file')
    tournament_calc.add_argument('--output', required=True, help='файл результатов турнира', dest='output_file')
    tournament_calc.add_argument('--international', action='store_true',
                                 help='Использовать междунвродую систему подсчета очков', dest='international')
    args = tournament_calc.parse_args()
    tournament = TournamentHandler(input_file=args.input_file, output_file=args.output_file,
                                   international=args.international)
    tournament.calculate()

# Командная строка Для вызова с терминала (русский подсчкет очков)
# python 02_tournament.py --input tournament.txt --output tournament_result.txt

# Командная строка Для вызова с терминала (междунаорождный подсчкет очков)
# python 02_tournament.py --input tournament.txt --output tournament_result.txt --international
# Зачет