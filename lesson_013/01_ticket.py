# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru

import argparse
import os
from PIL import Image, ImageDraw, ImageFont, ImageColor


def make_ticket(fio, from_, to, date):
    ticket_path = os.path.join(os.getcwd(), 'images')
    ticket_blank = 'ticket_template.png'
    ticket_result = 'ticket.png'
    ticket = Image.open(os.path.join(ticket_path, ticket_blank))
    font_path = os.path.join(os.getcwd(), 'fonts')
    font_file = 'ofont.ru_Open Sans.ttf'
    font = ImageFont.truetype(os.path.join(font_path, font_file), size=14)
    draw = ImageDraw.Draw(ticket)

    x = 46
    y = ticket.size[1] - 276
    field = f'{fio}'
    draw.text((x, y), field, font=font, fill=ImageColor.colormap['black'])

    y = ticket.size[1] - 207
    field = f'{from_}'
    draw.text((x, y), field, font=font, fill=ImageColor.colormap['black'])

    y = ticket.size[1] - 141
    field = f'{to}'
    draw.text((x, y), field, font=font, fill=ImageColor.colormap['black'])

    x = 286
    y = ticket.size[1] - 141
    field = f'{date}'
    draw.text((x, y), field, font=font, fill=ImageColor.colormap['black'])

    ticket.save(os.path.join(ticket_path, ticket_result))


if __name__ == '__main__':
    make_ticket(fio='ГАЛЬПЕРИН В.А.', from_='ЭЙЛАТ (IL)', to='МОСКВА (RU)', date='20.07.2020')

# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля agrparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.
# Зачет