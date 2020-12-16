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
wf = "C:/Users/foxth/Desktop/балдеж/Wallpapers/"

wallpapers = config_object['WALLPAPERS']

date_periods = {wallpapers['morning']: [i for i in range(6, 12)],
                wallpapers['day']: [i for i in range(12, 17)],
                wallpapers['evening']: [i for i in range(17, 21)],
                wallpapers['night']: [i for i in range(0, 6)]}


def setwall():
    for wallpaper, hour in date_periods.items():
        if datetime.today().hour in hour:
            ctypes.windll.user32.SystemParametersInfoW(SPI, 0, wallpaper, 0)


def thread_loop():
    while True:
        setwall()
        time.sleep(600)


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Wallpy')
        menu = QtWidgets.QMenu(parent)

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: os._exit(1))

        menu.addSeparator()
        self.setContextMenu(menu)


def tray():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon(wf + 'tray.ico'), w)
    tray_icon.show()
    sys.exit(app.exec_())


my_loop = Thread(target=thread_loop, args=())
my_loop.start()
tray()
