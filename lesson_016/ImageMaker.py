# -*- coding: utf-8 -*-

import os
import cv2

from set import BLANK_FILE, RESULT_FILE, IMAGE_DIR, CARD_DIR, RAIN_ICON, SNOW_ICON, DRIZZLE_ICON, CLOUDY_ICON, \
    OVERCAST_ICON, FOGGY_ICON, SUNNY_ICON, SLEET_ICON, FONT_COLOR, YELLOW, CYAN, BLUE, GRAY


class ImageMaker:
    def __init__(self, weather_dict):
        self.weather_dict = weather_dict
        self.image_dir = IMAGE_DIR
        self.card_dir = CARD_DIR
        self.source_file = BLANK_FILE
        self.recipient_file = RESULT_FILE
        self.source_full_path = self.recipient_full_path = ''
        self.image = None

    def run(self):
        self.path_create()
        self.card_create()

    def path_create(self):
        self.source_full_path = os.path.join(os.getcwd(), self.image_dir, self.source_file)
        if not os.path.exists(self.card_dir):
            os.mkdir(self.card_dir)
        self.recipient_full_path = os.path.join(os.getcwd(), self.card_dir, self.recipient_file)

    def card_create(self):
        self.image = cv2.imread(self.source_full_path)
        if self.image is None:
            return False
        image_size = self.image.shape
        line_step = int(image_size[0] / 255)

        icon = self.gradient_and_icon_choose(image_size, line_step)

        icon_image = cv2.imread(os.path.join(os.getcwd(), self.image_dir, icon))
        icon_size = icon_image.shape
        self.image[0:icon_size[0], 400: 400 + icon_size[1]] = icon_image

        print_date = self.weather_dict['date'].strftime("%d/%m/%Y")

        self.make_legend(print_date)
        cv2.imwrite(self.recipient_full_path, self.image)
        # TODO Похоже что название открыток никак не изменяется
        # TODO и каждая новая просто перезаписывает старую
        # TODO Это не очень функционально
        # TODO я бы посоветовал использовать дату в качестве названия (можно с городом)
        # Вывод открытки на экран
        # cv2.imshow("Image", self.image)
        # cv2.waitKey(0)

    def gradient_and_icon_choose(self, image_size, line_step):
        icon = SUNNY_ICON
        if self.weather_dict['cloudiness'].find('Дождь') != -1 or (
                self.weather_dict['precipitation'].find('Дождь') != -1 and
                self.weather_dict['precipitation_hours'] and self.weather_dict['precipitation_hours'] > 4):
            self.gradient(image_size, line_step, BLUE)
            icon = RAIN_ICON
        elif self.weather_dict['cloudiness'].find('Снег') != -1 or (
                self.weather_dict['precipitation'].find('Снег') != -1 and
                self.weather_dict['precipitation_hours'] and self.weather_dict['precipitation_hours'] > 4):
            self.gradient(image_size, line_step, CYAN)
            if self.weather_dict['cloudiness'] == 'Мокрый Снег':
                icon = SLEET_ICON
            else:
                icon = SNOW_ICON
        elif self.weather_dict['cloudiness'].find('Морось') != -1:
            self.gradient(image_size, line_step, BLUE)
            icon = DRIZZLE_ICON
        elif self.weather_dict['cloudiness'].find('Облачно') != -1:
            self.gradient(image_size, line_step, GRAY)
            icon = CLOUDY_ICON
        elif self.weather_dict['cloudiness'].find('Пасмурно') != -1:
            self.gradient(image_size, line_step, GRAY)
            icon = OVERCAST_ICON
        elif self.weather_dict['cloudiness'].find('Туман') != -1:
            self.gradient(image_size, line_step, YELLOW)
            icon = FOGGY_ICON
        elif self.weather_dict['cloudiness'].find('Солнечно') != -1:
            self.gradient(image_size, line_step, YELLOW)
            icon = SUNNY_ICON
        return icon

    def gradient(self, image_size, line_step, color_tuple):
        for i in range(0, 257):
            cv2.line(self.image, pt1=(0, 256 - i * line_step), pt2=(image_size[1], 256 - i * line_step),
                     color=(255 - i * color_tuple[0], 255 - i * color_tuple[1], 255 - i * color_tuple[2]),
                     thickness=int(image_size[0] / 255))

    def make_legend(self, print_date):
        cv2.putText(self.image, self.weather_dict['location_name'], (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR,
                    2)
        cv2.putText(self.image, self.weather_dict['coordinates'], (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, FONT_COLOR,
                    2)
        cv2.putText(self.image, 'Дата: ' + print_date, (20, 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'Температура: ', (20, 120), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['min_temp'], (20, 150), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['max_temp'], (115, 150), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, 'Давление: ', (20, 190), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['pressures'], (180, 190), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR,
                    2)
        cv2.putText(self.image, 'Влажность: ', (20, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['humidity'], (190, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, ' : ', (20, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'Ветер: ', (290, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'км/ч', (300, 244), cv2.FONT_HERSHEY_COMPLEX, 0.5, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['wind_speed'], (390, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR,
                    2)

# image = ImageMaker()
# image.run()
