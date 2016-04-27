import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        
        container.config(cursor="none")
        w, h = container.winfo_screenwidth(), container.winfo_screenheight()
        container.overrideredirect(1)
        container.geometry("%dx%d+0+0" % (w, h))
        

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
        label = tk.Label(self, text="this is text")
        label.pack(pady=10, padx=10)


app = App()
app.mainloop()
