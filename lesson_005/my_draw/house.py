# -*- coding: utf-8 -*-

import simple_draw as sd


def draw_house(house_left, house_bottom, house_right, house_top):
    left_bottom = sd.get_point(house_left, house_bottom)
    right_top = sd.get_point(house_right, house_top)
    right_bottom = sd.get_point(house_right, house_bottom)
    right_top_plus = sd.get_point(house_right + 26, house_top)
    sd.rectangle(left_bottom, right_top, color=sd.COLOR_DARK_RED, width=0)
    for i in range(int((house_right - house_left) / 25)):
        for j in range(int((house_top - house_bottom) / 12) + 1):
            brick = sd.rectangle(sd.get_point((i * 25 + j % 2 * 12) + house_left, (0 + j * 12) + house_bottom),
                                 sd.get_point((25 + i * 25 + j % 2 * 12) + house_left, (12 + j * 12) + house_bottom),
                                 color=sd.COLOR_WHITE, width=1)
    sd.rectangle(right_bottom, right_top_plus, color=sd.background_color, width=0)
    roof_left_x = house_left - (house_right - house_left) / 6
    roof_right_x = house_right + (house_right - house_left) / 6
    house_center_x = house_left + (house_right - house_left) / 2
    roof_top_y = house_top + (house_top - house_bottom) / 2
    roof_points = []
    roof_points.append(sd.get_point(house_center_x, roof_top_y))
    roof_points.append(sd.get_point(roof_left_x, house_top))
    roof_points.append(sd.get_point(roof_right_x, house_top))
    sd.polygon(roof_points, color=sd.COLOR_RED, width=0, )
    left_bottom_window = sd.get_point(house_left + 50, house_bottom + 50)
    right_top_window = sd.get_point(house_right - 50, house_top - 50)
    sd.rectangle(left_bottom_window, right_top_window, color=sd.COLOR_GREEN, width=0)
    sd.rectangle(left_bottom_window, right_top_window, color=sd.COLOR_WHITE, width=5)
    sd.line(sd.get_point(house_center_x, house_top - 50), sd.get_point(house_center_x, house_bottom + 50),
            color=sd.COLOR_WHITE, width=5)

