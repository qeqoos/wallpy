import ctypes
import time
import os
import sys

from threading import Thread
from datetime import datetime
from PySide2 import QtWidgets, QtGui

SPI = 20
wf = "C:/Users/foxth/Desktop/балдеж/Wallpapers/"

def setwall():
    if datetime.today().hour in range(7, 12):
        ctypes.windll.user32.SystemParametersInfoW(
            SPI, 0, wf + 'Morning.jpg', 0)
    if datetime.today().hour in range(12, 16):
        ctypes.windll.user32.SystemParametersInfoW(
            SPI, 0, wf + 'Day.jpg', 0)
    if datetime.today().hour in range(16, 19):
        ctypes.windll.user32.SystemParametersInfoW(
            SPI, 0, wf + 'Evening2.jpg', 0)
    if datetime.today().hour in range(19, 22):
        ctypes.windll.user32.SystemParametersInfoW(
            SPI, 0, wf + 'Evening.jpg', 0)
    if datetime.today().hour in range(22, 24):
        ctypes.windll.user32.SystemParametersInfoW(
            SPI, 0, wf + 'Night.jpg', 0)
    if datetime.today().hour in range(0, 7):
        ctypes.windll.user32.SystemParametersInfoW(
            SPI, 0, wf + 'Night.jpg', 0)


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
