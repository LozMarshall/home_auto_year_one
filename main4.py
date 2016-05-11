from board import Board
from sensehat import _SenseHat
import tkinter as tk
from tkinter import ttk


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
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

        number = 24

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
        ##########COLUMN 1 END###########

        ##########COLUMN 2 START - INITIALISING#########
        self.tempscale = tk.Scale(self, from_=10, to=30, orient="horizontal")
        self.tempscale.set(number)

        self.button_light = tk.Button(self, text="Lights on", width=25, anchor="w",
                                      command=lambda: self.light())
        ##########COLUMN 2 END#########

        ##########COLUMN 100 START#####
        # button_page = tk.Button(self, text="Help", anchor="w",
        #                        command=lambda: controller.show_frame(HelpPage))
        button_page = ttk.Button(self, text="Help",
                                 command=lambda: controller.show_frame(HelpPage))
        button_quit = ttk.Button(self, text="quit", command=self.quit)
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

        self.tempscale.grid(row=0, column=2, pady=10, padx=10, sticky="W")

        self.button_light.grid(row=1, column=2, pady=10, padx=10, sticky="W")

        button_page.grid(row=14, column=3, pady=10, padx=10, sticky="se")
        button_quit.grid(row=15, column=3, pady=10, padx=10, sticky="se")

        self.update_sensors()
        self.update_interface()
        self.update_sensing()

    def update_sensors(self):
        sense = _SenseHat(rpi)
        self.temperature = round(sense.temp_c, 1)
        self.pressure = round(sense.pressure, 2)
        self.humidity = round(sense.humidity, 1)

        self.after(250, self.update_sensors())

    def update_interface(self):
        # thermostat_temp = self.tempscale.get()

        self.label.configure(text="temperature: " + str(self.temperature) + " \u2103")
        self.label2.configure(text="pressure: " + str(round(self.pressure, 2)) + " mbar")
        self.label3.configure(text="humidity: " + str(round(self.humidity, 1)) + " %")
        ##### self.label4.configure(text="thermostat temperature: " + str(thermostat_temp) + " \u2103")
        ##### self.label5.configure(text="heating: " + str(heating(temperature, thermostat_temp)))

        self.after(500, self.update_interface)  # METHOD UPDATES EVERY HALF SECOND WITHIN EVENT HANDLER
                                                # THIS IS NOT PROCEDURAL ANYTHING ELSE CAN RUN TOO

    def update_sensing(self):
        self.thermostat_update()

        self.after(200, self.update_sensing)

    def light(self):
        self.light_state = sense_led(self.light_state)

        if self.light_state == "off":
            self.button_light.configure(text="Lights on")
            self.label7.configure(text="lights: " + self.sense)
        elif self.sense == "on":
            self.button_light.configure(text="Lights off")
            self.label7.configure(text="lights: " + self.sense)

    def thermostat_update(self):
        sense = _SenseHat(rpi)

        temperature = round(sense.temp_c, 1)
        thermostat_temp = self.tempscale.get()

        self.label4.configure(text="thermostat temperature: " + str(thermostat_temp) + " \u2103")
        self.label5.configure(text="heating: " + str(heating(temperature, thermostat_temp)))


def sense_led(state):
    sense = _SenseHat(rpi)
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


def heating(temperature, thermostat_temp):
    sense = _SenseHat(rpi)
    red = [255, 0, 0]
    black = [0, 0, 0]
    if thermostat_temp <= temperature:
        sense.led_2(black)
        return "OFF"
    else:
        sense.led_2(red)
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
app = App()

app.mainloop()
