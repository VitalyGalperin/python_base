# -*- coding: utf-8 -*-

import simple_draw as sd


def cat(x, y):
    sd.ellipse(left_bottom=sd.get_point(x - 40, y - 12), right_top=sd.get_point(x + 40, y + 16),
               color=sd.COLOR_BLACK)
    sd.ellipse(left_bottom=sd.get_point(x + 30, y - 50), right_top=sd.get_point(x + 40, y),
               color=sd.COLOR_BLACK)
    sd.circle(sd.get_point(x - 40, y + 12), radius=16, color=sd.COLOR_WHITE)
    sd.circle(sd.get_point(x - 40, y + 12), radius=15, color=sd.COLOR_BLACK, width=0)
    cat_ear = []
    cat_ear.append(sd.get_point(x - 43, y + 23))
    cat_ear.append(sd.get_point(x - 53, y + 23))
    cat_ear.append(sd.get_point(x - 47, y + 33))
    sd.polygon(cat_ear, color=sd.COLOR_BLACK, width=0)
    cat_ear = []
    cat_ear.append(sd.get_point(x - 30, y + 23))
    cat_ear.append(sd.get_point(x - 40, y + 23))
    cat_ear.append(sd.get_point(x - 35, y + 33))
    sd.polygon(cat_ear, color=sd.COLOR_BLACK, width=0)
    sd.circle(sd.get_point(x - 40, y + 12), radius=1, color=sd.COLOR_WHITE)
    sd.circle(sd.get_point(x - 45, y + 17), radius=2, color=sd.COLOR_BLUE)
    sd.circle(sd.get_point(x - 35, y + 18), radius=2, color=sd.COLOR_BLUE)
    sd.line(sd.get_point(x - 42, y + 6), sd.get_point(x - 38, y + 6))
