# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint, sample


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
    cats = []

    def __init__(self):
        self.money = 100
        self.food = 50
        self.cat_food = 50
        self.mud = 0

    # TODO В финальном решении не должно быть ни каких закоментированных строк
    #  кода. Необходимо исправить этот недочет во всем задании
    # def __str__(self):
    #     return 'В доме {} денег, {} еды, {} грязи'.format(self.money, self.food, self.mud)

    def food_incident(self):
        self.food = round(self.food / 2, -1)

    def cat_food_incident(self):
        self.cat_food = round(self.cat_food / 2, -1)

    def money_incident(self):
        self.money = round(self.money / 2, -1)


class Creature:
    eaten_food = 0
    is_live = True

    def __init__(self, name):
        self.name = name
        self.fullness = 30
        self.happiness = 100
        self.house = None

    # def __str__(self):
    #     if self.is_live:
    #         return '{} сытость {}, довольство {}'.format(self.name, self.fullness, self.happiness)
    #     else:
    #         return '{} умер(ла)'

    def eat(self):
        self.fullness += 30
        self.house.food -= 30
        self.eaten_food += 30
        # cprint('{} поел(а)'.format(self.name), color='yellow')

    def go_to_the_house(self, house):
        self.house = house
        # cprint('{} терерь живёт в доме'.format(self.name), color='yellow')


class Human(Creature):
    def __init__(self, name):
        super().__init__(name=name)

    def pet_cat(self):
        if self.house.cats:
            self.happiness += 5
            # cprint('{} гладил(а) кота'.format(self.name), color='yellow')


class Husband(Human):
    salary = 0
    earned_money = 0

    def __init__(self, name):
        super().__init__(name=name)

    def act(self):
        self.house.mud += 5
        dice = randint(1, 6)
        if self.fullness <= 0:
            self.is_live = False
            # cprint('{} умер от голода'.format(self.name), color='red')
            return
        if self.happiness <= 0:
            self.is_live = False
            # cprint('{} умер от депрессии'.format(self.name), color='red')
            return
        if self.fullness <= 20:
            self.eat()
        elif self.house.money <= 350:
            self.work()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.pet_cat()
        else:
            self.gaming()

    def work(self):
        self.fullness -= 10
        self.happiness -= 10
        self.house.money += self.salary
        Husband.earned_money += self.salary
        # cprint('{} поработал'.format(self.name), color='yellow')

    def gaming(self):
        self.fullness -= 10
        self.happiness += 20
        # cprint('{} играл в WoT'.format(self.name), color='yellow')


class Wife(Human):
    bought_fur_coats = 0

    def __init__(self, name):
        super().__init__(name=name)

    def act(self):
        dice = randint(1, 6)
        if self.fullness <= 0:
            self.is_live = False
            # cprint('{} умерла от голода'.format(self.name), color='red')
            return
        if self.happiness <= 0:
            self.is_live = False
            # cprint('{} умерла от депрессии'.format(self.name), color='red')
            return
        if self.fullness <= 20:
            self.eat()
        elif self.happiness <= 10 and self.house.money >= 350:
            self.buy_fur_coat()
        elif self.house.food < 60:
            self.shopping()
        elif self.house.cat_food < 60:
            self.cat_shopping()
        elif self.house.mud >= 90:
            self.clean_house()
        elif dice == 1:
            self.eat()
        elif dice == 2 or dice == 3:
            self.pet_cat()
        else:
            self.watch_TV()

    def shopping(self):
        self.fullness -= 10
        self.happiness -= 10
        if self.house.money >= 60:
            self.house.food += 60
            self.house.money -= 60
        else:
            self.house.food += self.house.money
            self.house.money = 0
        # cprint('{} сходила в магазин за едой'.format(self.name), color='yellow')

    def cat_shopping(self):
        self.happiness -= 10
        if self.house.money >= 60:
            self.house.cat_food += 60
            self.house.money -= 60
        else:
            self.house.cat_food += self.house.money
            self.house.money = 0
        # cprint('{} сходила в магазин за кошачьей едой'.format(self.name), color='yellow')

    def buy_fur_coat(self):
        self.house.money -= 350
        self.fullness -= 10
        self.happiness += 60
        Wife.bought_fur_coats += 1
        # cprint('{} купила шубу'.format(self.name), color='yellow')

    def clean_house(self):
        self.fullness -= 10
        self.happiness -= 10
        if self.house.mud < 100:
            self.house.mud = 0
        else:
            self.house.mud -= 100
        # cprint('{} убралась в доме'.format(self.name), color='yellow')

    def watch_TV(self):
        self.fullness -= 10
        self.happiness += 5
        # cprint('{} смотрела телевизор'.format(self.name), color='yellow')


class Cat(Creature):

    def __init__(self, name):
        super().__init__(name=name)
        self.eaten_cat_food = 0

    def act(self):
        dice = randint(1, 6)
        if self.fullness <= 0:
            self.is_live = False
            # cprint('{} умер от голода'.format(self.name), color='red')
            return
        if self.fullness <= 20:
            self.eat()
        elif dice == 1 or dice == 2 or dice == 3:
            self.sleep()
        elif dice == 4:
            self.eat()
        else:
            self.soil()

    def eat(self):
        self.fullness += 20
        self.house.cat_food -= 10
        self.eaten_cat_food += 10
        # cprint('{} поел(а)'.format(self.name), color='yellow')

    def sleep(self):
        self.fullness -= 10
        # cprint('{} спал'.format(self.name), color='yellow')

    def soil(self):
        self.fullness -= 10
        self.house.mud += 5
        # cprint('{} драл обои'.format(self.name), color='yellow')


class Child(Human):

    def __init__(self, name):
        super().__init__(name=name)

    def act(self):
        if self.fullness <= 0:
            self.is_live = False
            # cprint('{} умер от голода'.format(self.name), color='red')
            return
        if self.fullness <= 5:
            self.eat()
        else:
            self.sleep()

    def eat(self):
        self.fullness += 10
        self.house.food -= 10
        self.eaten_food += 10
        # cprint('{} поел(а)'.format(self.name), color='yellow')

    def sleep(self):
        self.fullness -= 5
        # cprint('{} спал'.format(self.name), color='yellow')


# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайн
# остей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
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


class Simulation:

    def __init__(self, money_incidents=0, food_incidents=0):
        self.money_incidents = money_incidents
        self.food_incidents = food_incidents

    def add_cats(self, home, cat_numbers):
        cat = Cat(name='Кот №{}'.format(cat_numbers))
        home.cats.append(cat)
        cat.go_to_the_house(home)

    def experiment(self, salary):
        home = House()
        serge = Husband(name='Сережа')
        serge.go_to_the_house(home)
        serge.salary = salary
        masha = Wife(name='Маша')
        masha.go_to_the_house(home)
        kolya = Child(name='Коля')
        kolya.go_to_the_house(home)
        Husband.earned_money = 0
        Wife.bought_fur_coats = 0
        food_incident_days = sample(range(365), self.food_incidents)
        money_incident_days = sample(range(365), self.money_incidents)
        for cat_numbers in range(100):
            self.add_cats(home, cat_numbers)
            for day in range(365):
                if day in money_incident_days:
                    home.money_incident()
                if day in food_incident_days:
                    home.food_incident()
                serge.act()
                masha.act()
                kolya.act()
                if not serge.is_live or not masha.is_live or not kolya.is_live:
                    return cat_numbers - 1
                for cat in home.cats:
                    cat.act()
                    if not cat.is_live:
                        return cat_numbers - 1


for food_incidents in range(6):
    for money_incidents in range(6):
        cprint('==================================================', color='blue')
        life = Simulation(money_incidents, food_incidents)
        for salary in range(50, 401, 50):
            cprint('-----------------------------------------------------', color='blue')
            for test_number in range(3):
                max_cats = life.experiment(salary)
                if max_cats == -1:
                    # TODO Необходимо, чтобы длина строки не превышала 80 символов
                    cprint(
                        'Зарплата {}, пропаж еды {}, пропаж денег {}. Тест № {} недостаточно людям'.format(salary,
                                                                                                           food_incidents,
                                                                                                           money_incidents,
                                                                                                           test_number + 1),
                        color='red')
                else:
                    # TODO Необходимо, чтобы длина строки не превышала 80 символов
                    cprint(
                        'Зарплата {}, пропаж еды {}, пропаж денег {}. Тест № {} Максимум котов: {}'.format(salary,
                                                                                                           food_incidents,
                                                                                                           money_incidents,
                                                                                                           test_number + 1,
                                                                                                           max_cats),
                        color='yellow')


#