from io import BytesIO
import requests
from PIL import Image, ImageFont, ImageDraw

TEMPLATE_PATH = 'files/ticket_base.png'
FONT_PATH = 'files/Roboto-Regular.ttf'
FONT_SIZE = 50
BLACK = (0, 0, 0, 255)

NAME_OFFSET = (250, 220)
EMAIL_OFFSET = (250, 450)

AVATAR_SIZE = 180
AVATAR_OFFSET = (10, 10)


def generate_ticket(name, email):
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    response = requests.get(url=f'https://api.adorable.io/avatars/{AVATAR_SIZE}/{email}')
    # Полученный аватар можно сохранить в файл
    # with open("files/avatar.png", "wb") as avatar_file:
    #     avatar_file.write(response.content)
    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)
    base.paste(avatar, AVATAR_OFFSET)

    # Результат можно сохранять в файл
    # with open('files/ticket_example.png', 'wb') as file:
    #     base.save(file, 'png')

    # Или в виртуальный файл
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)           # возврат курсора в точку 0

    return temp_file

# Вызов самой себя для теста
# generate_ticket('Vasily', 'vasily@ghj.kjn')
