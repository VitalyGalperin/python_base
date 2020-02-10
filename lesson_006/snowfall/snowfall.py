# -*- coding: utf-8 -*-

import simple_draw as sd


# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
def create_snows(snows, snow_numbers=20):
    for i in range(snow_numbers):
        snow = []
        snow.append(sd.random_number(0, 900))
        snow.append(300 + sd.random_number(0, 600))
        snow.append(sd.random_number(3, 20))
        snow.append(sd.random_number(1, 10) * 0.1)
        snow.append(sd.random_number(1, 50) * 0.01)
        snow.append(sd.random_number(1, 90))
        snows.append(snow)
    return snows


def draw_snows(snows, color=sd.COLOR_WHITE):
    for i, snows_item in enumerate(snows, 0):
        sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2],
                     factor_a=snows[i][3], factor_b=snows[i][4], factor_c=snows[i][5], color=color)


def move_snows(snows):
    for i, snows_item in enumerate(snows, 0):
        if snows[i][1] > 0:
            snows[i][0] = snows[i][0] + sd.random_number(-3, 3)
            snows[i][1] -= 1


def fallen_snows(snows):
    numbers_of_fallen_snows =[]
    for i, snows_item in enumerate(snows, 0):
        if snows[i][1] <= 0:
            numbers_of_fallen_snows.append(i)
    return numbers_of_fallen_snows


def delete_snows(snows, numbers_of_fallen_snows):
    for i in numbers_of_fallen_snows:
        snows.pop(i)
