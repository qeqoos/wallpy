import ctypes
import time
import os
import sys
from configparser import ConfigParser
from threading import Thread
from datetime import datetime
from PySide2 import QtWidgets, QtGui

config_object = ConfigParser()
config_object.read("config.ini")


SPI = 20

wallpapers = config_object['WALLPAPERS']
timestamps = config_object['TIMESTAMPS']

period_list = list(wallpapers.keys())


date_periods = {}

for period in period_list:
    formatted_timestamp = timestamps[period].split('-')
    date_periods.update({wallpapers[period]: formatted_timestamp})


def setwall():
    for wallpaper, hour in date_periods.items():
        start = int(hour[0])
        fin = int(hour[1])
        if start < fin:
            if datetime.today().hour in range(start, fin):
                ctypes.windll.user32.SystemParametersInfoW(
                    SPI, 0, wallpaper, 0)
        elif start > fin:
            if datetime.today().hour in range(start, 24) or datetime.today().hour in range(0, fin):
                ctypes.windll.user32.SystemParametersInfoW(
                    SPI, 0, wallpaper, 0)


def thread_loop():
    while True:
        setwall()
        time.sleep(600)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Wallpy')
        menu = QtWidgets.QMenu(parent)

        open_config_app = menu.addAction('Configure wallpy')
        open_config_app.triggered.connect(self.open_config)

        exit_ = menu.addAction('Exit')
        exit_.triggered.connect(lambda: os._exit(1))

        menu.addSeparator()
        self.setContextMenu(menu)

    def open_config(self):
        os.system('config_wallpy.py')


def tray():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon('tray.ico'), w)
    tray_icon.show()
    sys.exit(app.exec_())


my_loop = Thread(target=thread_loop, args=())
my_loop.start()
tray()
