from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog as fd
import sys

config_object = ConfigParser()
config_object.read("config.ini")


root = Tk()

w = 650
h = 450
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = int((ws / 2) - (w / 2))
y = int((hs / 2) - (h / 2))

root.geometry(f'{w}x{h}+{x}+{y}')

root.title('Configuration window')
root.iconbitmap('tray.ico')


date_periods = list(config_object['WALLPAPERS'].keys())

row = 1
apply_but = Button(root, text='Apply', width=25)
exit_but = Button(root, text='Exit', command=sys.exit, width=10)
apply_but.grid(column=1, row=row - 1, padx=120, pady=20, sticky=E)
exit_but.grid(column=2, row=row - 1, padx=20, pady=20, sticky=E)

label_dict = {}
entry_dict = {}
but_dict = {}
dest_dict = {}

timestamp = 7


for period in date_periods:
    time_range = f'{period}, from {timestamp} to {(timestamp+5)%24}:'
    label_dict[period] = Label(text=time_range)
    label_dict[period].grid(column=1, row=row, padx=20, pady=10, sticky=W)

    entry_dict[period] = Entry(root, width=50)
    entry_dict[period].grid(column=1, row=row + 1, padx=20, pady=0, sticky=E)

    but_dict[period] = Button(root, text='Choose',
                              width=10, command=lambda r=row + 1: choose_(r))
    but_dict[period].grid(column=2,
                          row=row + 1, padx=20, pady=0, sticky=E)

    dest_dict[period] = Button(text='x', command=lambda r=row + 1: destroy_(r))
    dest_dict[period].grid(column=3,
                           row=row + 1, padx=0, pady=0, sticky=E)

    row += 2
    timestamp = (timestamp + 5) % 24


def choose_(r):
    path = fd.askopenfilename(filetypes=[
        ('Images', '.png'),
        ('Images', '.jpg'),
        ('Images', '.jpeg')])
    for period in date_periods:
        if r == entry_dict[period].grid_info()['row']:
            entry_dict[period].delete(0, END)
            entry_dict[period].insert(0, path)


def destroy_(r):
    for period in date_periods:
        if r == entry_dict[period].grid_info()['row']:
            date_periods.remove(period)
            label_dict[period].destroy()
            entry_dict[period].destroy()
            but_dict[period].destroy()
            dest_dict[period].destroy()


def apply_(event):
    config_object['WALLPAPERS'] = {}
    for period in date_periods:
        config_object['WALLPAPERS'].update({period: entry_dict[period].get()})

    with open('config.ini', 'w') as conf:
        config_object.write(conf)


apply_but.bind('<Button-1>', apply_)


root.mainloop()
