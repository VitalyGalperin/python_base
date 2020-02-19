# -*- coding: utf-8 -*-

from random import randint, choice

from termcolor import cprint


# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)

# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня

# Человеку и коту надо вместе прожить 365 дней.


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None
        self.cat = []

    def __str__(self):
        return 'Я - {}, сытость {}'.format(
            self.name, self.fullness)

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} въехала в дом'.format(self.name), color='cyan')

    def eat(self):
        if self.house.food >= 20:
            cprint('{} поела'.format(self.name), color='yellow')
            self.fullness += 20
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')

    def work(self):
        cprint('{} сходила на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_lets_get_married(self):
        cprint('{} смотрела Давай Поженимся целый день'.format(self.name), color='green')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходила в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
            self.fullness -= 10
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def cat_shopping(self):
        if self.house.money >= 50:
            cprint('{} сходила в магазин за кошачьей едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.cat_food += 50
            self.fullness -= 10
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def cleaning(self):
        cprint('{} убиралась в доме'.format(self.name), color='green')
        self.fullness -= 20
        self.house.dirt -= 100

    def get_cat(self):
        self.cat = Cat()
        self.fullness -= 10
        self.cat.house = my_sweet_home
        cprint('{} взял в дом кота'.format(self.name), color='cyan')
        return self.cat

    def act(self):
        dice = randint(1, 6)
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        if self.fullness < 20:
            self.eat()
        elif self.house.money < 50:
            self.work()
        elif self.house.food < 30:
            self.shopping()
        elif self.house.cat_food < 30:
            self.cat_shopping()
        elif self.house.dirt >= 100 and self.fullness > 20:
            self.cleaning()
        elif self.house.money > 500:
            self.get_cat()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.watch_lets_get_married()


class House:

    def __init__(self):
        self.food = 50
        self.money = 0
        self.dirt = 0
        self.cat_food = 0

    def __str__(self):
        return 'В доме еды осталось {}, кошачьей еды осталось {}, денег осталось {}, грязь {}'.format(
            self.food, self.cat_food, self.money, self.dirt)


class Cat:
    names = ['Васька', 'Мурзик', 'Черныш', 'Аполлон', 'Рыжик', 'Миша', 'Белёк', 'Антон Палыч', 'Пушкин', 'Иди сюда',
             'Иди отсюда', 'Бегемот', 'Костик', 'Хот Дог', 'Пельмень', 'Просто кот', 'Дашка']

    def __init__(self):

        self.name = choice(Cat.names)
        self.fullness = 20
        self.house = None

    def __str__(self):
        return 'Кот - {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.cat_food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 20
            self.house.cat_food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')

    def sleep(self):
        cprint('{} спал'.format(self.name), color='magenta')
        self.fullness -= 10

    def tear_wallpaper(self):
        cprint('{} драл обои'.format(self.name), color='blue')
        self.fullness -= 10
        self.house.dirt += 5

    def act(self):
        dice = randint(1, 6)
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        if self.fullness < 20:
            self.eat()
        elif dice == 1:
            self.sleep()
        elif dice == 2:
            self.tear_wallpaper()
        else:
            self.sleep()

person = Man(name='Ирина Марковна')

my_sweet_home = House()
person.go_to_the_house(house=my_sweet_home)
cats = person.get_cat()

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    print(person)
    person.act()
    print(cats)
    cats.act()
    print('--- в конце дня ---')
    print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)
