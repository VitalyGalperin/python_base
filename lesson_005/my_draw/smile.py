# -*- coding: utf-8 -*-

import simple_draw as sd


def smile(x, y, blink=True):
    sd.ellipse(left_bottom=sd.get_point(x - 30, y - 35), right_top=sd.get_point(x + 30, y + 35),
               color=sd.COLOR_PURPLE)
    face_color = sd.COLOR_DARK_BLUE
    if blink:
        sd.line(start_point=sd.get_point(x + 4, y + 12), end_point=sd.get_point(x + 24, y + 12),
                color=face_color, width=2)
        sd.line(start_point=sd.get_point(x - 23, y + 12), end_point=sd.get_point(x - 3, y + 12),
                color=face_color, width=2)
    else:
        sd.ellipse(left_bottom=sd.get_point(x + 4, y + 6), right_top=sd.get_point(x + 24, y + 18),
                   color=face_color, width=2)
        sd.ellipse(left_bottom=sd.get_point(x - 23, y + 6), right_top=sd.get_point(x - 3, y + 18),
                   color=face_color, width=2)
        sd.circle(sd.get_point(x + 12, y + 12), radius=2, color=face_color)
        sd.circle(sd.get_point(x - 15, y + 12), radius=2, color=face_color)
    sd.line(start_point=sd.get_point(x, y - 8), end_point=sd.get_point(x, y + 8), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x - 4, y - 8), end_point=sd.get_point(x + 5, y - 8), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x - 10, y - 18), end_point=sd.get_point(x + 11, y - 18), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x + 11, y - 18), end_point=sd.get_point(x + 16, y - 15), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x - 10, y - 18), end_point=sd.get_point(x - 15, y - 15), color=face_color, width=3)
