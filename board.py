import RPi.GPIO


class Board:
    def __init__(self):
        self.GPIO = RPi.GPIO
        self.setup()

    def setup(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)

    def clean_up(self):
        self.GPIO.cleanup()
