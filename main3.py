import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.config(cursor="none")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.overrideredirect(1)
        self.geometry("%dx%d+0+0" % (w, h))

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="thermostat: ")
        label2 = tk.Label(self, text="heating: ")
        label3 = tk.Label(self, text="temperature: ")

        button_quit = tk.Button(self, text="quit", command=self.quit)

        label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        label2.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        label3.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        button_quit.grid(row=0, column=1, pady=10, padx=10, sticky="se")


app = App()
app.mainloop()
