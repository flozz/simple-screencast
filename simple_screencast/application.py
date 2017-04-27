import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gio

from . import APPLICATION_ID


class SimpleScreencastApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                application_id=APPLICATION_ID,
                flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        # Create actions
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.action_quit_cb)
        self.add_action(action)

    def do_activate(self):
        win = Gtk.ApplicationWindow(
                application=self,
                visible=True,
                title="Simple Screencast")

    def action_quit_cb(self, action, parameter):
        self.quit()

