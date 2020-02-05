# -*- coding: utf-8 -*-

import simple_draw as sd


def start_snowfall(snow_number=20, snowfall_left=0, snowfall_right=250):
    snows = []
    for i in range(snow_number):
        create_snow(snow_number=i, snowfall_left=snowfall_left, snowfall_right=snowfall_right, snows=snows)
    return snows


def create_snow(snow_number=0, snowfall_left=0, snowfall_right=250, replacement=False, snows=None):
    snow = []
    snow.append(sd.random_number(snowfall_left, snowfall_right))
    snow.append(300 + sd.random_number(0, 600))
    snow.append(sd.random_number(3, 20))
    snow.append(sd.random_number(1, 10) * 0.1)
    snow.append(sd.random_number(1, 100) * 0.01)
    snow.append(sd.random_number(1, 90))
    if replacement:
        snows.insert(snow_number, snow)
    else:
        snows.append(snow)
    return snows


def snowfall(snows=None, snowfall_left=0, snowfall_right=250):
    snowdrift = snows

    for i in range(len(snows)):
        sd.start_drawing()
        for j in range(len(snowdrift)):
            sd.snowflake(center=sd.get_point(snowdrift[j][0], snowdrift[j][1]), length=snowdrift[j][2],
                         factor_a=snowdrift[j][3], factor_b=snowdrift[j][4], factor_c=snowdrift[j][5])
        sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                     factor_b=snows[i][4], factor_c=snows[i][5], color=sd.background_color)
        if snows[i][1] > 0:
            snows[i][0] = snows[i][0] + sd.random_number(-3, 3)
            if snows[i][0] > snowfall_right:
                snows[i][0] -= 3
            if snows[i][0] < snowfall_left:
                snows[i][0] += 3
            snows[i][1] -= 1
            sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                         factor_b=snows[i][4], factor_c=snows[i][5], color=sd.background_color)
        else:
            sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                         factor_b=snows[i][4], factor_c=snows[i][5])
            snows.remove(snows[i])
            create_snow(snow_number=i, snowfall_left=snowfall_left, snowfall_right=snowfall_right, replacement=True,
                        snows=snows)
        sd.snowflake(center=sd.get_point(snows[i][0], snows[i][1]), length=snows[i][2], factor_a=snows[i][3],
                     factor_b=snows[i][4], factor_c=snows[i][5])

        sd.finish_drawing()
