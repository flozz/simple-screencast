from gi.repository import GLib
import pydbus

from .monitor_selection_window import MonitorSelectionWindow
from .monitors import Monitors


GNOME_SHELL_SCREENSHOT = "org.gnome.Shell.Screenshot"
GNOME_SHELL_SCREENCAST = "org.gnome.Shell.Screencast"


class Screencast:

    def __init__(self):
        self._options = {
            "file-template": "Screencast %d %t.webm",
            "draw-cursor": True,
            "framerate": 30,
            "pipeline": None
        }
        self._bus = pydbus.SessionBus()
        self._screenshot = self._bus.get(GNOME_SHELL_SCREENSHOT)
        self._screencast = self._bus.get(GNOME_SHELL_SCREENCAST)

    def get_options(self):
        return self._options

    def set_options(self, options):
        raise NotImplementedError()  # TODO

    def select_monitor_async(self, callback):
        win = MonitorSelectionWindow(callback)
        win.show()

    def select_area(self):
        try:
            return self._screenshot.SelectArea()
        except GLib.Error, e:
            # Error code 19: Operation was cancelled
            if e.code != 19:
                raise e
            return None

    def record_desktop(self):
        return self._screencast.Screencast(self._options["file-template"], {})  # TODO options

    def record_monitor(self, monitor_id):
        for monitor in Monitors().list_monitors():
            if monitor["id"] != monitor_id:
                continue
            self._screencast.ScreencastArea(monitor["x"], monitor["y"],
                    monitor["width"], monitor["height"],
                    self._options["file-template"], {})  # TODO options
            break

    def record_area(self, x, y, width, height):
        return self._screencast.ScreencastArea(x, y, width, height,
                self._options["file-template"], {})  # TODO options

    def stop_recording(self):
        return self._screencast.StopScreencast()

