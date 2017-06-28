from gi.repository import GLib, Gio

from .monitor_selection_window import MonitorSelectionWindow
from .monitors import Monitors


class Screencast:

    def __init__(self):
        self._options = {
            "file-template": "Screencast %d %t.webm",
            "draw-cursor": True,
            "framerate": 30,
            "pipeline": None
        }
        self._bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self._screenshot_bus_proxy = Gio.DBusProxy.new_sync(
                self._bus,
                Gio.DBusProxyFlags.NONE,
                None,
                "org.gnome.Shell.Screenshot",
                "/org/gnome/Shell/Screenshot",
                "org.gnome.Shell.Screenshot",
                None)
        self._screencast_bus_proxy = Gio.DBusProxy.new_sync(
                self._bus,
                Gio.DBusProxyFlags.NONE,
                None,
                "org.gnome.Shell.Screencast",
                "/org/gnome/Shell/Screencast",
                "org.gnome.Shell.Screencast",
                None)

    def get_options(self):
        return self._options

    def set_options(self, options):
        raise NotImplementedError()  # TODO

    def select_monitor_async(self, callback):
        win = MonitorSelectionWindow(callback)
        win.show()

    def select_area(self):
        try:
            area = self._screenshot_bus_proxy.call_sync(
                    "SelectArea",
                    None,
                    Gio.DBusCallFlags.NONE,
                    -1,
                    None)
            return area.unpack()
        except GLib.Error, e:
            # Error code 19: Operation was cancelled
            if e.code != 19:
                raise e
            return None

    def record_desktop(self):
        response = self._screencast_bus_proxy.call_sync(
                    "Screencast",
                    GLib.Variant.new_tuple(
                        GLib.Variant.new_string(self._options["file-template"]),
                        GLib.Variant("a{sv}", {})  # TODO options
                        ),
                    Gio.DBusCallFlags.NONE,
                    -1,
                    None)
        return response.unpack()

    def record_monitor(self, monitor_id):
        for monitor in Monitors().list_monitors():
            if monitor["id"] != monitor_id:
                continue
            response = self._screencast_bus_proxy.call_sync(
                        "ScreencastArea",
                        GLib.Variant.new_tuple(
                            GLib.Variant.new_int32(monitor["x"]),
                            GLib.Variant.new_int32(monitor["y"]),
                            GLib.Variant.new_int32(monitor["width"]),
                            GLib.Variant.new_int32(monitor["height"]),
                            GLib.Variant.new_string(self._options["file-template"]),
                            GLib.Variant("a{sv}", {})  # TODO options
                            ),
                        Gio.DBusCallFlags.NONE,
                        -1,
                        None)
            return response.unpack()

    def record_area(self, x, y, width, height):
        response = self._screencast_bus_proxy.call_sync(
                    "ScreencastArea",
                    GLib.Variant.new_tuple(
                        GLib.Variant.new_int32(x),
                        GLib.Variant.new_int32(y),
                        GLib.Variant.new_int32(width),
                        GLib.Variant.new_int32(height),
                        GLib.Variant.new_string(self._options["file-template"]),
                        GLib.Variant("a{sv}", {})  # TODO options
                        ),
                    Gio.DBusCallFlags.NONE,
                    -1,
                    None)
        return response.unpack()

    def stop_recording(self):
        success = self._screencast_bus_proxy.call_sync(
                    "StopScreencast",
                    None,
                    Gio.DBusCallFlags.NONE,
                    -1,
                    None)
        return success.unpack()

