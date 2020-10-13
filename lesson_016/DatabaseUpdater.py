# -*- coding: utf-8 -*-

import sqlite3
import peewee

database = peewee.SqliteDatabase("database/weather.db")


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Weather(BaseTable):
    location_name = peewee.CharField()
    coordinates = peewee.CharField()
    date = peewee.CharField()
    max_temp = peewee.CharField()
    min_temp = peewee.CharField()
    pressures = peewee.CharField()
    cloudiness = peewee.CharField()
    cloud_cover = peewee.CharField()
    precipitation = peewee.CharField()
    humidity = peewee.CharField()
    wind_speed = peewee.CharField()
    precipitation_hours = peewee.CharField()


class DatabaseUpdater:
    def __init__(self):
        self.connection = None
        database.create_tables([Weather])
        # try:
        #     self.connection = sqlite3.connect("database/weather.db")
        # except Exception:
        #     print('Ошибка открытия базы данных')

    def select_row(self):
        pass

    def insert_row(self, weather_dict):
        Weather(location_name=weather_dict['location_name'],
                coordinates=weather_dict['coordinates'],
                date=weather_dict['date'],
                max_temp=weather_dict['max_temp'],
                min_temp=weather_dict['min_temp'],
                pressures=weather_dict['pressures'],
                cloudiness=weather_dict['cloudiness'],
                cloud_cover=weather_dict['cloud_cover'],
                precipitation=weather_dict['precipitation'],
                humidity=weather_dict['humidity'],
                wind_speed=weather_dict['wind_speed'],
                precipitation_hours=weather_dict['precipitation_hours'])



