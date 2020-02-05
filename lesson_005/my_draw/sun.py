# -*- coding: utf-8 -*-

import simple_draw as sd


def sun(x, y, blink=True, galo_count=0):
    sd.circle(sd.get_point(x, y), radius=50, color=sd.COLOR_YELLOW, width=0)
    face_color = sd.COLOR_RED
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
        sd.circle(sd.get_point(x + 13, y + 12), radius=2, color=face_color)
        sd.circle(sd.get_point(x - 13, y + 12), radius=2, color=face_color)
    sd.line(start_point=sd.get_point(x, y - 12), end_point=sd.get_point(x, y + 8), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x - 4, y - 12), end_point=sd.get_point(x + 5, y - 12), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x - 10, y - 23), end_point=sd.get_point(x + 11, y - 23), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x + 11, y - 23), end_point=sd.get_point(x + 16, y - 18), color=face_color, width=3)
    sd.line(start_point=sd.get_point(x - 10, y - 23), end_point=sd.get_point(x - 15, y - 18), color=face_color, width=3)
    sd.circle(sd.get_point(x, y), radius=50 + galo_count * 6, color=sd.COLOR_YELLOW, width=2)
    sd.circle(sd.get_point(x, y), radius=50 + (galo_count - 1) * 6, color=sd.background_color, width=2)
    if galo_count == 0:
        sd.circle(sd.get_point(x, y), radius=50 + (galo_count + 9) * 6, color=sd.background_color, width=2)
