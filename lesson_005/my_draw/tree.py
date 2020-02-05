# -*- coding: utf-8 -*-

import random
import simple_draw as sd

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

