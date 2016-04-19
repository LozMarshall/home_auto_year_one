from sense_hat import SenseHat


class _SenseHat:
    def __init__(self, board_object, colour=""):
        self.board = board_object
        self.colour = colour
        self.sense = SenseHat()
        self.temp_c = self.__temp_c()
        self.pressure = self.__pressure()
        self.humidity = self.__humidity()

    def __temp_c(self):
        return (self.sense.temp + self.sense.get_temperature_from_humidity() + self.sense.get_temperature_from_pressure())/3

    def __pressure(self):
        return self.sense.pressure

    def __humidity(self):
        return self.sense.humidity

    def led_all(self, colour):
        lcd = []
        for i in range(0, 64):
            lcd.append(colour)
        self.sense.set_pixels(lcd)

    def led_1(self, colour):
        self.sense.set_pixel(0, 0, colour)
        self.sense.set_pixel(0, 1, colour)
        self.sense.set_pixel(1, 0, colour)
        self.sense.set_pixel(1, 1, colour)

    def led_2(self, colour):
        self.sense.set_pixel(2, 2, colour)
        self.sense.set_pixel(2, 3, colour)
        self.sense.set_pixel(3, 2, colour)
        self.sense.set_pixel(3, 3, colour)

    def led_3(self, colour):
        self.sense.set_pixel(4, 4, colour)
        self.sense.set_pixel(4, 5, colour)
        self.sense.set_pixel(5, 4, colour)
        self.sense.set_pixel(5, 5, colour)

    def led_4(self, colour):
        self.sense.set_pixel(6, 6, colour)
        self.sense.set_pixel(6, 7, colour)
        self.sense.set_pixel(7, 6, colour)
        self.sense.set_pixel(7, 7, colour)

    def clear(self):
        self.sense.clear()

"""
if __name__ == "__main__":
    from board import Board
    from time import sleep
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    white = [255, 255, 255]
    rpi = Board()
    sh = _SenseHat(rpi)
    print(sh.temp_c)
    print(sh.humidity)
    print(sh.pressure)
    sh.led_1(red)
    sleep(5)
    sh.led_1(blue)
    sleep(5)
    sh.clear()
    rpi.clean_up()
"""

