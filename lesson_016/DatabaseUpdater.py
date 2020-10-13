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
    def __init__(self, weather_dict, ):
        self.weather_dict = weather_dict

    def run(self):
        pass

    def select_row(self):
        pass

    def insert_row(self):
        pass


database.create_tables([Weather])

conn = sqlite3.connect("database/weather.db")
conn.text_factory = bytes
cursor = conn.cursor()

cursor.execute('SELECT * FROM Weather')
results = cursor.fetchall()
print(results)
