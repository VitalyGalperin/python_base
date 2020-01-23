# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)

start_point = sd.get_point(50, 50)
end_point = sd.get_point(350, 450)

color_number = 0

for _ in rainbow_colors:
    sd.line(start_point=start_point, end_point=end_point, color=rainbow_colors[color_number], width=4)
    start_point = sd.get_point(50 + 5 * color_number, 50)
    end_point = sd.get_point(350 + 5 * color_number, 450)
    color_number += 1

sd.user_want_exit(1)
sd.clear_screen()

# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво

center_position = sd.get_point(400, -100)
color_number = 0

for _ in rainbow_colors:
    center_position = sd.get_point(400, -100)
    sd.circle(center_position=center_position, radius=500 + 20 * color_number, color=rainbow_colors[color_number],
              width=20)
    color_number += 1

sd.pause()

# Зачет
