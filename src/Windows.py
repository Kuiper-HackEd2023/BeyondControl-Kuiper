
import win32process
import win32gui
import win32con
import psutil
from pynput.keyboard import Key, Controller


class Windows:
    _keyboard = Controller()

    def _updateActiveInfo(self):
        gui_id: int = win32gui.GetForegroundWindow()
        pid: int = win32process.GetWindowThreadProcessId(gui_id)[-1]
        name: str = psutil.Process(pid).name()

        self._prev_gui_id: int = self._current_gui_id
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

    def maximizeWindow(self):
        self._updateActiveInfo()
        win32gui.ShowWindow(self._prev_gui_id, win32con.SW_MAXIMIZE)

    def changeVolume(self, decrease: bool = False):
        volume_key = Key.media_volume_down if decrease else Key.media_volume_up
        self._keyboard.press(volume_key)
        return

    def tester(self):
        self._updateActiveInfo()