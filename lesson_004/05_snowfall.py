# -*- coding: utf-8 -*-

import simple_draw as sd
from pprint import pprint

sd.resolution = (1200, 600)


# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()


def create_snow(snow_number=None):
    snow = []
    snow.append(sd.random_number(0, 1200))
    snow.append(600 + sd.random_number(0, 600))
    snow.append(sd.random_number(10, 100))
    snow.append(sd.random_number(1, 10) * 0.1)
    snow.append(sd.random_number(1, 100) * 0.01)
    snow.append(sd.random_number(1, 90))
    if snow_number is None:
        snows.append(snow)
    else:
        snows.insert(snow_number, snow)

N = 20
snows = []
snowdrift = []

for _ in range(N):
    create_snow()

while True:
    for i in range(len(snows)):
        sd.start_drawing()
        for j in range(len(snowdrift)):
            sd.snowflake(center=sd.get_point(snowdrift[j][0], snowdrift[j][1]), length=snowdrift[j][2],
                         factor_a=snowdrift[j][3], factor_b=snowdrift[j][4], factor_c=snowdrift[j][5])
        sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                     factor_b=snows[i][4], factor_c=snows[i][5], color=sd.background_color)
        if snows[i][1] > 0:
            snows[i][0] = snows[i][0] + sd.random_number(-3, 3)
            snows[i][1] -= 1
        else:
            sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                         factor_b=snows[i][4], factor_c=snows[i][5], color=sd.background_color)
            snowdrift.append(snows[i])
            snows.remove(snows[i])
            create_snow(snow_number=i)
        sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                     factor_b=snows[i][4], factor_c=snows[i][5])

        sd.finish_drawing()

sd.pause()

# подсказка! для ускорения отрисовки можно
#  - убрать clear_screen()
#  - в начале рисования всех снежинок вызвать sd.start_drawing()
#  - на старом месте снежинки отрисовать её же, но цветом sd.background_color
#  - сдвинуть снежинку
#  - отрисовать её цветом sd.COLOR_WHITE на новом месте
#  - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg
