class RGBLED:
    def __init__(self, board_object, red, green, blue):
        self.GPIO = board_object
        self.red = red
        self.green = green
        self.blue = blue
        self.pins = [self.red, self.green, self.blue]

    def setup(self):
        for pin in self.pins:
            self.GPIO.setup(pin, self.GPIO.OUT)

    def red_turn_on(self):
        self.clear()
        self.GPIO.output(self.red, self.GPIO.HIGH)
        return "RED LED ON"

    def green_turn_on(self):
        self.clear()
        self.GPIO.output(self.green, self.GPIO.HIGH)
        return "GREEN LED ON"

    def blue_turn_on(self):
        self.clear()
        self.GPIO.output(self.blue, self.GPIO.HIGH)
        return "BLUE LED ON"

    def white_turn_on(self):
        self.clear()
        self.GPIO.output(self.red, self.GPIO.HIGH)
        self.GPIO.output(self.green, self.GPIO.HIGH)
        self.GPIO.output(self.blue, self.GPIO.HIGH)
        return "WHITE LED ON"

    def clear(self):
        for pin in self.pins:
            self.GPIO.output(pin, self.GPIO.LOW)

"""
if __name__ == "__name__":
    from board import Board
    from time import sleep
    rpi = Board()
    led = RGBLED(rpi, 18, 19, 20)
    led.red_turn_on()
    sleep(2)
    led.clear()
    led.white_turn_on()
    sleep(5)
    led.clear()
"""