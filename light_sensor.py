from time import sleep


class LDR:
    def __init__(self, board_object, pin):
        self.__board = board_object
        self.pin = pin
        self.reading = 0
        self.setup()

    def setup(self):
        self.__board.GPIO.setup(self.pin, self.__board.GPIO.OUT)

    def sensor_read(self):
        self.__board.GPIO.output(self.pin, self.__board.GPIO.LOW)
        sleep(0.1)
        self.__board.GPIO.setup(self.pin, self.__board.GPIO.IN)
        if self.__board.GPIO.input(self.pin) == self.__board.GPIO.LOW:
            self.reading += 1
        return self.reading


#
# import time
# import RPi.GPIO as GPIO
#
# GPIO.setmode(GPIO.BCM)
#
#
# def rc_time(rc_pin):
#     reading = 0
#     GPIO.setup(rc_pin, GPIO.OUT)
#     GPIO.output(rc_pin, GPIO.LOW)
#     time.sleep(0.1)
#
#     GPIO.setup(rc_pin, GPIO.IN)
#     while GPIO.input(rc_pin) == GPIO.LOW:
#         reading += 1
#     return reading
#
# while True:
#     print(rc_time(24))
