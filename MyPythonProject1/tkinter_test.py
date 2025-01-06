'''import tkinter
window = tkinter.Tk()
window.title('Hello Python')
window.geometry("300x200+10+20")
window.mainloop()'''

'''import tkinter

def on_button_click():
    print("Button clicked!")

window = tkinter.Tk()
window.title('Hello Python')
window.geometry("300x200+10+20")

button = tkinter.Button(window, text="Click Me", command=on_button_click)
button.pack()

window.mainloop()'''

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter

def on_button_click():
    print("Button clicked!")

window = tkinter.Tk()
window.title('Hello Python')
window.geometry("300x200+10+20")

button = tkinter.Button(window, text="Click Me", command=on_button_click)
button.pack()

window.mainloop()