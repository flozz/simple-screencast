from gi.repository import GLib, Gio


class Monitors:

    def __init__(self):
        self._bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
        self._displayconfig_bus_proxy = Gio.DBusProxy.new_sync(
                self._bus,
                Gio.DBusProxyFlags.NONE,
                None,
                "org.gnome.Mutter.DisplayConfig",
                "/org/gnome/Mutter/DisplayConfig",
                "org.gnome.Mutter.DisplayConfig",
                None)
        self._shell_bus_proxy = Gio.DBusProxy.new_sync(
                self._bus,
                Gio.DBusProxyFlags.NONE,
                None,
                "org.gnome.Shell",
                "/org/gnome/Shell",
                "org.gnome.Shell",
                None)

    def list_monitors(self):
        response = self._displayconfig_bus_proxy.call_sync(
                "GetResources",
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None)

        serial, crtcs, outputs, modes, max_screen_width, max_screen_height = response.unpack()

        for _, _, id_, _, _, _, _, rr_output in outputs:
            for crtcid, _, x, y, width, height, _, _, _, _ in crtcs:
                if crtcid != id_:
                    continue
                yield {
                    "id": id_,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                    "display-name": rr_output["display-name"],
                    "connector-type": rr_output["connector-type"],
                    "height-mm": rr_output["height-mm"],
                    "width-mm": rr_output["width-mm"],
                    "primary": rr_output["primary"],
                    "product": rr_output["product"],
                    "serial": rr_output["serial"],
                    "vendor": rr_output["vendor"]}
                break

    def get_labels(self):
        monitors = self.list_monitors()
        labels = {}
        for monitor in monitors:
            labels[monitor["id"]] = str(monitor["id"] + 1)
        return labels

    def show_labels(self, labels=None):
        if not labels:
            labels = self.get_labels()

        g_labels = GLib.Variant.new_tuple(
                GLib.Variant("a{uv}", {i: GLib.Variant.new_string(v) for i, v in labels.items()})
                )

        self._shell_bus_proxy.call(
                "ShowMonitorLabels",
                g_labels,
                Gio.DBusCallFlags.NONE,
                -1,
                None)

    def hide_labels(self):
        self._shell_bus_proxy.call(
                "HideMonitorLabels",
                None,
                Gio.DBusCallFlags.NONE,
                -1,
                None)

