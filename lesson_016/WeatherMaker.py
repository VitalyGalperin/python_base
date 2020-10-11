# -*- coding: utf-8 -*-

from geopy.geocoders import OpenMapQuest
import bs4
import requests
import re

OpenMapQuest_API_KEY = 'kvDuJJUTE50Ax5XG8mxbCVDGnQqHFdvL'


class WeatherMaker:

    def __init__(self, location, date):
        self.location_name = location
        self.coordinates = ''
        self.date = date

    def run(self):
        if self.get_coordinates():
            return self.dark_sky_parsing()
        else:
            return False

    def get_coordinates(self):
        try:
            location_request = OpenMapQuest(api_key=OpenMapQuest_API_KEY).geocode(self.location_name)
        except Exception:
            print('Ошибка запроса места')
            return False
        if not location_request:
            print('Такое место не найдено')
            return False

        location_latitude = str(round(location_request.latitude, 4))
        location_longitude = str(round(location_request.longitude, 4))
        self.coordinates = location_latitude + ',' + location_longitude
        return True

    def dark_sky_parsing(self):
        weather_dict = {}
        re_pressure = r'"pressure":(\d+\.\d)'
        re_cloud_cover = r'"cloudCover":(\d+\.\d)'
        re_temperature = r'"temperature":(-?\d+\.\d+)'
        re_humidity = r'"humidity":(\d\.\d+)'
        re_wind_speed = r'"windSpeed":(\d+\.\d+)'
        re_cloudiness = r'"summary":"([A-Za-z ]+)"'
        re_precipitation = r'"precipType":"([A-Za-z ]+)"'

        try:
            response = requests.get(f'https://darksky.net/details/{self.coordinates}/{self.date}/ca12/en').text
        except Exception:
            print('Ошибка запроса прогноза погоды')
            return False

        soup = bs4.BeautifulSoup(response, 'html.parser')
        scripts = soup.find_all('script')

        pressures_values = re.findall(re_pressure, str(scripts[1]))
        cloud_cover_values = re.findall(re_cloud_cover, str(scripts[1]))
        temperature_values = re.findall(re_temperature, str(scripts[1]))
        humidity_values = re.findall(re_humidity, str(scripts[1]))
        wind_speed_values = re.findall(re_wind_speed, str(scripts[1]))
        cloudiness_values = re.findall(re_cloudiness, str(scripts[1]))
        precipitation_values = re.findall(re_precipitation, str(scripts[1]))

        temperature_values = [round(float(item), 0) for item in temperature_values]
        pressures_values = [float(item) for item in pressures_values]
        humidity_values = [float(item) for item in humidity_values]
        wind_speed_values = [float(item) for item in wind_speed_values]
        cloud_cover_values = [float(item) for item in cloud_cover_values]
        pressures = humidity = wind_speed = cloud_cover = precipitation = cloudiness = precipitation_hours = ''

        if pressures_values:
            pressures = str(round(sum(pressures_values) / len(pressures_values), 1))
        if humidity_values:
            humidity = str(round(sum(humidity_values) / len(humidity_values), 2))
        if wind_speed_values:
            wind_speed = str(round(sum(wind_speed_values) / len(wind_speed_values), 2))
        if cloud_cover_values:
            cloud_cover = str(round(sum(cloud_cover_values) / len(cloud_cover_values), 1))
        if precipitation_values:
            precipitation = max(list(precipitation_values), key=lambda x: precipitation_values.count(x))
            precipitation_hours = len(precipitation_values)
        if cloudiness_values:
            cloudiness = str(max(list(cloudiness_values), key=lambda x: cloudiness_values.count(x)))

        if max(temperature_values) > 0:
            max_temperature = '+' + str(max(temperature_values))
        else:
            max_temperature = str(max(temperature_values))

        if min(temperature_values) > 0:
            min_temperature = '+' + str(min(temperature_values))
        else:
            min_temperature = str(min(temperature_values))

        year, month, day = self.date.split('-')
        self.date = day + '/' + month + '/' + year

        weather_dict = {'location_name': self.location_name, 'coordinates': self.coordinates, 'date': self.date,
                        'max_temp': max_temperature, 'min_temp': min_temperature, 'pressures': pressures,
                        'cloudiness': cloudiness, 'humidity': humidity, 'wind_speed': wind_speed,
                        'cloud_cover': cloud_cover, 'precipitation': precipitation,
                        'precipitation_hours': precipitation_hours}
        return weather_dict

# if __name__ == "__main__":
#     weather = WeatherMaker('Нижний Новгород', '2020-10-5')
#     weather.run()
