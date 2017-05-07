import pydbus


MUTTER_DISPLAYCONFIG = "org.gnome.Mutter.DisplayConfig"


class Monitors:

    def __init__(self):
        self._bus = pydbus.SessionBus()
        self._displayconfig = self._bus.get(MUTTER_DISPLAYCONFIG)

    def list_monitors(self):
        serial, crtcs, outputs, modes, max_screen_width, max_screen_height = self._displayconfig.GetResources()

        for crtc, output in zip(crtcs, outputs):
            id_, _, x, y, width, height, _, _, _, _ = crtc
            _, _, _, _, _, _, _, rr_output = output
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

