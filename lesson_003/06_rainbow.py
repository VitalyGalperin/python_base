# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)

start_point = sd.get_point(50, 50)
end_point = sd.get_point(350, 450)
i = 1
# TODO Необхомо итерироваться по rainbow_colors
for i in range(7):
    sd.line(start_point=start_point, end_point=end_point, color=rainbow_colors[i], width=4)
    start_point = sd.get_point(50 + 5 * i, 50)
    end_point = sd.get_point(350 + 5 * i, 450)

sd.user_want_exit(1)
sd.clear_screen()

# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво

center_position = sd.get_point(400, -100)
i = 1
# TODO Необхомо итерироваться по rainbow_colors
for i in range(7):
    center_position = sd.get_point(400, -100)
    sd.circle(center_position=center_position, radius=500 + 20 * i, color=rainbow_colors[i], width=20)

sd.pause()
