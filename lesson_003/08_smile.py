# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd

import random


# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.

def smile(X, Y):
    sd.ellipse(left_bottom=sd.get_point(X - 40, Y - 45), right_top=sd.get_point(X + 40, Y + 45),
               color=sd.random_color())
    face_color = sd.random_color()
    sd.ellipse(left_bottom=sd.get_point(X + 10, Y + 8), right_top=sd.get_point(X + 30, Y + 20),
               color=face_color, width=2)
    sd.ellipse(left_bottom=sd.get_point(X - 27, Y + 8), right_top=sd.get_point(X - 7, Y + 20),
               color=face_color, width=2)
    sd.circle(sd.get_point(X + 18, Y + 14), radius=2, color=face_color)
    sd.circle(sd.get_point(X - 19, Y + 14), radius=2, color=face_color)
    sd.line(start_point=sd.get_point(X, Y - 8), end_point=sd.get_point(X, Y + 13), color=face_color, width=4)
    sd.line(start_point=sd.get_point(X - 4, Y - 8), end_point=sd.get_point(X + 5, Y - 8), color=face_color, width=4)
    sd.line(start_point=sd.get_point(X - 10, Y - 18), end_point=sd.get_point(X + 11, Y - 18), color=face_color, width=4)
    sd.line(start_point=sd.get_point(X + 11, Y - 18), end_point=sd.get_point(X + 16, Y - 15), color=face_color, width=4)
    sd.line(start_point=sd.get_point(X - 10, Y - 18), end_point=sd.get_point(X - 15, Y - 15), color=face_color, width=4)


sd.background_color = sd.random_color()
for _ in range(10):
    smile(X=random.randint(40, 560), Y=random.randint(45, 555))

sd.pause()
