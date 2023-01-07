import os
import sys
import math
# import pywin
import win32api
import win32gui
import win32con
from pynput.keyboard import Key, Controller
keyboard = Controller()


def main():
    active_window: int = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(active_window, win32con.SW_MINIMIZE)


if __name__ == '__main__':
    main()
