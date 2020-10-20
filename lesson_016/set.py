import re

re_date = re.compile(
    r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')

OpenMapQuest_API_KEY = 'kvDuJJUTE50Ax5XG8mxbCVDGnQqHFdvL'

DB_URL = "sqlite:///database/weather.db"

IMAGE_DIR = 'image_data'
CARD_DIR = 'card'
BLANK_FILE = 'blank.jpg'

RAIN_ICON = 'rain.jpg'
SNOW_ICON = 'snow.jpg'
DRIZZLE_ICON = 'drizzle.jpg'
CLOUDY_ICON = 'cloudy.jpg'
OVERCAST_ICON = 'overcast.jpg'
FOGGY_ICON = 'foggy.jpg'
SUNNY_ICON = 'sun.jpg'
SLEET_ICON = 'sleet.jpg'

FONT_COLOR = (20, 20, 0)

YELLOW = (1, 0, 0)
CYAN = (0, 0, 1)
BLUE = (0, 1, 1)
GRAY = (0.5, 0.5, 0.5)
