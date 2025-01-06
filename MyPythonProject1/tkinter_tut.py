import tkinter as tk

class application(tk.Tk):
    def _init_(self):
        tk.Tk._init_(self)
        self.geometry('500x500')
        self.title("First App")

app = application()
app.mainloop()