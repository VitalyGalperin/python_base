# -*- coding: utf-8 -*-
import bs4
import requests
import re

re_pressure = r'"pressure":(\d+\.\d)'
re_cloud_cover = r'"cloudCover":(\d+\.\d)'
re_temperature = r'"temperature":(-?\d+\.\d+)'
re_humidity = r'"humidity":(\d\.\d+)'
re_wind_speed = r'"windSpeed":(\d+\.\d+)'
re_cloudiness = r'"summary":"([A-Za-z ]+)"'
re_precipitation = r'"precipType":"([A-Za-z ]+)"'

# response = requests.get('https://darksky.net/details/29.5563,34.9525/2020-10-5/ca12/en').text  # NN
response = requests.get(f'https://darksky.net/details/56.3268,44.0058/2019-11-14/ca12/en').text  # Eilat

soup = bs4.BeautifulSoup(response, 'html.parser')

spans = soup.find_all('span')
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
    pressures = round(sum(pressures_values) / len(pressures_values), 1)
if humidity_values:
    humidity = round(sum(humidity_values) / len(humidity_values), 2)
if wind_speed_values:
    wind_speed = round(sum(wind_speed_values) / len(wind_speed_values), 2)
if cloud_cover_values:
    cloud_cover = round(sum(cloud_cover_values) / len(cloud_cover_values), 1)
if precipitation_values:
    precipitation = max(list(precipitation_values), key=lambda x: precipitation_values.count(x))
    precipitation_hours = len(precipitation_values)
if cloudiness_values:
    cloudiness = max(list(cloudiness_values), key=lambda x: cloudiness_values.count(x))

weather_dict = {'MaxTemp': max(temperature_values), 'MinTemp': min(temperature_values), 'pressures': pressures,
                'humidity': humidity, 'wind_speed': wind_speed, 'cloud_cover': cloud_cover, 'cloudiness': cloudiness,
                'precipitation': precipitation, 'precipitation_hours': precipitation_hours}

