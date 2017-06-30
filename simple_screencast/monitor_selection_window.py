from __future__ import division

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk

from . import PROGRAM_NAME
from .helpers import find_data_path
from .monitors import Monitors


class MonitorSelectionWindow(Gtk.Window):

    selected_monitor = None

    _callback = None
    _recording_button = None

    _monitor = None

    _canvas_width = None
    _canvas_height = None
    _scale = None
    _monitors_rects = []

    def __init__(self, callback):
        Gtk.Window.__init__(self,
                title=PROGRAM_NAME,
                icon_name="simple-screencast",
                resizable=False)

        self._callback = callback

        builder = Gtk.Builder()
        builder.add_from_file(find_data_path("ui/monitor-selection-window.ui"))
        builder.connect_signals(self)

        recording_window_content = builder.get_object("monitor-selection-window-content")
        recording_window_content.unparent()
        self.add(recording_window_content)

        self._recording_button = builder.get_object("start-recording")
        self._monitor = Monitors()

        self._calculate_display_geometries()

        self.connect("delete-event", self.cancel)
        self.connect("focus-in-event", self.on_focus_in_event)
        self.connect("focus-out-event", self.on_focus_out_event)

    def _calculate_display_geometries(self):
        CANVAS_MAX_WIDTH = 600
        CANVAS_MAX_HEIGHT = 500

        monitors = list(self._monitor.list_monitors())

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
                "label": monitor["label"],
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

        COLOR_LABELS_BG = (0x33/255, 0x33/255, 0x33/255)
        COLOR_LABELS_TEXT = (0xFF/255, 0xFF/255, 0xFF/255)

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

            # draw screen labels
            cr.set_source_rgb(*COLOR_LABELS_BG)
            cr.rectangle(x + 10, y + 10, 30, 30)
            cr.fill();

                # cr.select_font_face
            cr.set_source_rgb(*COLOR_LABELS_TEXT)
            cr.set_font_size(20)
            x_bearing, y_bearing, width, height = cr.text_extents(kwargs["label"])[:4]
            cr.move_to(
                    x + 10 + 15 - x_bearing - width / 2,
                    y + 10 + 15 - y_bearing - height / 2
                    )
            cr.show_text(kwargs["label"])

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
            self._recording_button.set_sensitive(True)

    def on_focus_in_event(self, widget, event):
        labels = self._monitor.get_labels()
        self._monitor.show_labels(labels)

    def on_focus_out_event(self, widget, event):
        self._monitor.hide_labels()

    def validate(self, *args):
        self._monitor.hide_labels()
        self.destroy()
        self._callback(self.selected_monitor)

    def cancel(self, *args):
        self._monitor.hide_labels()
        self.destroy()
        self._callback(None)
