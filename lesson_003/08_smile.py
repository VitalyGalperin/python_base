# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd

import random


# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.

def smile(x, y):
    sd.ellipse(left_bottom=sd.get_point(x - 40, y - 45), right_top=sd.get_point(x + 40, y + 45),
               color=sd.random_color())
    face_color = sd.random_color()
    sd.ellipse(left_bottom=sd.get_point(x + 10, y + 8), right_top=sd.get_point(x + 30, y + 20),
               color=face_color, width=2)
    sd.ellipse(left_bottom=sd.get_point(x - 27, y + 8), right_top=sd.get_point(x - 7, y + 20),
               color=face_color, width=2)
    sd.circle(sd.get_point(x + 18, y + 14), radius=2, color=face_color)
    sd.circle(sd.get_point(x - 19, y + 14), radius=2, color=face_color)
    sd.line(start_point=sd.get_point(x, y - 8), end_point=sd.get_point(x, y + 13), color=face_color, width=4)
    sd.line(start_point=sd.get_point(x - 4, y - 8), end_point=sd.get_point(x + 5, y - 8), color=face_color, width=4)
    sd.line(start_point=sd.get_point(x - 10, y - 18), end_point=sd.get_point(x + 11, y - 18), color=face_color, width=4)
    sd.line(start_point=sd.get_point(x + 11, y - 18), end_point=sd.get_point(x + 16, y - 15), color=face_color, width=4)
    sd.line(start_point=sd.get_point(x - 10, y - 18), end_point=sd.get_point(x - 15, y - 15), color=face_color, width=4)


sd.background_color = sd.random_color()
for _ in range(10):
    smile(x=random.randint(40, 560), y=random.randint(45, 555))

sd.pause()

# Зачет
