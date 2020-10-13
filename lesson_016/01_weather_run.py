from WeatherMaker import WeatherMaker
from ImageMaker import ImageMaker


class WeatherHandler:
    def __init__(self, location, stare_date, final_date=None, is_rewrite_db=False, is_card=True, is_console=False):
        self.location = location
        self.stare_date = stare_date
        if final_date is None:
            self.final_date = stare_date
        self.is_card = is_card
        self.is_rewrite = is_rewrite_db
        self.is_console = is_console

    def run(self):
        pass


if __name__ == "__main__":
    weather = WeatherMaker('Нижний Новгород', '2020-1-15')
    # weather = WeatherMaker('Эйлат', '2020-11-10')
    weather_dict = weather.run()
    image = ImageMaker(weather_dict)
    image.run()
