# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for
simple_draw.background_color = (255, 255, 255)
for x in range(7):
    for y in range(12):
        brick = simple_draw.rectangle(simple_draw.get_point(-50 + x * 100 + y % 2 * 50, 0 + y * 50),
                                      simple_draw.get_point(50 + x * 100 + y % 2 * 50, 50 + y * 50),
                                      color=simple_draw.COLOR_BLACK, width=1)

simple_draw.line(simple_draw.get_point(190,358),simple_draw.get_point(315,395),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(240,375),simple_draw.get_point(240,300),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(260,365),simple_draw.get_point(260,330),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(278,363),simple_draw.get_point(278,320),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(260,342),simple_draw.get_point(278,345),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(302,363),simple_draw.get_point(302,320),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(302,361),simple_draw.get_point(358,380),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(308,338),simple_draw.get_point(333,344),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(302,320),simple_draw.get_point(337,327),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(185,280),simple_draw.get_point(215,180),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(215,180),simple_draw.get_point(235,265),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(232,263),simple_draw.get_point(251,178),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(251,178),simple_draw.get_point(285,276),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(270,176),simple_draw.get_point(288,230),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(288,230),simple_draw.get_point(302,178),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(278,194),simple_draw.get_point(299,199),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(322,230),simple_draw.get_point(320,176),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(320,176),simple_draw.get_point(338,186),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(350,238),simple_draw.get_point(351,173),color=simple_draw.COLOR_RED, width=4)
simple_draw.line(simple_draw.get_point(352,173),simple_draw.get_point(376,186),color=simple_draw.COLOR_RED, width=4)

simple_draw.pause()

# Вас получилось отличное решение, мало кто пишет такой выразительный код!

# Зачет
