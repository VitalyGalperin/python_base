# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (900, 600)


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:

    def __init__(self):
        # TODO Лучше использовать несколько переменных, а не список, так код
        #  будет гораздо лучше читаться
        self.snow = [sd.random_number(0, 900), 300 + sd.random_number(0, 600), sd.random_number(3, 20),
                     sd.random_number(1, 10) * 0.1, sd.random_number(1, 50) * 0.01, sd.random_number(1, 90)]

    def clear_previous_picture(self):
        sd.snowflake(center=sd.get_point(self.snow[0], self.snow[1]), length=self.snow[2],
                     factor_a=self.snow[3], factor_b=self.snow[4], factor_c=self.snow[5], color=sd.background_color)

    def move(self):
        if self.snow[1] > 0:
            self.snow[0] = self.snow[0] + sd.random_number(-3, 3)
            self.snow[1] -= 1

    def draw(self):
        sd.snowflake(center=sd.get_point(self.snow[0], self.snow[1]), length=self.snow[2],
                     factor_a=self.snow[3], factor_b=self.snow[4], factor_c=self.snow[5], color=sd.COLOR_WHITE)

    def can_fall(self):
        # TODO Гораздо проще возвращать просто результат сравнения
        if self.snow[1] > 0:
            return True
        else:
            return False


def get_flakes(snow_numbers):
    snows = []
    for i in range(snow_numbers):
        snows.append(Snowflake())
    return snows


def get_fallen_flakes():
    count_fallen_flakes = 0
    for snow in flakes:
        if snow.snow[1] <= 0:
            flakes.remove(snow)
            count_fallen_flakes += 1
    return count_fallen_flakes


def append_flakes(count):
    for _ in range(count):
        flakes.append(Snowflake())


flake = Snowflake()

while True:
    flake.clear_previous_picture()
    flake.move()
    flake.draw()
    if not flake.can_fall():
        break
    # sd.sleep(0.1)
    if sd.user_want_exit():
        break

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:

N = 20
flakes = get_flakes(N)  # создать список снежинок
while True:
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
    if fallen_flakes > 0:
        append_flakes(count=fallen_flakes)  # добавить еще сверху
    # sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
