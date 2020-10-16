from WeatherMaker import WeatherMaker
from DatabaseUpdater import DatabaseUpdater
from ImageMaker import ImageMaker
from set import DB_URL, re_date

import datetime
import re


class WeatherHandler:
    def __init__(self, location, start_date, final_date=None, is_write_db=False, is_read_db=False,
                 is_card=True, is_console=False, db_url=DB_URL):
        self.location = location
        self.start_date = start_date
        self.is_card = is_card
        self.is_write_db = is_write_db
        self.is_read_db = is_read_db
        self.is_console = is_console
        self.final_date = final_date
        self.db_url = db_url
        self.weather_dict = None

    def run(self):
        if not self.get_dates():
            return False
        db = DatabaseUpdater(db_url=self.db_url)
        db.run()
        db.delete_all_data()
        for day in range((self.final_date - self.start_date).days + 1):
            self.weather_dict = None
            if self.is_read_db:
                self.weather_dict = db.select_row(self.location, self.start_date + datetime.timedelta(days=day))
            if not self.weather_dict:
                self.weather_dict = WeatherMaker(self.location, self.start_date + datetime.timedelta(days=day)).run()
            if not self.weather_dict:
                return False
            if self.is_write_db:
                db.insert_row(self.weather_dict)
        if self.is_card:
            ImageMaker(self.weather_dict).run()
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
    # WeatherHandler('Нижний Новгород', '01-10-2020').run()
    # WeatherHandler('Нижний Новгород', '01-10-2020', is_write_db=True).run()
    # WeatherHandler('Эйлат', '02-10-2020', is_write_db=True, is_card=False).run()
    # WeatherHandler('Эйлат', '02-10-2020', is_write_db=False, is_read_db=True, is_card=True).run()
    # WeatherHandler('Эйлат', '02-10-2020', '05-10-2020', is_write_db=True).run()
    # WeatherHandler('Эйлат', '15-10-2020', '17-10-2020', is_write_db=True, is_card=False).run()
    WeatherHandler('Нижний Новгород', '01-10-2020', '03-10-2020', is_write_db=True, is_card=True).run()