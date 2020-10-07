import os
import cv2

FONT_COLOR = (20, 20, 0)


class ImageMaker:
    def __init__(self, weather_dict, recipient_file='card.jpg', source_file='blank.jpg', image_dir='image_data'):
        self.weather_dict = weather_dict
        self.image_dir = image_dir
        self.source_file = source_file
        self.recipient_file = recipient_file
        self.source_path = self.recipient_path = ''
        self.image = None

    def run(self):
        self.path_maker()
        self.card_maker()

    def path_maker(self):
        self.source_path = os.path.join(os.getcwd(), self.image_dir, self.source_file)
        self.recipient_path = os.path.join(os.getcwd(), self.image_dir, self.recipient_file)

    def card_maker(self):
        self.image = cv2.imread(self.source_path)
        color = (255, 255, 0)
        image_size = self.image.shape
        line_step = int(image_size[0]/255)
        for i in range(0, 256):
            # cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
            #          color=(255-i/2, 255-i/2, 255-i/2),
            #          thickness=int(image_size[0]/255))  #gray

            cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
                     color=(255, 255 - i, 255 - i),
                     thickness=int(image_size[0] / 255)) #blue

            # cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
            #          color=(255 - i, 255, 255),
            #          thickness=int(image_size[0] / 255)) #yellow

            # cv2.line(self.image, pt1=(0, i * line_step), pt2=(image_size[1], i * line_step),
            #          color=(255, 255, 255 - i),
            #          thickness=int(image_size[0] / 255)) #cyan

        cv2.putText(self.image, self.weather_dict['location_name'], (20, 30), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['coordinates'], (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['date'], (340, 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['max_temp'], (150, 130), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        cv2.putText(self.image, self.weather_dict['min_temp'], (60, 130), cv2.FONT_HERSHEY_COMPLEX, 0.9, FONT_COLOR, 2)
        # cv2.imshow("Image", self.image)
        # cv2.waitKey(0)
        cv2.imwrite(self.recipient_path, self.image)


# image = ImageMaker()
# image.run()
