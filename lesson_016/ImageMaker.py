import os
import cv2


class ImageMaker:
    def __init__(self, recipient_file='card.jpg', source_file='blank.jpg', image_dir='image_data'):
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

        cv2.putText(self.image, "Здрасте", (20, 20), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
        # cv2.imshow("Image", self.image)
        # cv2.waitKey(0)
        cv2.imwrite(self.recipient_path, self.image)


image = ImageMaker()
image.run()
