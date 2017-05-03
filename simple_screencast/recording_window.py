import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk

from . import PROGRAM_NAME
from .helpers import find_data_path


class RecordingWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                application=app,
                title=PROGRAM_NAME,
                icon_name="simple-screencast",
                default_width=10,
                default_height=10,
                resizable=False,
                show_menubar=False)

        builder = Gtk.Builder()
        builder.add_from_file(find_data_path("ui/recording-window.ui"))
        builder.connect_signals(self)

        recording_window_content = builder.get_object("recording-window-content")
        recording_window_content.unparent()
        self.add(recording_window_content)

    def _stop_button_clicked(self, widget):
        app = self.get_application()
        app.activate_action("stop-recording")
