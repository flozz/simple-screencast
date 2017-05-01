import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

from . import PROGRAM_NAME


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                application=app,
                title=PROGRAM_NAME,
                icon_name="simple-screencast")

        area_button = Gtk.Button(label="Record Area")
        area_button.connect("clicked", self._area_button_clicked)
        self.add(area_button)

    def _area_button_clicked(self, widget):
        app = self.get_application()

        area_rect = app.screencast.select_area()

        if not area_rect:
            return

        app.switch_state(app.STATE_RECORDING)
        app.screencast.record_area(*area_rect)
