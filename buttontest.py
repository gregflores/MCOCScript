# import tkinter as tk
# def write_slogan():
#     print('Tkinter is easy to use!')

# def close_window():
#     root.destroy()
#     print('Quit')

# root = tk.Tk()
# frame = tk.Frame(root)
# frame.pack()

# button = tk.Button(frame,
#                     text='QUIT',
#                     fg='red',
#                     command=close_window)
# button.pack(side=tk.LEFT)

# slogan = tk.Button(frame,
#                     text='Hello',
#                     command=write_slogan)
# slogan.pack(side=tk.LEFT)

# #root.mainloop()
# while True:
#     root.update_idletasks()
#     root.update()

import tkinter as tk

def onClick(event=None):
    counter.set(counter.get() + 1)

def onQuit(event=None):
    running.set(False)

master = tk.Tk()
master.geometry('200x200+500+800')
w = tk.Label(master, text = 'Series Count', width = 30)
button = tk.Button(master, text = 'plus', command = onClick).pack()
quitbutton = tk.Button(master, text = 'quit', command = onQuit).pack()

w.pack()

counter = tk.IntVar()
running = tk.BooleanVar()
tk.Label(master,textvariable = counter).pack()

running.set(True)
print(running.get())
while running.get():
    master.update_idletasks()
    master.update()