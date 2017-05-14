from __future__ import division

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk

from . import PROGRAM_NAME
from .helpers import find_data_path


class MonitorSelectionWindow(Gtk.ApplicationWindow):

    selected_monitor = None

    _canvas_width = None
    _canvas_height = None
    _scale = None
    _monitors_rects = []

    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self,
                application=app,
                title=PROGRAM_NAME,
                icon_name="simple-screencast",
                resizable=False,
                show_menubar=False)

        builder = Gtk.Builder()
        builder.add_from_file(find_data_path("ui/monitor-selection-window.ui"))
        builder.connect_signals(self)

        recording_window_content = builder.get_object("monitor-selection-window-content")
        recording_window_content.unparent()
        self.add(recording_window_content)

        self._calculate_display_geometries()

    def _calculate_display_geometries(self):
        CANVAS_MAX_WIDTH = 600
        CANVAS_MAX_HEIGHT = 500

        app = self.get_application()
        monitors = list(app.monitors.list_monitors())

        # Calculate the display geometry
        min_x = float("+inf")
        min_y = float("+inf")
        max_x = float("-inf")
        max_y = float("-inf")

        for monitor in monitors:
            min_x = min(min_x, monitor["x"])
            min_y = min(min_y, monitor["y"])
            max_x = max(max_x, monitor["x"] + monitor["width"])
            max_y = max(max_y, monitor["y"] + monitor["height"])

        display_width = max_x - min_x
        display_height = max_y - min_y

        # Calculate best canvas size and scale
        scale = None
        canvas_width = None
        canvas_height = None

        if display_width >= display_height:
            scale = CANVAS_MAX_WIDTH / display_width
            canvas_width = CANVAS_MAX_WIDTH
            canvas_height = round(display_height * scale)
        else:
            scale = CANVAS_MAX_HEIGHT / display_height
            canvas_width = round(display_height * scale)
            canvas_height = CANVAS_MAX_HEIGHT

        # Calculate offsets to center the screens on the canvas
        offset_x = round((canvas_width - display_width * scale) / 2)
        offset_y = round((canvas_height - display_height * scale) / 2)

        # Calculate monitors rectangles
        monitors_rects = []

        for monitor in monitors:
            PADDING = 3

            monitors_rects.append({
                "id": monitor["id"],
                "x": offset_x + round((monitor["x"] - min_x) * scale) + PADDING,
                "y": offset_y + round((monitor["y"] - min_y) * scale) + PADDING,
                "width": round(monitor["width"] * scale) - PADDING * 2,
                "height": round(monitor["height"] * scale) - PADDING * 2})

        self._canvas_width = canvas_width
        self._canvas_height = canvas_height
        self._scale = scale
        self._monitors_rects = monitors_rects

    def on_drawing_area_draw(self, widget, cr):
        widget.set_size_request(self._canvas_width, self._canvas_height)

        def _draw_monitor(cr, x=0, y=0, width=0, height=0, **kwargs):
            COLOR_BG = (0x88/255, 0x88/255, 0x88/255)
            if self.selected_monitor == kwargs["id"]:
                COLOR_BG = (0x00/255, 0xFF/255, 0xFF/255)
            COLOR_FG = (0x33/255, 0x33/255, 0x33/255)

            # TODO draw the wallpaper, if any, instead of a color
            cr.set_source_rgb(*COLOR_BG)
            cr.rectangle(x, y, width, height)
            cr.fill()

            cr.set_source_rgb(*COLOR_FG)
            cr.rectangle(x, y, width, height)
            cr.stroke()

            # TODO draw screen labels

        for monitor_rect in self._monitors_rects:
            _draw_monitor(cr, **monitor_rect)

    def on_drawing_area_button_press_event(self, widget, event):
        for monitor_rect in self._monitors_rects:
            if event.x < monitor_rect["x"]:
                continue
            if event.x > monitor_rect["x"] + monitor_rect["width"]:
                continue
            if event.y < monitor_rect["y"]:
                continue
            if event.y > monitor_rect["y"] + monitor_rect["height"]:
                continue
            self.selected_monitor = monitor_rect["id"]
            self.queue_draw()
