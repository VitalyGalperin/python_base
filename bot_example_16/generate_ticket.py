from PIL import Image, ImageFont, ImageDraw

TEMPLATE_PATH = 'files/ticket_base.png'
FONT_PATH = 'files/Roboto-Regular.ttf'
FONT_SIZE = 50
BLACK = (0, 0, 0, 255)

NAME_OFFSET = (250, 220)
EMAIL_OFFSET = (250, 450)


def generate_ticket(name, email):
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    base.show()


generate_ticket('Vasily', 'vasily@ghj.kjn')