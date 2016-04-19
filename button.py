class Button:
    def __init__(self, board_object, pin):
        self.GPIO = board_object
        self.pin = pin
        self.setup()

    def setup(self):
        self.GPIO.setup(self.pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        # function sets up the button

    def button_state(self):
        return self.GPIO.input(self.pin)
        # returns false for button pressed, true for not pressed
