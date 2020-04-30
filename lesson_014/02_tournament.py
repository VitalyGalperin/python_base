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

from collections import defaultdict, Counter
from bowling import get_score


class TournamentHandler:

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.tour_stat = defaultdict()
        self.tournament_stat = defaultdict()

    def calculate(self):
        with open(self.input_file, mode='r', encoding='utf8') as file:
            with open(self.output_file, mode='w', encoding='utf8') as out_file:
                for line in file:
                    if line[0:9] == '### Tour ':
                        tour_number = int(line[9:])
                        out_file.write(line)
                        continue
                    line = line.rstrip('\n')
                    if line[0:19] == 'winner is .........':
                        tour_max_score = max(self.tour_stat.values())
                        for key, value in self.tour_stat.items():
                            if value == tour_max_score:
                                winner_name = key
                        out_file.write(f'{line} {winner_name}\n')
                        self.tournament_stat[tour_number] = self.tour_stat
                        self.tour_stat.clear()
                        continue
                    try:
                        name, game_result = line.split('\t')
                    except ValueError:
                        out_file.write(f'{line}\n')
                        continue
                    try:
                        score = get_score(game_result)
                        self.tour_stat[name] = score
                    except Exception as exc:
                        score = exc
                        self.tour_stat[name] = -1
                    out_file.write(f'{name:7} {game_result:20} {score}\n')
                    # self.stat[name] += score
        a = 1


tournament = TournamentHandler(input_file='tournament.txt', output_file='tournament_result.txt')
tournament.calculate()

# parser = argparse.ArgumentParser()
# parser.add_argument('--result', required=True, help='Строка с результатом игры', dest='game_result')
# args = parser.parse_args()
# try:
#     print("Результат игры:", get_score(args.game_result))
# except Exception as exc:
#     print("Неверные входные данные")
#     print(exc)
