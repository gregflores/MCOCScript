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

master = tk.Tk()
w = tk.Label(master, text = 'Hello World!', fg = 'red', font = ('Helvetica', 16), height = 30, width = 30)

w.pack()

v = tk.IntVar()
tk.Label(master, textvariable = v).pack()

while True:
    master.update_idletasks()
    master.update()
    v.set(v.get() + 1)