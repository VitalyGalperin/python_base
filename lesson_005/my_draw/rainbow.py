# -*- coding: utf-8 -*-

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)


def draw_raindow(center, radius, width):
    color_number = 0

    for _ in rainbow_colors:
        center_position = center
        sd.circle(center_position=center, radius=radius + width * color_number,
                  color=rainbow_colors[color_number],
                  width=width)
        color_number += 1
