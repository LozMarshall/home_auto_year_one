from time import sleep


class Buzzer:
    def __init__(self, board_object, pin):
        self.__board = board_object
        self.pin = pin
        self.setup()

    def setup(self):
        self.__board.GPIO.setup(self.pin, self.__board.GPIO.OUT)

    def buzz(self):
        self.__board.GPIO.output(self.pin, self.__board.GPIO.HIGH)
        sleep(0.2)
        self.__board.GPIO.output(self.pin, self.__board.GPIO.LOW)
