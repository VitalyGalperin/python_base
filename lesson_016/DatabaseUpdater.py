# -*- coding: utf-8 -*-

import peewee
from playhouse.db_url import connect

database = peewee.SqliteDatabase("database/weather.db")


class BaseTable(peewee.Model):
    class Meta:
        database = database


class Weather(BaseTable):
    location_name = peewee.CharField()
    location_en = peewee.CharField()
    coordinates = peewee.CharField()
    date = peewee.DateField()
    max_temp = peewee.CharField()
    min_temp = peewee.CharField()
    pressures = peewee.CharField()
    cloudiness = peewee.CharField()
    cloud_cover = peewee.CharField()
    precipitation = peewee.CharField()
    humidity = peewee.CharField()
    wind_speed = peewee.CharField()
    precipitation_hours = peewee.IntegerField()


class DatabaseUpdater:
    def __init__(self, db_url):
        self.connection = None
        self.db_url = db_url
        self.proxy = peewee.DatabaseProxy()  # TODO сейчас этим инструментом вы не пользуетесь
        # TODO его идея в том, что он заменит строку peewee.SqliteDatabase("database/weather.db")
        # TODO и в зависимости от того, какой db_url ему передадут - он создаст объект нужной БД
        # TODO если передать "sqlite:///weather.db", то будет создана как раз SqliteDatabase
        # TODO однако, чтобы это работало - надо будет указать self.proxy в
        #     class Meta:
        #         database = database
        # TODO либо просто можно пока убрать это, т.к. в нашем случае нам не нужно гарантировать работу
        # TODO с разными типами БД

    def run(self):
        try:
            self.connection = connect(self.db_url)
            self.proxy.initialize(self.connection)
        except Exception:
            print('Ошибка открытия базы данных')
        database.create_tables([Weather])

    def insert_row(self, weather_dict):
        if not self.select_row(weather_dict['location_name'], weather_dict['date']):
            Weather.create(location_name=weather_dict['location_name'],
                           location_en=weather_dict['location_en'],
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

    def select_row(self, location, date):
        try:
            row = Weather.select().where((Weather.location_name == location) & (Weather.date == date)).get()
        except Exception:
            return False
        weather_dict = {'location_name': row.location_name, 'location_en': row.location_en,
                        'coordinates': row.coordinates, 'date': row.date,
                        'max_temp': row.max_temp, 'min_temp': row.min_temp, 'pressures': row.pressures,
                        'cloudiness': row.cloudiness, 'humidity': row.humidity, 'wind_speed': row.wind_speed,
                        'cloud_cover': row.cloud_cover, 'precipitation': row.precipitation,
                        'precipitation_hours': row.precipitation_hours}
        return weather_dict

    def delete_all_data(self):
        Weather.delete().execute()
