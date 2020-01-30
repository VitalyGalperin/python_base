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
# Результат решения см lesson_004/results/exercise_02_global_color.jpg)

def figure_drawing(point, angle=0, length=200, corner_numbers=3, color_drawing=sd.COLOR_YELLOW):
    angle_coordinates = [point]
    for i in range(corner_numbers):
        vector = sd.get_vector(start_point=angle_coordinates[i], angle=angle + 360 / corner_numbers * i, length=length)
        vector.draw(color=color_drawing)
        angle_coordinates.append(vector.end_point)
    sd.line(start_point=point, end_point=angle_coordinates[corner_numbers], color=color_drawing)


def triangle(point, angle=0, length=200, figure_color=sd.COLOR_YELLOW):
    figure_drawing(point, angle, length, corner_numbers=3, color_drawing=figure_color)


def square(point, angle=0, length=200, figure_color=sd.COLOR_YELLOW):
    figure_drawing(point, angle, length, corner_numbers=4, color_drawing=figure_color)


def pentagon(point, angle=0, length=200, figure_color=sd.COLOR_YELLOW):
    figure_drawing(point, angle, length, corner_numbers=5, color_drawing=figure_color)


def hexagon(point, angle=0, length=200, figure_color=sd.COLOR_YELLOW):
    figure_drawing(point, angle, length, corner_numbers=6, color_drawing=figure_color)


def select_color():
    colors_list = [sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN, sd.COLOR_CYAN, sd.COLOR_BLUE,
                   sd.COLOR_PURPLE]
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
        if color_number.isdigit() and 0 <= int(color_number) <= 6:
            return colors_list[int(color_number)]
        else:
            print('Некорректный ввод')


color = select_color()
point_triangle = sd.get_point(100, 100)
point_square = sd.get_point(400, 100)
point_pentagon = sd.get_point(100, 400)
point_hexagon = sd.get_point(400, 350)

triangle(point=point_triangle, angle=30, length=100, figure_color=color)
square(point=point_square, angle=30, length=100, figure_color=color)
pentagon(point=point_pentagon, angle=30, length=100, figure_color=color)
hexagon(point=point_hexagon, angle=30, length=100, figure_color=color)

sd.pause()

# Зачет
