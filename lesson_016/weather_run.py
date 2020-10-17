# -*- coding: utf-8 -*-

from WeatherMaker import WeatherMaker
from DatabaseUpdater import DatabaseUpdater
from ImageMaker import ImageMaker
from ConsolePrinter import ConsolePrinter
from set import DB_URL, re_date

import datetime
import re
import argparse


class WeatherHandler:
    def __init__(self, location, start_date=None, final_date=None, is_write_db=False, is_read_db=False,
                 is_card=True, is_console_out=False):
        self.location = location
        self.start_date = start_date
        is_card, is_console_out, is_read_db, is_write_db = self.check_parameters(is_card, is_console_out, is_read_db,
                                                                                 is_write_db)
        self.is_card = is_card
        self.is_write_db = is_write_db
        self.is_read_db = is_read_db
        self.is_console = is_console_out
        self.final_date = final_date
        self.db_url = DB_URL
        self.weather_dict = None

    def run(self):
        if not self.get_dates():
            return False
        db = DatabaseUpdater(db_url=self.db_url)
        db.run()
        # db.delete_all_data()
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
            if self.is_console:
                ConsolePrinter(self.weather_dict).run()
        if self.is_card:
            ImageMaker(self.weather_dict).run()
        return True

    def get_dates(self):
        if not self.start_date:
            self.start_date = datetime.datetime.now() - datetime.timedelta(days=7)
            self.final_date = datetime.datetime.now()
        else:
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

    def check_parameters(self, is_card, is_console_out, is_read_db, is_write_db):
        if isinstance(is_card, str):
            is_card = is_card.upper()
            if is_card.find('Y') != -1 or is_card.find('ДА') != -1:
                is_card = True
            else:
                is_card = False
        if isinstance(is_write_db, str):
            is_write_db = is_write_db.upper()
            if is_write_db.find('N') != -1 or is_write_db.find('НЕТ') != -1:
                is_write_db = False
            else:
                is_write_db = True
        if isinstance(is_read_db, str):
            is_read_db = is_read_db.upper()
            if is_read_db.find('N') != -1 or is_read_db.find('НЕТ') != -1:
                is_read_db = False
            else:
                is_read_db = True
        if isinstance(is_console_out, str):
            is_console_out = is_console_out.upper()
            if is_console_out.find('N') != -1 or is_console_out.find('НЕТ') != -1:
                is_console_out = False
            else:
                is_console_out = True
        return is_card, is_console_out, is_read_db, is_write_db


if __name__ == "__main__":
    # WeatherHandler('Нижний Новгород', '01-10-2020').run()
    # WeatherHandler('Нижний Новгород', '01-10-2020', is_write_db=True).run()
    # WeatherHandler('Эйлат', '02-10-2020', is_write_db=True, is_card=False).run()
    # WeatherHandler('Эйлат', '02-10-2020', is_write_db=False, is_read_db=True, is_card=True).run()
    # WeatherHandler('Эйлат', '02-10-2020', '05-10-2020', is_write_db=True).run()
    # WeatherHandler('Эйлат', '15-10-2020', '17-10-2020', is_write_db=True, is_card=False).run()
    WeatherHandler('Нижний Новгород', '10-12-2019', '10-10-2020', is_write_db=True, is_card=True, is_read_db=False, is_console_out=True).run()
    # WeatherHandler('Эйлат', '10-10-2019', '10-10-2020', is_write_db=True, is_card=True, is_read_db=False, is_console_out=True).run()

# if __name__ == '__main__':
#     weather_run = argparse.ArgumentParser()
#     weather_run.add_argument('--start_date', dest='start_date', help='Дата начала периода в формате DD-MM-YYYY')
#     weather_run.add_argument('--final_date', dest='final_date', help='Дата конца периода в формате DD-MM-YYYY')
#     weather_run.add_argument('--write', dest='is_write_db', help='Сохранять ли резулшьтаты в БД. Y(Да)/N(Нет)')
#     weather_run.add_argument('--read', dest='is_read_db', help='Брать ли резулшьтаты из БД. Y(Да)/N(Нет)')
#     weather_run.add_argument('--card', dest='is_card',
#                              help='Рисовать ли открытку Y(Да)/N (Нет). Открытка формируется для последнего дня периода')
#     weather_run.add_argument('--print', dest='is_console_out', help='Печатать ли результат на консоль Y(Да)/N(Нет).')


# Командная строка Для вызова с терминала
# python weather_run --start_date '10-10-2020'
