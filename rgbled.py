class RGBLED:
    def __init__(self, board_object, red, green, blue):
        self.board = board_object
        self.red = red
        self.green = green
        self.blue = blue
        self.pins = [self.red, self.green, self.blue]

    def setup(self):
        for pin in self.pins:
            self.board.GPIO.setup(pin, self.board.GPIO.OUT)

    def red_turn_on(self):
        self.clear()
        self.board.GPIO.output(self.red, self.board.GPIO.HIGH)
        # return "RED LED ON"

    def green_turn_on(self):
        self.clear()
        self.board.GPIO.output(self.green, self.board.GPIO.HIGH)
        # return "GREEN LED ON"

    def blue_turn_on(self):
        self.clear()
        self.board.GPIO.output(self.blue, self.board.GPIO.HIGH)
        # return "BLUE LED ON"

    def white_turn_on(self):
        self.clear()
        self.board.GPIO.output(self.red, self.board.GPIO.HIGH)
        self.board.GPIO.output(self.green, self.board.GPIO.HIGH)
        self.board.GPIO.output(self.blue, self.board.GPIO.HIGH)
        # return "WHITE LED ON"

    def clear(self):
        for pin in self.pins:
            self.board.GPIO.output(pin, self.board.GPIO.LOW)
