from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog as fd
import sys

config_object = ConfigParser()
config_object['WALLPAPERS'] = {}

root = Tk()
root.geometry('700x450')
root.title('Configuration window')
root.iconbitmap('C:/Users/foxth/Desktop/балдеж/Wallpapers/tray.ico/')


date_periods = ['morning', 'day', 'evening', 'night']

entry_dict = {}
but_dict = {}


timestamp = 7

row = 0
for period in date_periods:
    time_range = f'From {timestamp} to {(timestamp+5)%24}:'
    Label(text=time_range).grid(column=0, row=row, padx=20, pady=30, sticky=E)

    entry_dict[period] = Entry(root, width=50)
    entry_dict[period].grid(column=1, row=row, padx=0, pady=0, sticky=E)

    but_dict[period + '_but'] = Button(root, text='Choose', width=10, command=lambda r=row: choose_(r))
    but_dict[period + '_but'].grid(column=2, row=row, padx=20, pady=0, sticky=E)

    row += 1
    timestamp = (timestamp + 5) % 24


apply_but = Button(root, text='Apply', width=10)
exit_but = Button(root, text='Exit', command=sys.exit, width=10)


def choose_(r):
    path = fd.askopenfilename()
    for period in date_periods:
        if r == entry_dict[period].grid_info()['row']:
            entry_dict[period].delete(0, END)
            entry_dict[period].insert(0, path)


def apply_(event):
    for period in date_periods:
        config_object['WALLPAPERS'].update({period: entry_dict[period].get()})

    with open('config.ini', 'w') as conf:
        config_object.write(conf)


apply_but.bind('<Button-1>', apply_)

apply_but.grid(column=1, row=4, padx=0, pady=20, sticky=W)
exit_but.grid(column=1, row=4, padx=0, pady=20, sticky=E)

root.mainloop()
