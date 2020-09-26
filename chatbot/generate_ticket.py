from io import BytesIO
import requests
from PIL import Image, ImageFont, ImageDraw

TEMPLATE_PATH = 'sourсes/air-ticket-blank.png'
FONT_PATH = 'sourсes/Roboto-Regular.ttf'
FONT_SIZE = 18
BLACK = (0, 0, 0, 255)

NAME_OFFSET = (270, 145)
DEPARTURE_CITY_OFFSET = (130, 190)
ARRIVAL_CITY_OFFSET = (130, 231)
FLIGHT_OFFSET = (145, 307)
DATE_OFFSET = (145, 365)
TIME_OFFSET = (590, 365)

AVATAR_SIZE = 56
AVATAR_OFFSET = (685, 35)


def generate_ticket(first_name, last_name, departure_city, departure_date, departure_time, arrival_city, flight):
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, first_name + ' ' + last_name, font=font, fill=BLACK)
    draw.text(DEPARTURE_CITY_OFFSET, departure_city, font=font, fill=BLACK)
    draw.text(ARRIVAL_CITY_OFFSET, arrival_city, font=font, fill=BLACK)
    draw.text(FLIGHT_OFFSET, flight, font=font, fill=BLACK)
    draw.text(DATE_OFFSET, departure_date, font=font, fill=BLACK)
    draw.text(TIME_OFFSET, departure_time, font=font, fill=BLACK)

    response = requests.get(url=f'https://api.adorable.io/avatars/{AVATAR_SIZE}/{last_name}')

    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)
    base.paste(avatar, AVATAR_OFFSET)

    # with open('sourсes/ticket_to_send.png', 'wb') as file:
    #     base.save(file, 'png')
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)           # возврат курсора в точку 0

    return temp_file

# generate_ticket('Виталий', 'Гальперин', 'Нижний Новгород (GOJ)', '01-12-2020', '14:55+03:00', 'Москва (MOW)', 'S7 1096')


