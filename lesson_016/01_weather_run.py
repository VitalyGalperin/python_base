from WeatherMaker import WeatherMaker
from DatabaseUpdater import DatabaseUpdater
from ImageMaker import ImageMaker

import datetime
import re

re_date = re.compile(
    r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')


class WeatherHandler:
    def __init__(self, location, start_date, final_date=None, is_write_db=False, is_read_db=False, is_card=True,
                 is_console=False):
        self.location = location
        self.start_date = start_date
        self.is_card = is_card
        self.is_write_db = is_write_db
        self.is_read_db = is_read_db
        self.is_console = is_console
        self.final_date = final_date

    def run(self):
        if not self.get_dates():
            return False
        weather_dict = WeatherMaker(self.location, self.start_date).run()
        if not weather_dict:
            return False
        if self.is_card:
            ImageMaker(weather_dict).run()
        if self.is_write_db:
            a = DatabaseUpdater()
            a.insert_row(weather_dict)
        return True

    def get_dates(self):
        self.start_date = self.convert_date(self.start_date)
        if self.start_date is None:
            print('Дата должна быть указана в формате DD-MM-YYYY')
            return False
        if self.final_date is None:
            self.final_date = self.start_date
        else:
            self.final_date = self.convert_date(self.final_date)
            if self.final_date is None:
                print('Финальная дата должна быть указана в формате DD-MM-YYYY')
                return False
        return True

    def convert_date(self, date):
        if date:
            match = re.match(re_date, date)
            if match and len(date) == 10:
                date = datetime.date(day=int(date[:2]), month=int(date[3:5]), year=int(date[6:10]))
                return date
        else:
            return False


if __name__ == "__main__":
    WeatherHandler('Нижний Новгород', '01-10-2020').run()
    WeatherHandler('Эйлат', '01-10-2020', is_write_db=True, is_card=False).run()
