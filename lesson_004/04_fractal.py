# -*- coding: utf-8 -*-
import random
import simple_draw as sd

sd.resolution = (800, 600)


# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длинна ветвей" в 0.75 меньшей чем длина только что нарисованной ветви

# 3) первоначальный вызов:
# root_point = get_point(300, 30)
# draw_bunches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения


def draw_branches(start_point, angle, length):
    if length < 10:
        return
    v1 = sd.get_vector(start_point=start_point, angle=angle, length=length, width=2)
    v1.draw()
    v2 = sd.get_vector(start_point=start_point, angle=angle, length=length, width=2)
    v2.draw()
    next_point_1 = v1.end_point
    next_point_2 = v1.end_point
    next_angle_plus = angle + 30
    next_angle_minus = angle - 30
    next_length = length * .75
    draw_branches(start_point=next_point_1, angle=next_angle_plus, length=next_length)
    draw_branches(start_point=next_point_2, angle=next_angle_minus, length=next_length)


root_point = sd.get_point(300, 30)
draw_branches(start_point=root_point, angle=90, length=100)

sd.user_want_exit(1)
sd.clear_screen()


# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg

# Пригодятся функции
# sd.random_number()

def draw_branches(start_point, angle, length, is_random=True, is_summer_tree=True):
    if length < 2:
        return

    branch_width = int(1 + length / 5)
    if branch_width > 2:
        tree_color = sd.COLOR_DARK_RED
    elif is_summer_tree:
        tree_color = sd.COLOR_GREEN
    else:
        tree_color = sd.COLOR_WHITE

    for i in (-1, 1):
        v = sd.get_vector(start_point=start_point, angle=angle, length=length, width=branch_width)
        v.draw(tree_color)
        next_point_1 = v.end_point
        next_angle_1 = angle + 30 * i + is_random * random.randint(-40, 40)
        next_length_1 = length * .75 + is_random * length * random.randint(-20, 20) * 0.01
        draw_branches(start_point=next_point_1, angle=next_angle_1, length=next_length_1,
                      is_random=is_random, is_summer_tree=is_summer_tree)


root_point = sd.get_point(300, 30)
random_tree = True
summer_tree = False
draw_branches(start_point=root_point, angle=90, length=100, is_random=random_tree, is_summer_tree=summer_tree)


sd.pause()
