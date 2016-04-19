from board import Board
from sensehat import _SenseHat
from led import LED
from rgbled import RGBLED
from temperature import Temperature
from time import sleep
from msvcrt import getch


def led_on_demo():
    pin_number = 18  # edit pin number
    led = LED(rpi, pin_number)
    led.turn_on()
    sleep(2)
    led.turn_off()


def rgb_led_on_demo():
    pin1 = 18
    pin2 = 19
    pin3 = 20
    led = RGBLED(rpi, pin1, pin2, pin3)
    led.red_turn_on()
    sleep(2)
    led.clear()
    led.white_turn_on()
    sleep(5)
    led.clear()


def sense_demo():
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    white = [255, 255, 255]
    print(sense.temp_c)
    print(sense.humidity)
    print(sense.pressure)
    sense.led_1(red)
    sleep(5)
    sense.led_1(blue)
    sleep(5)
    sense.clear()
    rpi.clean_up()


def sense_led():
    white = [255, 255, 255]
    sense.led_all(white)
    sleep(5)
    while True:
        key = getch()
        print("key pressed: " + key)
    sense.clear()
    rpi.clean_up()


def get_temperature_demo():
    tempc = Temperature(sense)      # theoretically this should return the temperature in celsius from the sensehat
    print(tempc.temperature_c())    # it is untested however.


rpi = Board()
sense = _SenseHat(rpi)
sense_led()


# sense_demo()
# led_on_demo() # calls led_on_demo function in main.py to turn on LED
# rgb_led_on_demo() # calls rgb_led_on_demo function in main.py to turn on red led then off and turn on white.
# get_temperature_demo() # demo of temperature get from the Temperature class
