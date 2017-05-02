import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from . import PROGRAM_NAME


class RecordingWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                application=app,
                title="recording... - %s" % PROGRAM_NAME)

        stop_button = Gtk.Button(label="Stop recording")
        stop_button.connect("clicked", self._stop_button_clicked)
        self.add(stop_button)

    def _stop_button_clicked(self, widget):
        app = self.get_application()
        app.activate_action("stop-recording")
