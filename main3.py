from board import Board
from sensehat import _SenseHat
from temperature import Temperature
import tkinter as tk


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

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, HelpPage):
            frame = F(container, self)
            print("break point 4")
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)
        print("break point 1")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="temperature: ")
        self.label2 = tk.Label(self, text="pressure: ")
        self.label3 = tk.Label(self, text="humidity: ")
        self.label4 = tk.Label(self, text="thermostat: ")
        self.label5 = tk.Label(self, text="heating: ")

        button_page = tk.Button(self, text="Help", anchor="sw",
                                command=lambda: controller.show_frame(HelpPage))
        button_quit = tk.Button(self, text="quit", anchor="sw", command=self.quit)

        self.label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.label2.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.label3.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.label4.grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.label5.grid(row=4, column=0, pady=10, padx=10, sticky="w")

        button_page.grid(row=14, column=1, pady=10, padx=10, sticky="se")
        button_quit.grid(row=15, column=1, pady=10, padx=10, sticky="se")

        self.update_method()

    def update_method(self):
        tempc = Temperature(sense)
        temp_new = tempc.temperature_c()
        self.label.configure(text="temperature: " + str(round(temp_new, 1)) + " \u2103")
        print("update pushed")
        self.after(2000, self.update_method)


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
print("break point 3")
app.mainloop()
