from tkinter import *


class App:
    def __init__(self, master):
        master.config(cursor="none")
        w, h = master.winfo_screenwidth(), master.winfo_screenheight()
        master.overrideredirect(1)
        master.geometry("%dx%d+0+0" % (w, h))

        content = Frame(master, padding=(3, 3, 12, 12))
        frame = Frame(content, borderwidth=5, relief="sunken", width=200, height=100)

        content.grid(column=0, row=0, sticky=(N, S, E, W))
        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))


        self.label = Label(
            content, text="item1"
        ).grid(row=0, pady=10, padx=10, sticky=W)

        self.label2 = Label(
            content, text="item2"
        ).grid(row=1, pady=10, padx=10, sticky=W)

        self.button = Button(
            content, text="quit", command=content.quit
        ).grid(row=2)

        # self.button.pack(side=LEFT)

        self.hi_there = Button(
            content, text="hello", command=self.say_hi
        ).grid(row=3, column=2)

        # self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("hello")


root = Tk()

app = App(root)

root.mainloop()

