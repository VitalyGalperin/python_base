import os
import cv2

FONT_COLOR = (20, 20, 0)


class ImageMaker:
    def __init__(self, weather_dict, recipient_file='card.jpg', source_file='blank.jpg', image_dir='image_data'):
        self.weather_dict = weather_dict
        self.image_dir = image_dir
        self.source_file = source_file
        self.recipient_file = recipient_file
        self.source_full_path = self.recipient_full_path = ''
        self.image = None

    def run(self):
        self.path_create()
        self.card_create()

    def path_create(self):
        self.source_full_path = os.path.join(os.getcwd(), self.image_dir, self.source_file)
        self.recipient_full_path = os.path.join(os.getcwd(), self.image_dir, self.recipient_file)

    def card_create(self):
        self.image = cv2.imread(self.source_full_path)
        if self.image is None:
            return False
        image_size = self.image.shape
        line_step = int(image_size[0] / 255)

        for i in range(0, 256):
            # cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
            #          color=(255-i/2, 255-i/2, 255-i/2),
            #          thickness=int(image_size[0]/255))  #gray

            cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
                     color=(255, 255 - i, 255 - i),
                     thickness=int(image_size[0] / 255))  # blue

            # cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
            #          color=(255 - i, 255, 255),
            #          thickness=int(image_size[0] / 255)) #yellow

            # cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
            #          color=(255, 255, 255 - i),
            #          thickness=int(image_size[0] / 255)) #cyan

        icon_image = cv2.imread(os.path.join(os.getcwd(), self.image_dir, 'sun.jpg'))
        icon_size = icon_image.shape
        self.image[0:icon_size[0], 400: 400 + icon_size[1]] = icon_image

        # cv2.imshow("Image", self.image)
        # cv2.waitKey(0)
        print_date = self.weather_dict['date'].strftime("%d/%m/%Y")

        cv2.putText(self.image, self.weather_dict['location_name'], (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR,
                    2)
        cv2.putText(self.image, self.weather_dict['coordinates'], (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, FONT_COLOR,
                    2)
        cv2.putText(self.image, 'Дата: ' + print_date, (20, 80), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'Температура: ', (20, 120), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['min_temp'], (20, 150), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['max_temp'], (115, 150), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, 'Давление: ', (20, 190), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['pressures'], (180, 190), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'Влажность: ', (20, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['humidity'], (190, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, ' : ', (20, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'Ветер: ', (290, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, 'км/ч', (300, 244), cv2.FONT_HERSHEY_COMPLEX, 0.5, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['wind_speed'], (390, 230), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)

        cv2.imwrite(self.recipient_full_path, self.image)

# image = ImageMaker()
# image.run()
