# -*- coding: utf-8 -*-

import simple_draw as sd
from my_draw import tree
from my_draw import rainbow
from my_draw import house
from my_draw import snowfall
from my_draw import smile
from my_draw import sun
from my_draw import cat

sd.resolution = (1200, 600)

# Создать пакет, в который скопировать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Функции по модулям разместить по тематике. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)

sd.start_drawing()
rainbow_center = sd.get_point(1100, -100)
rainbow_radius = 650
rainbow_width = 10
rainbow.draw_raindow(center=rainbow_center, radius=rainbow_radius, width=rainbow_width)
root_point = sd.get_point(900, 30)
zero_point = sd.get_point(0, 0)
horizon_point = sd.get_point(1200, 200)
sd.rectangle(zero_point, horizon_point, color=sd.background_color, width=0)
sd.rectangle(sd.get_point(0, 0), sd.get_point(250, 20), color=sd.COLOR_WHITE, width=0)
house_left = 350
house_bottom = 25
house_right = 700
house_top = 250
house.draw_house(house_left=house_left, house_bottom=house_bottom, house_right=house_right, house_top=house_top)
random_tree = True
summer_tree = False
cat.cat(x=600, y=80)
tree.draw_branches(start_point=root_point, angle=90, length=90, is_random=random_tree, is_summer_tree=summer_tree)
root_point = sd.get_point(1100, 30)
tree.draw_branches(start_point=root_point, angle=90, length=50, is_random=random_tree, is_summer_tree=summer_tree)
sd.finish_drawing()

snowfall_left = 0
snowfall_right = 250
# snowfall.create_snow(snow_number=20, snows=snows, snowfall_left=snowfall_left, snowfall_right=snowfall_right)
snows = snowfall.start_snowfall(snow_number=20, snowfall_left=0, snowfall_right=250)

for count in range(10000):
    snowfall.snowfall(snows=snows)
    sd.circle(center_position=sd.get_point(50, 0), radius=60, color=sd.COLOR_WHITE, width=0)
    sd.circle(center_position=sd.get_point(140, 0), radius=70, color=sd.COLOR_WHITE, width=0)
    sd.circle(center_position=sd.get_point(230, 0), radius=40, color=sd.COLOR_WHITE, width=0)
    galo_count = str(count)
    galo_count = galo_count[-1][0]
    galo_count = int(galo_count)

    if count / 10 == int(count / 10):
        smile.smile(x=450, y=150, blink=True)
    else:
        smile.smile(x=450, y=150, blink=False)
    if count / 10 + 2 == int(count / 10) + 2:
        sun.sun(x=500, y=500, blink=True, galo_count=galo_count)
    else:
        sun.sun(x=500, y=500, blink=False, galo_count=galo_count)

sd.pause()

# Усложненное задание (делать по желанию)
# Анимировать картину.
# Пусть слева идет снегопад, радуга переливается цветами, смайлик моргает, солнце крутит лучами, етс.
# Задержку в анимировании все равно надо ставить, пусть даже 0.01 сек - так библиотека устойчивей работает.
