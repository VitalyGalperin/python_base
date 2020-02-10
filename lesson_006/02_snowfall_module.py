# -*- coding: utf-8 -*-

import simple_draw as sd
from snowfall import create_snows, draw_snows, move_snows, fallen_snows, delete_snows

sd.resolution = (900, 600)
# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

# # создать_снежинки(N)
# while True:
#     #  нарисовать_снежинки_цветом(color=sd.background_color)
#     #  сдвинуть_снежинки()
#     #  нарисовать_снежинки_цветом(color)
#     #  если есть номера_достигших_низа_экрана() то
#     #       удалить_снежинки(номера)
#     #       создать_снежинки(count)
#     sd.sleep(0.1)
#     if sd.user_want_exit():
#         break

N = 20
snows = []
create_snows(snows, snow_numbers=N)
while True:
    sd.start_drawing()
    draw_snows(snows, color=sd.background_color)
    move_snows(snows)
    draw_snows(snows, color=sd.COLOR_WHITE)
    numbers_of_fallen_snows = fallen_snows(snows)
    delete_snows(snows, numbers_of_fallen_snows)
    create_snows(snows, len(numbers_of_fallen_snows))
    sd.finish_drawing()
    # sd.sleep(0.1)
    if sd.user_want_exit():
        break
sd.pause()
