class PIR:
    def __init__(self, board_object, pin):
        self.__board = board_object
        self.pin = pin
        self.setup()

    def setup(self):
        self.__board.GPIO.setup(self.pin, self.__board.GPIO.IN)

    def motion_detect(self):
        if self.__board.GPIO.input(self.pin):
            return True

