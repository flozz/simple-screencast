import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk


class RecordingWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                application=app,
                title="Simple Screencast - recording...")

        stop_button = Gtk.Button(label="Stop recording")
        stop_button.connect("clicked", self._stop_button_clicked)
        self.add(stop_button)

    def _stop_button_clicked(self, widget):
        app = self.get_application()
        app.switch_state(app.STATE_MAIN)
        app.screencast.stop_recording()
