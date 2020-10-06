from WeatherMaker import WeatherMaker
from ImageMaker import ImageMaker


class WeatherHandler():
    def __init__(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    weather = WeatherMaker()
    nn_weather = weather.darksky_parsing('56.3268,44.0058', '2019-11-14')  # NN
    # weather.darksky_parsing('29.5563,34.9525', '2020-10-5')   # Eilat ....
    image = ImageMaker()
    image.run()
