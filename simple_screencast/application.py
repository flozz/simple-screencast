import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio

from . import APPLICATION_ID
from .screencast import Screencast
from .main_window import MainWindow
from .recording_window import RecordingWindow
from .helpers import find_data_path


class SimpleScreencastApplication(Gtk.Application):

    STATE_MAIN = "main"
    STATE_RECORDING = "recording"

    def __init__(self):
        Gtk.Application.__init__(self,
                application_id=APPLICATION_ID,
                flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.screencast = None
        self.main_window = None
        self.recording_window = None

    def switch_state(self, state):
        app_windows = self.get_windows()

        for win in app_windows:
            win.destroy()

        if state == self.STATE_MAIN:
            win = MainWindow(self)
            win.show_all()
        elif state == self.STATE_RECORDING:
            win = RecordingWindow(self)
            win.show_all()
        else:
            raise ValueError()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self.screencast = Screencast()

        # Create actions
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.action_quit_cb)
        self.add_action(action)

        # App Menu
        builder = Gtk.Builder()
        builder.add_from_file(find_data_path("ui/app-menu.ui"))
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        app_windows = self.get_windows()

        if not app_windows:
            self.switch_state(self.STATE_MAIN)
        else:
            win = app_windows[0]
            win.hide()
            win.show_all()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)
        self.screencast.stop_recording()

    def action_quit_cb(self, action, parameter):
        self.quit()

