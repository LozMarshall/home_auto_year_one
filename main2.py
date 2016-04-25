from board import Board
from sensehat import _SenseHat
from led import LED
from rgbled import RGBLED
from temperature import Temperature
from time import sleep
from tkinter import *


class App:
    def __init__(self, master):
        frame = Frame(master)
        """
        frame.pack()

        self.button = Button(
            frame, text="quit", fg="red", height=100, width=50, command=frame.quit
        )

        self.button.pack(side=LEFT)

        self.hi_there = Button(
            frame, text="hello", height=100, width=50, command=self.say_hi
        )

        self.hi_there.pack(side=LEFT)
        """

        self.label = Label(
            master, text="item1"
        ).grid(row=0, pady=10, padx=10, sticky=W)

        self.label2 = Label(
            master, text="item2"
        ).grid(row=1, pady=10, padx=10, sticky=W)

        master.config(cursor="none")
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        master.overrideredirect(1)
        master.geometry("%dx%d+0+0" % (w, h))

    def say_hi(self):
        print("hello")


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
    print(sense.temp_c)
    print(sense.humidity)
    print(sense.pressure)
    sense.led_1(red)
    sleep(5)
    sense.led_1(blue)
    sleep(5)
    sense.clear()
    rpi.clean_up()


def sense_led(white, black):
    state = "off"
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if state == "on":
                        state = "off"
                    elif state == "off":
                        state = "on"

                if state == "on":
                    sense.led_all(white)
                    print("LED on")
                elif state == "off":
                    sense.led_all(black)
                    print("LED off")

    sense.clear()
    rpi.clean_up()


def compass():
    sense.magnetometer_on()
    while True:
        print(sense.sense.compass)


def get_temperature_demo():
    tempc = Temperature(sense)      # theoretically this should return the temperature in celsius from the sensehat
    print(tempc.temperature_c())    # it is untested however.

red = [255, 0, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
white = [255, 255, 255]
black = [0, 0, 0]

rpi = Board()
sense = _SenseHat(rpi)
root = Tk()

#root.config(cursor="none")

# make it cover the entire screen
#w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#root.overrideredirect(1)
#root.geometry("%dx%d+0+0" % (w, h))

app = App(root)

root.mainloop()
root.destroy()
#scsd


#sense_led(white, black)
#compass()



# sense_demo()
# led_on_demo() # calls led_on_demo function in main.py to turn on LED
# rgb_led_on_demo() # calls rgb_led_on_demo function in main.py to turn on red led then off and turn on white.
# get_temperature_demo() # demo of temperature get from the Temperature class
