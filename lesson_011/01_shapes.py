# -*- coding: utf-8 -*-

import simple_draw as sd

# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    def figure_drawing(point=sd.get_point(200, 200), angle=13, length=100):
        current_point = point
        for i in range(n):
            vector = sd.get_vector(start_point=current_point, angle=angle + 360 / n * i, length=length)
            vector.draw()
            current_point =vector.end_point
        sd.line(start_point=point, end_point=current_point)
    return figure_drawing


draw_triangle = get_polygon(n=3)
draw_triangle(point=sd.get_point(200, 200), angle=13, length=100)

sd.pause()
