from board import Board
from sensehat import _SenseHat
from rgbled import RGBLED
from led import LED
import tkinter as tk
from tkinter import ttk
from time import sleep


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.config(cursor="none")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (w, h))

        container = tk.Frame(self)

        # container.pack(side="top", fill="both", expand=True)
        container.grid(rowspan=5, columnspan=2, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, HelpPage):
            frame = F(container, self)

            self.frames[F] = frame # instances of the classes for homepage and helppage

            frame.grid(row=0, column=0, sticky="nsew")
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent='', controller=''):
        tk.Frame.__init__(self, parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        self.light_state = "off"
        self.thermostat_temp = 24
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.red_scale_val = 0
        self.green_scale_val = 0
        self.blue_scale_val = 0

        ##########COLUMN 0 START - INITIALISING LABELS#########
        self.label = tk.Label(self)
        self.label2 = tk.Label(self)
        self.label3 = tk.Label(self)
        self.label4 = tk.Label(self)
        self.label5 = tk.Label(self)
        self.label7 = tk.Label(self, text="lights: " + self.light_state)
        ##########COLUMN 0 END###########

        ##########COLUMN 1 START - INITIALISING LABELS#########
        self.label6 = tk.Label(self, text="Set thermostat temperature: ")
        self.label8 = tk.Label(self, text="Red: ")
        self.label9 = tk.Label(self, text="Green: ")
        self.label10 = tk.Label(self, text="Blue: ")
        ##########COLUMN 1 END###########

        ##########COLUMN 2 START - INITIALISING#########
        self.tempscale = tk.Scale(self, from_=10, to=30, length=200, orient="horizontal",
                                  command=self.thermostat_update())
        # self.tempscale.set(self.thermostat_temp) #use this to load temperature previously from the home auto

        self.button_light = tk.Button(self, text="Lights on", width=25, anchor="w",
                                      command=lambda: self.light())
        self.red_scale = tk.Scale(self, from_=0, to=255, length=225, orient="horizontal",
                                  command=self.red_scale_update)
        self.green_scale = tk.Scale(self, from_=0, to=255, length=225, orient="horizontal",
                                    command=self.green_scale_update)
        self.blue_scale = tk.Scale(self, from_=0, to=255, length=225, orient="horizontal",
                                   command=self.blue_scale_update)
        ##########COLUMN 2 END#########

        ##########COLUMN 100 START#####
        # button_page = tk.Button(self, text="Help", anchor="w",
        #                        command=lambda: controller.show_frame(HelpPage))
        button_page = ttk.Button(self, text="Help",
                                 command=lambda: controller.show_frame(HelpPage))
        button_quit = ttk.Button(self, text="quit", command=self.close)
        ##########COLUMN 100 END#######

        ##########COLUMN 0 START - LABEL SETUP#########
        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.label2.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.label3.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.label4.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.label5.grid(row=4, column=0, pady=10, padx=10, sticky="w")
        self.label7.grid(row=5, column=0, pady=10, padx=10, sticky="w")
        ##########COLUMN 0 END#########################

        self.label6.grid(row=0, column=1, pady=10, padx=10, sticky="SW")
        self.label8.grid(row=2, column=1, pady=10, padx=10, sticky="E")
        self.label9.grid(row=3, column=1, pady=10, padx=10, sticky="E")
        self.label10.grid(row=4, column=1, pady=10, padx=10, sticky="E")

        self.tempscale.grid(row=0, column=2, pady=10, padx=10, sticky="W")

        self.button_light.grid(row=1, column=2, pady=10, padx=10, sticky="W")

        self.red_scale.grid(row=2, column=2, pady=10, padx=10, sticky="E")
        self.green_scale.grid(row=3, column=2, pady=10, padx=10, sticky="E")
        self.blue_scale.grid(row=4, column=2, pady=10, padx=10, sticky="E")

        button_page.grid(row=14, column=3, pady=10, padx=10, sticky="se")
        button_quit.grid(row=15, column=3, pady=10, padx=10, sticky="se")

        self.update_sensors()  # method that will become events
        self.update_interface()  # method that will become events

    def update_sensors(self):
        self.temperature = round(sense.temp_c, 1)
        self.pressure = round(sense.pressure, 2)
        self.humidity = round(sense.humidity, 1)
        self.thermostat_temp = self.tempscale.get()
        self.red_scale_val = self.red_scale.get()

        self.after(500, self.update_sensors)

    def update_interface(self):

        self.label.configure(text="temperature: " + str(self.temperature) + " \u2103")
        self.label2.configure(text="pressure: " + str(self.pressure) + " mbar")
        self.label3.configure(text="humidity: " + str(self.humidity) + " %")
        # self.label4.configure(text="thermostat temperature: " + str(self.thermostat_temp) + " \u2103")
        # self.label5.configure(text="heating: " + str(heating(self.temperature, self.thermostat_temp)))

        self.after(1200, self.update_interface)  # METHOD UPDATES EVERY HALF SECOND WITHIN EVENT HANDLER
                                                # THIS IS NOT PROCEDURAL ANYTHING ELSE CAN RUN TOO

    def thermostat_update(self):
        self.label4.configure(text="thermostat temperature: " + str(self.thermostat_temp) + " \u2103")
        self.label5.configure(text="heating: " + str(heating(self.temperature, self.thermostat_temp)))

        self.after(500, self.thermostat_update)

    def light(self):
        if self.light_state == "off":
            # sense_led(self.light_state)
            gpi_led(self.light_state, "green")
            self.light_state = "on"
        elif self.light_state == "on":
            # sense_led(self.light_state)
            gpi_led(self.light_state, "green")
            self.light_state = "off"

        if self.light_state == "off":
            self.button_light.configure(text="Lights on")
            self.label7.configure(text="lights: " + self.light_state)
        elif self.light_state == "on":
            self.button_light.configure(text="Lights off")
            self.label7.configure(text="lights: " + self.light_state)

    def red_scale_update(self, val):
        self.red_scale_val = val
        # sense.led_all([self.red_scale_val, self.green_scale_val, self.blue_scale_val])
        print("red update run " + str(self.red_scale_val))

    def green_scale_update(self, val):
        self.green_scale_val = val
        # sense_led(self.light_state)
        print("green update run " + str(self.green_scale_val))

    def blue_scale_update(self, val):
        self.blue_scale_val = val
        # sense_led(self.light_state)
        print("blue update run " + str(self.blue_scale_val))

    def close(self):
        sense.clear()
        rpi.clean_up()
        self.quit()


def gpi_led(state, colour):
    red = 13
    green = 19
    blue = 26
    led = RGBLED(rpi, red, green, blue)

    if state == "off":
        if colour == "red":
            led.red_turn_on()
        if colour == "green":
            led.green_turn_on()
        if colour == "blue":
            led.blue_turn_on()
    elif state == "on":
        led.clear()


def sense_led1(state):
    # sense = _SenseHat(rpi)
    white = [255, 255, 255]
    black = [0, 0, 0]

    if state == "on":
        sense.led_1(black)
        print("LED off")
        return "off"
    elif state == "off":
        sense.led_1(white)
        print("LED on")
        return "on"


def sense_led(state):
    # sense = _SenseHat(rpi)
    white = [255, 255, 255]
    black = [0, 0, 0]

    if state == "on":
        sense.led_1(black)
    elif state == "off":
        sense.led_1(white)


def heating(temperature, thermostat_temp):
    # red = [255, 0, 0]
    # black = [0, 0, 0]

    pin = 16
    led = LED(rpi, pin)
    if thermostat_temp <= temperature:
        # sense.led_2(black)
        led.turn_off()
        return "OFF"
    else:
        # sense.led_2(red)
        led.turn_on()
        return "ON"


class HelpPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="help page for all the penises: ")

        button_page = tk.Button(self, text="Home", anchor="sw",
                                command=lambda: controller.show_frame(HomePage))
        button_quit = tk.Button(self, text="quit", anchor="sw", command=self.quit)

        label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        button_page.grid(row=3, column=1, pady=10, padx=10, sticky="se")
        button_quit.grid(row=4, column=1, pady=10, padx=10, sticky="se")


rpi = Board()
sense = _SenseHat(rpi)
app = App()

app.mainloop()
