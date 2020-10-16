# -*- coding: utf-8 -*-

# import sqlite3
import peewee
# import os
from playhouse.db_url import connect

database = peewee.SqliteDatabase("database/weather.db")


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Weather(BaseTable):
    location_name = peewee.CharField()
    coordinates = peewee.CharField()
    date = peewee.DateTimeField()
    max_temp = peewee.CharField()
    min_temp = peewee.CharField()
    pressures = peewee.CharField()
    cloudiness = peewee.CharField()
    humidity = peewee.CharField()
    wind_speed = peewee.CharField()


class DatabaseUpdater:
    def __init__(self, db_url):
        self.connection = None
        self.db_url = db_url

    def run(self):
        try:
            self.connection = connect(self.db_url)
            # self.connection = sqlite3.connect()
        except Exception:
            print('Ошибка открытия базы данных')
        database.create_tables([Weather])

    def select_row(self, location, date):
        try:
            row = Weather.select().where(Weather.location_name == location and Weather.date == date).get()
        except Exception:
            return False
        weather_dict = {'location_name': row.location_name, 'coordinates': row.coordinates, 'date': row.date,
                        'max_temp': row.max_temp, 'min_temp': row.min_temp, 'pressures': row.pressures,
                        'cloudiness': row.cloudiness, 'humidity': row.humidity, 'wind_speed': row.wind_speed,
                        'cloud_cover': row.cloud_cover, 'precipitation': row.precipitation,
                        'precipitation_hours': row.precipitation_hours}
        return weather_dict

    def insert_row(self, weather_dict):
        if not self.select_row(weather_dict['location_name'], weather_dict['date']):
            Weather.create(location_name=weather_dict['location_name'],
                           coordinates=weather_dict['coordinates'],
                           date=weather_dict['date'],
                           max_temp=weather_dict['max_temp'],
                           min_temp=weather_dict['min_temp'],
                           pressures=weather_dict['pressures'],
                           cloudiness=weather_dict['cloudiness'],
                           humidity=weather_dict['humidity'],
                           wind_speed=weather_dict['wind_speed'])

    def delete_all_data(self):
        Weather.delete().execute()



