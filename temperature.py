""""@property
def temperature_c(self):
    return self.temp

@temperature_c.setup
def temperature_c(self):
    self.temp = Value
    """


class Temperature:  # Takes sensehat instance and a mode of necessary
    def __init__(self, sense_object, mode="celsius"):
        # mode is automatically set to celsius as default
        self.sh = sense_object
        self.mode = mode

    def temperature_c(self):
        return self.sh.sense.get_temperature()
    # returns current temperature in celsius

    def temperature_f(self):
        t_celsius = self.sh.get_temperature()
        return t_celsius * 1.8 + 32
    # returns current temperature in fahrenheit

    def thermostat(self, mode):
        # bottle method in here to get the temperature from the slider
        return

if __name__ == "__main__":
    from board import Board
    from sensehat import _SenseHat
    rpi = Board()
    sh = _SenseHat(rpi)
    temptest = Temperature(sh)
    print(temptest.temperature_c())
