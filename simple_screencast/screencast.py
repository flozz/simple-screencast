from gi.repository import GLib
import pydbus


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
        raise NotImplementedError()

    def select_area(self):
        try:
            return self._screenshot.SelectArea()
        except GLib.Error, e:
            # Error code 19: Operation was cancelled
            if e.code != 19:
                raise e
            return None

    def select_screen(self):
        raise NotImplementedError()

    def record_area(self, x, y, width, height):
        return self._screencast.ScreencastArea(x, y, width, height,
                self._options["file-template"], {})

    def record_screen(self, screen_id):
        raise NotImplementedError()

    def record_all_desktop(self):
        raise NotImplementedError()

    def stop_recording(self):
        return self._screencast.StopScreencast()

