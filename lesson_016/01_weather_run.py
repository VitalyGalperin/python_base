from WeatherMaker import WeatherMaker
from ImageMaker import ImageMaker


class WeatherHandler:
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    weather = WeatherMaker('Нижний Новгород', '2020-10-5')
    weather_dict = weather.run()
    image = ImageMaker(weather_dict)
    image.run()
