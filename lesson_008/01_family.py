# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint

######################################################## Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умрает от депресии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:

    def __init__(self):
        self.money = 100
        self.food = 50
        self.mud = 0

    def __str__(self):
        return 'В доме {} денег, {} еды, {} грязи'.format(self.money, self.food, self.mud)


class Husband:
    # TODO Эти атрибуты в целом относятся ко всем людям, по этому их нужно
    #  вынести в базовый класс (человек). Кроме этого в базовый класс нужно
    #  вынести все общие для всех людей методы (реализация которых одинакова и
    #  у мужа и у жены, один из примеров это метод __str__).
    eaten_food = 0
    earned_money = 0

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None

    def __str__(self):
        return '{} сытость {}, довольство {}'.format(self.name, self.fullness, self.happiness)
        # return super().__str__()

    def go_to_the_house(self,house):
        self.house = house
        cprint('{} поселился в доме'.format(self.name), color='yellow')

    def act(self):
        self.house.mud += 5
        dice = randint(1, 6)
        if self.fullness <= 0:
            cprint('{} умер от голода'.format(self.name), color='red')
            return
        if self.happiness <= 0:
            cprint('{} умер от депрессии'.format(self.name), color='red')
            return
        if self.fullness <= 20:
            self.eat()
        elif self.house.money <= 350:
            self.work()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        else:
            self.gaming()

    def eat(self):
        self.fullness += 30
        self.house.food -= 30
        Husband.eaten_food += 30
        cprint('{} поел'.format(self.name), color='yellow')

    def work(self):
        self.fullness -= 10
        self.happiness -= 10
        self.house.money += 150
        Husband.earned_money += 150
        cprint('{} поработал'.format(self.name), color='yellow')

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        cprint('{} играл в WoT'.format(self.name), color='yellow')


class Wife:
    # TODO Эти атрибуты в целом относятся ко всем людям, по этому их нужно
    #  вынести в базовый класс (человек)
    eaten_food = 0
    bought_fur_coats = 0
 
    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.fur_coats = 0
        self.house = None

    def __str__(self):
        return '{} сытость {}, довольство {}'.format(self.name, self.fullness, self.happiness)
        # return super().__str__()

    def go_to_the_house(self,house):
        self.house = house
        cprint('{} поселилась в доме'.format(self.name), color='yellow')

    def act(self):
        dice = randint(1, 6)
        if self.fullness <= 0:
            cprint('{} умерла от голода'.format(self.name), color='red')
            return
        if self.happiness <= 0:
            cprint('{} умерла от депрессии'.format(self.name), color='red')
            return
        if self.fullness <= 20:
            self.eat()
        elif self.happiness <= 10 and self.house.money >= 350:
            self.buy_fur_coat()
        elif self.house.food < 60:
            self.shopping()
        elif self.house.mud >= 90:
            self.clean_house()
        elif dice == 1:
            self.clean_house()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.shopping()
        else:
            self.watch_TV()

    def eat(self):
        self.fullness += 30
        self.house.food -= 30
        Wife.eaten_food += 30
        cprint('{} поела'.format(self.name), color='yellow')

    def shopping(self):
        self.fullness -= 10
        self.house.food += 60
        self.house.money -= 60
        cprint('{} сходила в магазин'.format(self.name), color='yellow')

    def buy_fur_coat(self):
        self.house.money -= 350
        self.fullness -= 10
        self.happiness += 60
        Wife.bought_fur_coats += 1
        cprint('{} купила шубу'.format(self.name), color='yellow')

    def clean_house(self):
        self.fullness -= 10
        self.happiness -= 10
        if self.house.mud < 100:
            self.house.mud = 0
        else:
            self.house.mud -= 100
        cprint('{} убралась в доме'.format(self.name), color='yellow')

    def watch_TV(self):
        self.fullness -= 10
        cprint('{} смотрела телевизор'.format(self.name), color='yellow')


home = House()
serge = Husband(name='Сережа')
serge.go_to_the_house(home)
masha = Wife(name='Маша')
masha.go_to_the_house(home)

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(home, color='cyan')

cprint('================== Прошел год ==================', color='blue')
cprint('Заработано денег {}'.format(Husband.earned_money), color='blue')
cprint('Съедено еды {}'.format(Husband.eaten_food + Wife.eaten_food), color='blue')
cprint('Куплено шуб {}'.format(Wife.bought_fur_coats), color='blue')


######################################################## Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов

#
# class Cat:
#
#     def __init__(self):
#         pass
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#     def soil(self):
#         pass


######################################################## Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)
#
# class Child:
#
#     def __init__(self):
#         pass
#
#     def __str__(self):
#         return super().__str__()
#
#     def act(self):
#         pass
#
#     def eat(self):
#         pass
#
#     def sleep(self):
#         pass
#
#
# # TODO после реализации второй части - отдать на проверку учителем две ветки
#

######################################################## Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.

#
# home = House()
# serge = Husband(name='Сережа')
# masha = Wife(name='Маша')
# kolya = Child(name='Коля')
# murzik = Cat(name='Мурзик')
#
# for day in range(365):
#     cprint('================== День {} =================='.format(day), color='red')
#     serge.act()
#     masha.act()
#     kolya.act()
#     murzik.act()
#     cprint(serge, color='cyan')
#     cprint(masha, color='cyan')
#     cprint(kolya, color='cyan')
#     cprint(murzik, color='cyan')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

