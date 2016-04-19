class LED:
    def __init__(self, board_object, pin):
        self.__board = board_object
        self.pin = pin
        self.setup()

    def setup(self):
        self.__board.GPIO.setup(self.pin, self.__board.GPIO.OUT)

    def turn_on(self):
        self.__board.GPIO.output(self.pin, self.__board.GPIO.HIGH)

    def turn_off(self):
        self.__board.GPIO.output(self.pin, self.__board.GPIO.LOW)

"""
#TEST PURPOSES ONLY#
if __name__ == "__name__":
    from board import Board
    from time import sleep
    rpi = Board()
    led = Led(rpi, 18)
    led.turn_on()
    sleep(2)
    led.turn_off()
"""
