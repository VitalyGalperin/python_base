# -*- coding: utf-8 -*-
import bs4
import requests
import re

re_pressure = r'"pressure":(\d+\.\d)'
re_cloud_cover = r'"cloudCover":(\d+\.\d)'
re_temperature = r'"temperature":(-?\d+\.\d+)'
re_humidity = r'"humidity":(\d\.\d+)'
re_wind_speed = r'"windSpeed":(\d+\.\d+)'
re_cloudiness = r'"summary":"(\w+)\"'
re_precipitation = r'"precipType":"(\w+)\"'

response = requests.get('https://darksky.net/details/56.3268,44.0058/2019-02-25/ca12/en').text
# response = requests.get('https://darksky.net/details/29.5563,34.9525/2020-10-3/ca12/en').text
# response = requests.get('https://darksky.net/details/56.3268,44.0058/2019-10-5/ca12/en').text

soup = bs4.BeautifulSoup(response, 'html.parser')

spans = soup.find_all('span')
scripts = soup.find_all('script')

for span in spans:
    if str(span).find('pressure') != -1:
        print(span)

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
pressures = humidity = wind_speed = ''

if pressures_values:
    pressures = round(sum(pressures_values) / len(pressures_values), 1)
if humidity_values:
    humidity = round(sum(humidity_values) / len(humidity_values), 2)
if wind_speed_values:
    wind_speed = round(sum(wind_speed_values) / len(wind_speed_values), 2)

weather_dict = {'MaxTemp': max(temperature_values), 'MinTemp': min(temperature_values), 'pressures': pressures,
                'humidity': humidity, 'wind_speed': wind_speed}

print(cloud_cover_values)
print(len(cloud_cover_values))
print(cloudiness_values)
print(len(cloudiness_values))
print(precipitation_values)
print(len(precipitation_values))
