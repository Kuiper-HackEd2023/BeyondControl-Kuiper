import win32process
import win32gui
import win32con
import psutil
from pynput.keyboard import Key, Controller


class GestureActions:
    _keyboard = Controller()
    _windows = []

    def _updateActiveInfo(self):
        gui_id: int = win32gui.GetForegroundWindow()
        pid: int = win32process.GetWindowThreadProcessId(gui_id)[-1]
        name: str = psutil.Process(pid).name()

        self._pid: int = pid
        self._current_gui_id: int = gui_id
        self._process_name: str = name
        return

    def __init__(self) -> None:
        self._prev_gui_id: int = 0
        self._current_gui_id: int = 0
        self._pid: int = 0
        self._current_gui_id: int = 0
        self._process_name: str = ""

        self._updateActiveInfo()

    def minimizeWindow(self):
        self._updateActiveInfo()
        win32gui.ShowWindow(self._current_gui_id, win32con.SW_MINIMIZE)
        self._windows.append(self._current_gui_id)

    def maximizeWindow(self):
        self._updateActiveInfo()
        if len(self._windows) == 0:
            return
        prev_window = self._windows.pop()
        win32gui.ShowWindow(prev_window, win32con.SW_MAXIMIZE)

    def increaseVolume(self):
        self._updateActiveInfo()
        self._keyboard.press(Key.media_volume_up)

    def decreaseVolume(self):
        self._updateActiveInfo()
        self._keyboard.press(Key.media_volume_down)

    def toggleMediaStatus(self):
        self._keyboard.press(Key.media_play_pause)

    def toggleMute(self):
        self._keyboard.press(Key.media_volume_mute)
