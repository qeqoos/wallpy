from configparser import ConfigParser
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter import simpledialog
import sys

config_object = ConfigParser()
config_object.read("config.ini")


root = Tk()

w = 650
h = 500
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = int((ws / 2) - (w / 2))
y = int((hs / 2) - (h / 2))

root.geometry(f'{w}x{h}+{x}+{y}')

root.title('Configuration window')
root.iconbitmap('tray.ico')

date_periods = list(config_object['WALLPAPERS'].keys())
timestamp_periods = config_object['TIMESTAMPS']

row = 1
apply_but = Button(root, text='Apply', width=25)
exit_but = Button(root, text='Exit', command=sys.exit, width=10)
apply_but.grid(column=1, row=row - 1, padx=120, pady=20, sticky=E)
exit_but.grid(column=2, row=row - 1, padx=20, pady=20, sticky=E)

label_dict = {}
entry_dict = {}
but_dict = {}
dest_dict = {}
add_but = 0


def display_periods(row):
    global add_but
    for period in date_periods:
        formatted_timestamp = timestamp_periods[period].split('-')
        time_range = f'{period}, from {formatted_timestamp[0]} to {formatted_timestamp[1]}:'
        label_dict[period] = Label(text=time_range)
        label_dict[period].grid(column=1, row=row, padx=20, pady=10, sticky=W)

        entry_dict[period] = Entry(root, width=50)
        entry_dict[period].grid(column=1, row=row + 1,
                                padx=20, pady=0, sticky=E)
        if period in config_object['WALLPAPERS']:
            entry_dict[period].insert(0, config_object['WALLPAPERS'][period])

        but_dict[period] = Button(root, text='Choose',
                                  width=10, command=lambda r=row + 1: choose_(r))
        but_dict[period].grid(column=2,
                              row=row + 1, padx=20, pady=0, sticky=E)

        dest_dict[period] = Button(
            text='x', command=lambda r=row + 1: destroy_(r))
        dest_dict[period].grid(column=3,
                               row=row + 1, padx=0, pady=0, sticky=E)

        row += 2

    add_but = Button(root, text='Add new', width=10, command=add_)
    add_but.bind('<Button-1>', add_)
    add_but.grid(column=1, row=row, padx=80, pady=40, sticky=E)


def choose_(r):
    path = fd.askopenfilename(filetypes=[
        ('Images', '.png'),
        ('Images', '.jpg'),
        ('Images', '.jpeg')])
    for period in date_periods:
        if r == entry_dict[period].grid_info()['row']:
            entry_dict[period].delete(0, END)
            entry_dict[period].insert(0, path)


def add_():
    global row
    period_name = simpledialog.askstring(
        title="Configuration", prompt="Name of your period:")
    period_from = simpledialog.askstring(
        title="Time interval", prompt="From hour:")
    period_to = simpledialog.askstring(
        title="Time interval", prompt="To hour:")

    if int(period_from) in range(0, 24) and int(period_to) in range(0, 24):
        timestamp = f'{period_from}-{period_to}'
    else:
        mb.showerror('Error', 'Invalid timestamp values.')

    if int(period_from) > int(period_to):
        local_time_range = [i for i in range(
            int(period_from), 24)] + [i for i in range(0, int(period_to))]
    elif int(period_from) < int(period_to):
        local_time_range = [i for i in range(int(period_from), int(period_to))]

    pass_ = True
    for period in date_periods:
        formatted_timestamp = timestamp_periods[period].split('-')
        for i in local_time_range:
            if i in range(int(formatted_timestamp[0]), int(formatted_timestamp[1])):
                mb.showerror(
                    'Error', f'Timestamps are overlapping with {period}')
                pass_ = False
                break
            else:
                pass

    if pass_:
        for period in date_periods:
            label_dict[period].destroy()
            entry_dict[period].destroy()
            but_dict[period].destroy()
            dest_dict[period].destroy()

        add_but.destroy()
        date_periods.append(period_name)
        timestamp_periods.update({period_name: timestamp})
        display_periods(row)


def destroy_(r):
    for period in date_periods:
        if r == entry_dict[period].grid_info()['row']:
            date_periods.remove(period)
            del timestamp_periods[period]
            label_dict[period].destroy()
            entry_dict[period].destroy()
            but_dict[period].destroy()
            dest_dict[period].destroy()


def apply_(event):
    config_object['WALLPAPERS'] = {}
    for period in date_periods:
        config_object['WALLPAPERS'].update({period: entry_dict[period].get()})
        config_object['TIMESTAMPS']

    with open('config.ini', 'w') as conf:
        config_object.write(conf)


apply_but.bind('<Button-1>', apply_)

display_periods(row)

root.mainloop()
