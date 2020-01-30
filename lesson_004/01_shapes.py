# -*- coding: utf-8 -*-

import simple_draw as sd

# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg


def figure_drawing(point, angle=0, length=200, corner_numbers=3):
    # TODO В один момент времени реально нужно использовать только 1 значение
    #  из списка, по этому необходимо оптимизироватьрешение и отказаться от
    #  списка (хранить нужно просто 1 точку).
    angle_coordinates = [point]
    for i in range(corner_numbers):
        vector = sd.get_vector(start_point=angle_coordinates[i], angle=angle + 360 / corner_numbers * i, length=length)
        vector.draw()
        angle_coordinates.append(vector.end_point)
    sd.line(start_point=point, end_point=angle_coordinates[corner_numbers])


def triangle(point, angle=0, length=200):
    figure_drawing(point, angle, length, corner_numbers=3)


def square(point, angle=0, length=200):
    figure_drawing(point, angle, length, corner_numbers=4)


def pentagon(point, angle=0, length=200):
    figure_drawing(point, angle, length, corner_numbers=5)


def hexagon(point, angle=0, length=200):
    figure_drawing(point, angle, length, corner_numbers=6)


point_triangle = sd.get_point(100, 100)
point_square = sd.get_point(400, 100)
point_pentagon = sd.get_point(100, 400)
point_hexagon = sd.get_point(400, 350)

triangle(point=point_triangle, angle=30, length=100)
square(point=point_square, angle=30, length=100)
pentagon(point=point_pentagon, angle=30, length=100)
hexagon(point=point_hexagon, angle=30, length=100)

sd.pause()



# def triangle(point, angle=0, length=200):
#     v1 = sd.get_vector(start_point=point, angle=angle, length=length)
#     v1.draw()
#
#     v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 120, length=length)
#     v2.draw()
#
#     v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 240, length=length)
#     v3.draw()
#     sd.line(start_point=v3.end_point, end_point=point)
#
#
# def square(point, angle=0, length=200):
#     v1 = sd.get_vector(start_point=point, angle=angle, length=length)
#     v1.draw()
#
#     v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 90, length=length)
#     v2.draw()
#
#     v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 180, length=length)
#     v3.draw()
#
#     v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 270, length=length)
#     v4.draw()
#
#     sd.line(start_point=v4.end_point, end_point=point)
#
#
# def pentagon(point, angle=0, length=200):
#     v1 = sd.get_vector(start_point=point, angle=angle, length=length)
#     v1.draw()
#
#     v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 72, length=length)
#     v2.draw()
#
#     v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 144, length=length)
#     v3.draw()
#
#     v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 216, length=length)
#     v4.draw()
#
#     v5 = sd.get_vector(start_point=v4.end_point, angle=angle + 288, length=length)
#     v5.draw()
#
#     sd.line(start_point=v5.end_point, end_point=point)
#
#
# def hexagon(point, angle=0, length=200):
#     v1 = sd.get_vector(start_point=point, angle=angle, length=length)
#     v1.draw()
#
#     v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 60, length=length)
#     v2.draw()
#
#     v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 120, length=length)
#     v3.draw()
#
#     v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 180, length=length)
#     v4.draw()
#
#     v5 = sd.get_vector(start_point=v4.end_point, angle=angle + 240, length=length)
#     v5.draw()
#
#     v6 = sd.get_vector(start_point=v5.end_point, angle=angle + 300, length=length)
#     v6.draw()
#
#     sd.line(start_point=v6.end_point, end_point=point)


# Первая часть зачтена

# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44? Код писать не нужно, просто представь объем работы... и запомни это.

# Часть 2 (делается после зачета первой части)
#
# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв
#   в начальной/конечной точках рисуемой фигуры (если он есть)

# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9
# Будьте ленивыми, не используйте копи-пасту!


sd.pause()
