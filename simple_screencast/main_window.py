import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio

from . import PROGRAM_NAME
from .helpers import find_data_path


class MainWindow(Gtk.ApplicationWindow):

    TARGET_DESKTOP = "record-desktop"
    TARGET_SCREEN = "record-screen"
    TARGET_AREA = "record-area"

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                application=app,
                title=PROGRAM_NAME,
                icon_name="simple-screencast",
                default_width=100,
                default_height=100,
                resizable=False)

        self._target = self.TARGET_DESKTOP

        builder = Gtk.Builder()
        builder.add_from_file(find_data_path("ui/main-window.ui"))
        builder.connect_signals(self)

        main_window_content = builder.get_object("main-window-content")
        main_window_content.unparent()
        self.add(main_window_content)

    def _screencast_target_changed(self, widget):
        if not widget.get_active():
            return
        btns = {
            "screencast-target-desktop": self.TARGET_DESKTOP,
            "screencast-target-screen": self.TARGET_SCREEN,
            "screencast-target-area": self.TARGET_AREA,
        }
        self._target = btns[widget.get_name()]

    def _start_recording_button_clicked(self, widget):
        app = self.get_application()
        app.activate_action(self._target)
