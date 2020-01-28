# -*- coding: utf-8 -*-
from typing import Tuple

import simple_draw as sd

# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg

def triangle(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    v1 = sd.get_vector(start_point=point, angle=angle, length=length)
    v1.draw(color=color)

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 120, length=length)
    v2.draw(color=color)

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 240, length=length)
    v3.draw(color=color)
    v_corr = sd.line(start_point=v3.end_point, end_point=point)


def square(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    v1 = sd.get_vector(start_point=point, angle=angle, length=length)
    v1.draw(color=color)

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 90, length=length)
    v2.draw(color=color)

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 180, length=length)
    v3.draw(color=color)

    v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 270, length=length)
    v4.draw(color=color)

    v_corr = sd.line(start_point=v4.end_point, end_point=point, color=color)


def pentagon(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    v1 = sd.get_vector(start_point=point, angle=angle, length=length)
    v1.draw(color=color)

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 72, length=length)
    v2.draw(color=color)

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 144, length=length)
    v3.draw(color=color)

    v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 216, length=length)
    v4.draw(color=color)

    v5 = sd.get_vector(start_point=v4.end_point, angle=angle + 288, length=length)
    v5.draw(color=color)

    v_corr = sd.line(start_point=v5.end_point, end_point=point, color=color)


def hexagon(point, angle=0, length=200, color=sd.COLOR_YELLOW):
    v1 = sd.get_vector(start_point=point, angle=angle, length=length)
    v1.draw(color=color)

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 60, length=length)
    v2.draw(color=color)

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 120, length=length)
    v3.draw(color=color)

    v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 180, length=length)
    v4.draw(color=color)

    v5 = sd.get_vector(start_point=v4.end_point, angle=angle + 240, length=length)
    v5.draw(color=color)

    v6 = sd.get_vector(start_point=v5.end_point, angle=angle + 300, length=length)
    v6.draw(color=color)

    v_corr = sd.line(start_point=v6.end_point, end_point=point, color=color)

# TODO Лучше назвать функцию select_color
def get_color():
    print('Возможные цвета:')
    print('   0 : red ')
    print('   1 : orange ')
    print('   2 : yellow ')
    print('   3 : green ')
    print('   4 : cyan ')
    print('   5 : blue ')
    print('   6 : purple ')

    while True:
        color_number = input('Введите желаемый цвет: ')

        # TODO Необходимо оптимизировать данное рещение при помощи списков
        if color_number == '0':
            getting_color = sd.COLOR_RED
            return getting_color
        elif color_number == '1':
            getting_color = sd.COLOR_ORANGE
            return getting_color
        elif color_number =='2':
            getting_color = sd.COLOR_YELLOW
            return getting_color
        elif color_number == '3':
            getting_color = sd.COLOR_GREEN
            return getting_color
        elif color_number == '4':
            getting_color = sd.COLOR_CYAN
            return getting_color
        elif color_number == '5':
            getting_color = sd.COLOR_BLUE
            return getting_color
        elif color_number == '6':
            getting_color = sd.COLOR_PURPLE
            return getting_color
        else:
            print('Некорректный ввод')



color = get_color()
point_triangle = sd.get_point(100,100)
point_square = sd.get_point(400, 100)
point_pentagon = sd.get_point(100, 400)
point_hexagon = sd.get_point(400, 350)

triangle(point=point_triangle, angle=30, length=100,color=color)
square(point=point_square, angle=30, length=100,color=color)
pentagon(point=point_pentagon, angle=30, length=100,color=color)
hexagon(point=point_hexagon, angle=30, length=100,color=color)

sd.pause()
