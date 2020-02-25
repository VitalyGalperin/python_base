# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (900, 600)


# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:

    def __init__(self):
        self.x_coordinate = sd.random_number(0, 900)
        self.y_coordinate = 300 + sd.random_number(0, 600)
        self.length = sd.random_number(3, 20)
        self.place_of_rays = sd.random_number(1, 10) * 0.1
        self.ray_length = sd.random_number(1, 50) * 0.01
        self.deflection_angle = sd.random_number(1, 90)

    def clear_previous_picture(self):
        sd.snowflake(center=sd.get_point(self.x_coordinate, self.y_coordinate), length=self.length,
                     factor_a=self.place_of_rays, factor_b=self.ray_length, factor_c=self.deflection_angle,
                     color=sd.background_color)

    def move(self):
        if self.y_coordinate > 0:
            self.x_coordinate += sd.random_number(-3, 3)
            self.y_coordinate -= 1

    def draw(self):
        sd.snowflake(center=sd.get_point(self.x_coordinate, self.y_coordinate), length=self.length,
                     factor_a=self.place_of_rays, factor_b=self.ray_length, factor_c=self.deflection_angle,
                     color=sd.COLOR_WHITE)

    def can_fall(self):
        return self.y_coordinate


def get_flakes(snow_numbers):
    snows = []
    for i in range(snow_numbers):
        snows.append(Snowflake())
    return snows


def get_fallen_flakes(flakes):
    count_fallen_flakes = 0
    for snow in flakes:
        if snow.y_coordinate <= 0:
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
    fallen_flakes = get_fallen_flakes(flakes)  # подчитать сколько снежинок уже упало
    if fallen_flakes > 0:
        append_flakes(count=fallen_flakes)  # добавить еще сверху
    # sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# Зачет
