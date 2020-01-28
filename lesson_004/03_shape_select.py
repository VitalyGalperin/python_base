# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (600, 600)


# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg


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


# TODO В данном случае нет необхожимости в функции
def get_shape(point):
    print('Возможные фигуры:')
    print('   0 : треугольник ')
    print('   1 : квадрат ')
    print('   2 : пятиугольник ')
    print('   3 : шестиугольник ')

    while True:
        shape = input('Введите желаемую фигуру: ')
        if shape == '0':
            triangle(point=point, angle=30, length=160)
            return shape
        elif shape == '1':
            square(point=point, angle=30, length=130)
            return shape
        elif shape == '2':
            pentagon(point=point, angle=30, length=110)
            return shape
        elif shape == '3':
            hexagon(point=point, angle=30, length=90)
            return shape
        else:
            print('Некорректный ввод')


start_point = sd.get_point(300, 220)
shape = get_shape(point=start_point)

sd.pause()
