import tkinter as tk

master = tk.Tk()
variable = tk.StringVar(master)
variable.set('one')
e = tk.Entry(master, width=50)
e.pack()
e.insert(0, 'Enter your Name:')
w = tk.OptionMenu(master, variable, 'one', 'two', 'three')
w.pack()


def myClick():
    myLabel = tk.Label(master, text='Hello ' + e.get())
    myLabel.pack()

myButton = tk.Button(master, text='Enter your name', command=myClick)
myButton.pack()
print(type(e.get()))
master.mainloop()
