from __future__ import division

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk

from . import PROGRAM_NAME
from .helpers import find_data_path


class MonitorSelectionWindow(Gtk.ApplicationWindow):

    selected_screen = None

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

    def on_drawing_area_draw(self, widget, cr):
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

        widget.set_size_request(canvas_width, canvas_height)

        # TODO check that the requested size has been applyied (widget.get_allocated_width/height)

        # Calculate offsets to center the screens on the canvas
        offset_x = round((canvas_width - display_width * scale) / 2)
        offset_y = round((canvas_height - display_height * scale) / 2)

        def _draw_monitor(cr, monitor):
            PADDING = 3
            COLOR_BG = (0x00/255, 0xFF/255, 0xFF/255)
            COLOR_FG = (0x33/255, 0x33/255, 0x33/255)

            monitor_rect_x = offset_x + round((monitor["x"] - min_x) * scale) + PADDING
            monitor_rect_y = offset_y + round((monitor["y"] - min_y) * scale) + PADDING
            monitor_rect_w = round(monitor["width"] * scale) - PADDING * 2
            monitor_rect_h = round(monitor["height"] * scale) - PADDING * 2

            # TODO draw the wallpaper, if any, instead of a color
            cr.set_source_rgb(*COLOR_BG)
            cr.rectangle(monitor_rect_x, monitor_rect_y, monitor_rect_w, monitor_rect_h)
            cr.fill()

            cr.set_source_rgb(*COLOR_FG)
            cr.rectangle(monitor_rect_x, monitor_rect_y, monitor_rect_w, monitor_rect_h)
            cr.stroke()

            # TODO draw screen labels

        for monitor in monitors:
            _draw_monitor(cr, monitor)

