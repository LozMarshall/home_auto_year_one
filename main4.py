from board import Board
from sensehat import _SenseHat
from rgbled import RGBLED
from led import LED
from pir import PIR
from buzzer import Buzzer

import tkinter as tk
from tkinter import ttk
import configparser
import os.path


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

        self.light_state = ''
        self.thermostat_temp = ''
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0
        self.red_scale_val = 0
        self.green_scale_val = 0
        self.blue_scale_val = 0
        print("Stating variables initialised")

        self.config = configparser.ConfigParser()
        self.config_manager()

        ##########COLUMN 0 START - INITIALISING LABELS#########
        self.label = tk.Label(self)
        self.label2 = tk.Label(self)
        self.label3 = tk.Label(self)
        self.label4 = tk.Label(self)
        self.label5 = tk.Label(self)
        self.label7 = tk.Label(self, text="lights: " + self.light_state)
        print("Left hand side statistic labels initialised")
        ##########COLUMN 0 END###########

        ##########COLUMN 1 START - INITIALISING LABELS#########
        self.label6 = tk.Label(self, text="Set thermostat temperature: ")
        self.label8 = tk.Label(self, text="Red: ")
        self.label9 = tk.Label(self, text="Green: ")
        self.label10 = tk.Label(self, text="Blue: ")
        print("Middle labels for thermostat and RGB initialised")
        ##########COLUMN 1 END###########

        ##########COLUMN 2 START - INITIALISING#########
        self.tempscale = tk.Scale(self, from_=10, to=30, length=200, orient="horizontal",
                                  command=self.thermostat_update())
        self.tempscale.set(self.thermostat_temp)
        print("Thermostat scale initialised")

        self.button_light = tk.Button(self, text="Lights on", width=25, anchor="w",
                                      command=lambda: self.light())
        print("'Turn on light' button initialised")

        self.red_scale = tk.Scale(self, from_=0, to=255, length=225, orient="horizontal",
                                  command=self.red_scale_update)
        self.red_scale.set(self.red_scale_val)
        print("Blue scale initialised and set to parameter from config file")

        self.green_scale = tk.Scale(self, from_=0, to=255, length=225, orient="horizontal",
                                    command=self.green_scale_update)
        self.green_scale.set(self.green_scale_val)
        print("Blue scale initialised and set to parameter from config file")

        self.blue_scale = tk.Scale(self, from_=0, to=255, length=225, orient="horizontal",
                                   command=self.blue_scale_update)
        self.blue_scale.set(self.blue_scale_val)
        print("Blue scale initialised and set to parameter from config file")
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
        self.update_pir_sensor()  # method called that runs and gets integrated into event handler

    def config_manager(self):
        cfg_file = open("config.ini", 'w')
        selector = "Default"

        if os.path.isfile('config.ini'):
            print(os.path.isfile('config.ini'))
            if not self.config.has_section('Profile_1'):
                for S in ('Default', 'Profile_1'):
                    self.config.add_section('%s' % S)
                    self.config.set('%s' % S, 'thermostat_temp', '20')
                    self.config.set('%s' % S, 'light_status', 'off')
                    self.config.set('%s' % S, 'red', '255')
                    self.config.set('%s' % S, 'green', '255')
                    self.config.set('%s' % S, 'blue', '255')
                    print("looping in the config setup")
                self.config.write(cfg_file)
                cfg_file.close()
            else:
                selector = "Profile_1"

        print("updating the variables")
        self.thermostat_temp = int(self.config['%s' % selector]['thermostat_temp'])
        print("thermostat temp input: " + str(self.thermostat_temp))
        self.light_state = self.config['%s' % selector]['light_status']
        self.red_scale_val = int(self.config['%s' % selector]['red'])
        self.green_scale_val = int(self.config['%s' % selector]['green'])
        self.blue_scale_val = int(self.config['%s' % selector]['blue'])

    # update sensors method is run as an event every 0.5 seconds and updating variables within the class
    # method is called at the end of the HomePage initialisation, then is run by the event handler
    def update_sensors(self):
        self.temperature = round(sense.temp_c, 1)
        self.pressure = round(sense.pressure, 2)
        self.humidity = round(sense.humidity, 1)
        self.thermostat_temp = self.tempscale.get()
        self.red_scale_val = self.red_scale.get()

        print("update sensors method run - refreshing variables every 0.5s")

        self.after(500, self.update_sensors)

    # update interface method is run as an event after being called at the end of the initialisation
    # the method runs every 1.2 seconds so that the interface isn't updating at too high of a rate
    def update_interface(self):
        self.label.configure(text="temperature: " + str(self.temperature) + " \u2103")
        self.label2.configure(text="pressure: " + str(self.pressure) + " mbar")
        self.label3.configure(text="humidity: " + str(self.humidity) + " %")

        print("update interface method run - refreshing temp, pressure and humidity variable every 1.2s")

        self.after(1200, self.update_interface)  # function to run method in the event handler

    def update_pir_sensor(self):
        pir = PIR(rpi, 6)  # passing in board object and pin number of the pir
        buzz = Buzzer(rpi, 20)
        if pir.motion_detect():
            buzz.buzz()
        self.after(1000, self.update_pir_sensor)

    # thermostat update method is called when the SET TEMPERATURE slider is toggled
    def thermostat_update(self):
        self.label4.configure(text="thermostat temperature: " + str(self.thermostat_temp) + " \u2103")
        self.label5.configure(text="heating: " + str(heating(self.temperature, self.thermostat_temp)))

        self.after(500, self.thermostat_update)  # function to run method in the event handler

    # light method is called from toggling the turn lights on button
    # the default state of the lights is off, so when the program runs the state changes to on and runs the methods
    # for the sense-hat LED matrix and the rpi GPIO rgbLED method
    def light(self):
        if self.light_state == "off":
            self.light_state = "on"
            self.sense_led(self.light_state)
            gpi_led(self.light_state, "green")
            # if the light state is off at the if statement, it is changed to on and then runs the method for sense-hat
            # and GPIO LED's to turn on

        elif self.light_state == "on":
            self.light_state = "off"
            self.sense_led(self.light_state)
            gpi_led(self.light_state, "green")
            # if the light state is on when the button is pressed again, the state is changed to off and then runs the
            # sense-hat and gpi LED's to turn off

        if self.light_state == "off":
            self.button_light.configure(text="Lights on")
            self.label7.configure(text="lights: " + self.light_state)
            # if the light state is off, change the text on the button to lights on and change the status of the light
            # on the left hand side "lights: off"

        elif self.light_state == "on":
            self.button_light.configure(text="Lights off")
            self.label7.configure(text="lights: " + self.light_state)

    def red_scale_update(self, val):
        self.red_scale_val = val
        self.sense_led(self.light_state)

    def green_scale_update(self, val):
        self.green_scale_val = val
        self.sense_led(self.light_state)

    def blue_scale_update(self, val):
        self.blue_scale_val = val
        self.sense_led(self.light_state)

    def sense_led(self, state):
        colour = [int(self.red_scale_val), int(self.green_scale_val), int(self.blue_scale_val)]
        black = [0, 0, 0]

        if state == "off":
            sense.led_all(black)
        elif state == "on":
            sense.led_all(colour)

    def close(self):
        sense.clear()
        rpi.clean_up()
        # call save method for variables
        self.config_save()
        self.quit()

    def config_save(self):
        cfg_file = open("config.ini", 'w')

        self.config.set('Profile_1', 'thermostat_temp', '%s' % self.thermostat_temp)
        self.config.set('Profile_1', 'light_status', '%s' % self.light_state)
        self.config.set('Profile_1', 'red', '%s' % self.red_scale_val)
        self.config.set('Profile_1', 'green', '%s' % self.green_scale_val)
        self.config.set('Profile_1', 'blue', '%s' % self.blue_scale_val)

        self.config.write(cfg_file)
        cfg_file.close()


def gpi_led(state, colour):
    red = 13
    green = 19
    blue = 26
    led = RGBLED(rpi, red, green, blue)

    if state == "on":
        if colour == "red":
            led.red_turn_on()
        if colour == "green":
            led.green_turn_on()
        if colour == "blue":
            led.blue_turn_on()
    elif state == "off":
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

# buzzer pin = 20
# pir pin = 6
