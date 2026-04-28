# ui/components/gantt_canvas.py
import tkinter as tk
from typing import List, Tuple
from ui.theme import colors

# timeline entry: (start_time, end_time, pid)
TimelineEntry = Tuple[int, int, str]

class GanttCanvas(tk.Canvas):
    """
    Draws a Gantt-style timeline.
    Call draw_timeline(timeline, color_map) to render.
    """
    def __init__(self, parent, height=300, **kwargs):
        super().__init__(parent, bg=colors.PANEL_BG, highlightthickness=0, **kwargs)
        self.height = height
        self.configure(height=height)
        self.padding = 12
        self.bar_height = 28
        self.row_gap = 8
        self.bind("<Configure>", lambda e: self.redraw())

        self._timeline = []
        self._color_map = {}
        self._pid_rows = {}  # pid -> row index
        self._max_time = 0

    def clear(self):
        self.delete("all")
        self._timeline = []
        self._pid_rows = {}
        self._max_time = 0

    def draw_timeline(self, timeline: List[TimelineEntry], color_map: dict):
        """
        timeline: list of (start, end, pid).
        color_map: pid -> color
        """
        self.clear()
        self._timeline = timeline
        self._color_map = color_map
        # compute pids and max time
        pids = [pid for _, _, pid in timeline if pid != "IDLE"]
        unique_pids = sorted(list(dict.fromkeys(pids)))  # preserve order
        for i, pid in enumerate(unique_pids):
            self._pid_rows[pid] = i
        self._max_time = max((e for _, e, _ in timeline), default=0)
        self.redraw()

    def redraw(self):
        self.delete("all")
        if not self._timeline:
            # draw placeholder text
            w = self.winfo_width()
            h = self.winfo_height()
            self.create_text(w//2, h//2, text="Gantt chart will appear here",
                             fill=colors.TEXT_MUTED, font=("Segoe UI", 12, "italic"))
            return

        # drawing area
        w = max(self.winfo_width(), 200)
        left = self.padding
        right = w - self.padding
        usable_w = max(1, right - left)
        scale = usable_w / max(1, self._max_time)

        # draw time grid (subtle)
        for t in range(0, int(self._max_time) + 1):
            x = left + t * scale
            self.create_line(x, 0, x, self.height, fill="#2F3440", dash=(2, 2))

        # draw bars
        for start, end, pid in self._timeline:
            if pid == "IDLE":
                color = colors.IDLE_COLOR
                row = -1  # idle row at top
            else:
                color = self._color_map.get(pid, colors.ACCENT_PALETTE[0])
                row = self._pid_rows.get(pid, 0)

            y_top = self.padding + (row + 1) * (self.bar_height + self.row_gap)
            y_bottom = y_top + self.bar_height
            x1 = left + start * scale
            x2 = left + end * scale
            # subtle rounded-like rectangle (create_rectangle + small oval ends)
            self.create_rectangle(x1, y_top, x2, y_bottom, fill=color, outline="", width=0)
            # text label
            if pid != "IDLE":
                self.create_text((x1 + x2) / 2, (y_top + y_bottom) / 2, text=pid,
                                 fill=colors.TEXT_PRIMARY, font=("Segoe UI", 9, "bold"))
