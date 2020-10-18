# -*- coding: utf-8 -*-

class ConsolePrinter:

    def __init__(self, weather_dict):
        self.weather_dict = weather_dict

    def run(self):
        precipitation_text = ''
        print('---------------------------------------------------------------------')
        print(self.weather_dict['location_name'] + '. координаты: ' + self.weather_dict['coordinates'])
        print('Дата: ' + self.weather_dict['date'].strftime("%d/%m/%Y"))
        print('Температура: от ' + self.weather_dict['min_temp'] + ' до ' + self.weather_dict['max_temp'])
        print('Атмосферное давление: ' + self.weather_dict['pressures'] + ' Влажность: ' + self.weather_dict[
            'humidity'] + ' Скорость ветра: ' + self.weather_dict['wind_speed'] + ' км/ч')
        print(self.weather_dict['cloudiness'])
        if self.weather_dict['precipitation_hours'] and self.weather_dict['precipitation_hours'] < 4:
            precipitation_text = 'Возможен '
        if self.weather_dict['precipitation']:
            precipitation_text += self.weather_dict['precipitation']
        if precipitation_text:
            print(precipitation_text)
