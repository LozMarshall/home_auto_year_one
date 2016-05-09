from board import Board
from sensehat import _SenseHat
import tkinter as tk
from time import sleep


def update_method(cont):
    sense = _SenseHat(rpi) # create instance of sensehat
    temperature = round(sense.temp_c, 1) # pull temperature method from sensehat
    thermostat_temp = cont.tempscale.get() # get thermostat temp from GUI scale

    # begin  of functions to post updates to labels
    cont.label.configure(text="temperature: " + str(temperature) + " \u2103")
    cont.label2.configure(text="pressure: " + str(round(sense.pressure, 2)) + " mbar")
    cont.label3.configure(text="humidity: " + str(round(sense.humidity, 1)) + " %")
    cont.label4.configure(text="thermostat temperature: " + str(thermostat_temp) + " \u2103")
    cont.label5.configure(text="heating: " + str(heating(temperature, thermostat_temp)))
    # end of functions to post updates to labels

    # begin of diagnostics of what is going on in this method
    print("update method run")
    print(sense.humidity)
    print(sense.pressure)
    print(thermostat_temp)
    print(cont.label.cget("text"))
    # end of diagnostics of what is going on in this method


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

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

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

        self.label = tk.Label(self, text="temperature: ")
        self.label2 = tk.Label(self, text="pressure: ")
        self.label3 = tk.Label(self, text="humidity: ")
        self.label4 = tk.Label(self, text="thermostat temperature: ")
        self.label5 = tk.Label(self, text="heating: ")

        self.label6 = tk.Label(self, text="Set thermostat temperature: ")

        number = 24
        self.tempscale = tk.Scale(self, from_=10, to=30, orient="horizontal")
        self.tempscale.set(number)

        self.button_light = tk.Button(self, text="Lights on", height=5, width=50, anchor="w")

        button_page = tk.Button(self, text="Help", anchor="w",
                                command=lambda: controller.show_frame(HelpPage))
        button_quit = tk.Button(self, text="quit", anchor="w", command=self.quit)

        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.label2.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.label3.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.label4.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.label5.grid(row=4, column=0, pady=10, padx=10, sticky="w")

        self.label6.grid(row=0, column=1, pady=10, padx=10, sticky="SW")

        self.tempscale.grid(row=0, column=2, pady=10, padx=10, sticky="W")

        self.button_light.grid(row=1, column=2, pady=10, padx=10, sticky="W")

        button_page.grid(row=14, column=3, pady=10, padx=10, sticky="se")
        button_quit.grid(row=15, column=3, pady=10, padx=10, sticky="se")

        self.update_interface()
        self.update_sensing()

    def update_interface(self):
        sense = _SenseHat(rpi)
        temperature = round(sense.temp_c, 1)
        thermostat_temp = self.tempscale.get()

        self.label.configure(text="temperature: " + str(temperature) + " \u2103")
        self.label2.configure(text="pressure: " + str(round(sense.pressure, 2)) + " mbar")
        self.label3.configure(text="humidity: " + str(round(sense.humidity, 1)) + " %")
        self.label4.configure(text="thermostat temperature: " + str(thermostat_temp) + " \u2103")
        self.label5.configure(text="heating: " + str(heating(temperature, thermostat_temp)))
        print("doing it")

        self.after(500, self.update_interface)

    def update_sensing(self):
        print("updating at the same time")

        self.after(500, self.update_sensing)


def heating(temperature, thermostat_temp):

    if thermostat_temp <= temperature:
        return "OFF"
    else:
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
