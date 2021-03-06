# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...
#
# если изначально не писать число в виде строки - теряется точность!

from decimal import *
from datetime import datetime
import json
import csv


class LabyrinthGame:
    def __init__(self, file_name, remaining_time):
        self.game_time = self.remaining_time = Decimal(remaining_time)
        self.file_name = file_name
        self.log = [['current_location', 'current_experience', 'current_date']]
        self.experience = 0
        self.rpg = self.level = self.current_level = self.level_name = None
        self.level_monsters = []
        self.level_exits = []
        self.level_time = Decimal()
        self.last_step = False

    def process_file(self, file_name):
        with open(file_name, "r") as read_file:
            self.rpg = json.load(read_file)

    def run(self):
        self.process_file(self.file_name)
        while True:
            self.get_level()
            if self.last_step:
                if self.experience >= 280:
                    self.log_write()
                    self.win_message()
                    break
                else:
                    self.exit_deadlock_message()
                    self.get_level()
            if self.current_level != self.level:
                self.level_state()
            self.action_choice()
            get_number = input()
            if get_number.isdigit() and int(get_number) == 1:
                monster = self.get_monster()
                self.attack_monster(monster)
            elif get_number.isdigit() and int(get_number) == 2:
                self.level_name = self.change_location()
            elif get_number.isdigit() and int(get_number) == 3:
                self.log_write()
                self.escape_message()
                break
            else:
                print('Эээ.... Не понимаю что делать. Попробуй ещё раз...')

    def action_choice(self):
        print(".................")
        print("Выберите действие:")
        if len(self.level_monsters) >= 1:
            print("    1.Атаковать монстра")
        print("    2.Перейти в другую локацию")
        print("    3.Сдаться и выйти из игры")

    def get_monster(self):
        while True:
            if len(self.level_monsters) < 1:
                print('Некого атаковать! На уровне не осталоссь монстров!')
                return None
            elif len(self.level_monsters) == 1:
                return self.level_monsters[0]
            else:
                print('Выберите какого монстра будем атоковать:')
                for number, monster_name in enumerate(self.level_monsters):
                    print(number + 1, ': ', monster_name)
                monster_number = input()
                try:
                    monster = self.level_monsters[int(monster_number) - 1]
                    return monster
                except IndexError:
                    print('Такого монстра на уровне нет, выберите ещё раз!')
                except ValueError:
                    print('Такого монстра на уровне нет, выберите ещё раз!')

    def attack_monster(self, monster):
        if not monster:
            return None
        print('Вы выбрали сражаться с монстром!')
        name, experience_plus, battle_time = monster.split('_')
        battle_time = Decimal(battle_time[2:])
        self.game_time -= battle_time
        self.experience += int(experience_plus[3:])
        self.level_monsters.remove(monster)
        print(f'Монстр {monster} повержен! Вы получили {experience_plus[3:]} опыта')
        print(f'Теперь у вас {self.experience} опыта! Времени осталось {self.game_time} секунд')
        self.add_log_line()
        if self.game_time <= 0:
            self.death_message()

    def change_location(self):
        if len(self.level_exits) < 1:
            self.deadlock_message()
            return None
        elif len(self.level_exits) == 1:
            return self.level_exits[0]
        else:
            while True:
                print('На какой уровень переходим?:')
                for number, level_name in enumerate(self.level_exits):
                    print(number + 1, ': ', level_name)
                choice_number = input()
                try:
                    level = self.level_exits[int(choice_number) - 1]
                    return level
                except ValueError:
                    print('Неверный номер уровня, попробуйте ещё раз!!!')
                except IndexError:
                    print('Неверный номер уровня, попробуйте ещё раз!!!')

    def get_level(self):
        if not self.level_name:
            for key, item in self.rpg.items():
                self.level_name, self.level = key, item
            self.welcome_message()
        else:
            for index, object in enumerate(self.level):
                if isinstance(object, dict) and list(object.keys())[0] == self.level_name:
                    for key, item in object.items():
                        self.level_name, self.level = key, item
        if self.level_name[:5] == 'Hatch':
            string, self.level_time = self.level_name.split('_')
            self.last_step = True
        else:
            string, level_number, self.level_time = self.level_name.split('_')
        self.level_time = Decimal(self.level_time[2:])

    def level_state(self):
        self.init_level()
        for string, object in enumerate(self.level):
            if isinstance(object, str):
                print('Монстра:', object)
                self.level_monsters.append(object)
            elif isinstance(object, dict):
                print('Вход в локацию: ', (list(object)[0]))
                self.level_exits.append(list(object)[0])

    def init_level(self):
        self.level_monsters.clear()
        self.level_exits.clear()
        self.current_level = self.level
        self.game_time -= self.level_time
        print(f'Вы находитесь в {self.level_name}')
        print(f'У вас {self.experience} опыта и осталось {self.game_time} секунд до наводнения')
        print("=================")
        print("Внутри вы видите:")
        self.add_log_line()

    def welcome_message(self):
        print("=======================================")
        print("|    Добро пожаловать в Лабиринт !!!  |")
        print("=======================================")

    def win_message(self):
        print("=======================================")
        print("|           Поздравляю!!!!!           |")
        print("|     Вы вырвались из Лабиринта!!!!   |")
        print("|        Вперёд, к Принцессе!!!!      |")
        print("=======================================")

    def exit_deadlock_message(self):
        print('Вот и Выход, вы навалились всем телом,но дверь не поддаётся...')
        print('Вы не сражались с монстрами и теперь у вас не хватает опыта чтобы открыть Выход')
        print('Вы оборачиваетесь...')
        self.deadlock_message()

    def deadlock_message(self):
        print('Дверь захлопнулась за вами. Вокруг каменные стены...')
        print('Вы не умрете с голода... Наводнение убъёт вас раньше...')
        print('Его ждать недолго...')
        self.death_message()

    def death_message(self):
        print('Вода захлестывает вас, нечем дышать.....')
        print('Но что это?!  Вы воскресли... Не зря матушка дала вам оберег :)')
        print('Но оберег не может вывести из Круга ....')
        print('Вы открываете глаза, за вами стена, а перед вами снова надпись:....')
        self.new_try()

    def escape_message(self):
        print('Ну что же... Вы вспомнили про подарок Домовихи..')
        print('Заговорённая скалка открыла портал к родному дому.')
        print('Монстры так и остались в пещере, да и к Принцессе теперь не вернёшься.....')
        print('Зато живой и дома.... Вот и Домовиха бежит навстречу.... ')
        print('Не Принцесса, конечно......Хотя........')

    def new_try(self):
        self.game_time = self.remaining_time
        self.experience = 0
        self.level_name = None
        self.last_step = False

    def add_log_line(self):
        now = datetime.now()
        self.log.append([self.level_name, self.experience, now.strftime("%d.%m.%Y %H:%M")])

    def log_write(self):
        with open('dungeon.csv', 'w', newline='') as result_file:
            writer = csv.writer(result_file, delimiter=';')
            for row in self.log:
                writer.writerow(row)


game = LabyrinthGame(file_name='rpg.json', remaining_time='123456.0987654321')
game.run()
#зачет!