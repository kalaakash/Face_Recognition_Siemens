from tkinter import *
import os
m = Tk()
m.title('Face Recognition UI')
Label(m, text='Name of group ').grid(row=0)
e1 = Entry(m)
e1.grid(row=0, column=1)
#button_1 = tk.Button(m, text='Add stuff', width=25, height=15, command=m.destroy)
#button_1.pack()
m.mainloop()
os.system("clear")

'''
from tkinter import *
master = Tk()
Label(master, text='First Name').grid(row=0)
Label(master, text='Last Name').grid(row=1)
e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
mainloop()
'''