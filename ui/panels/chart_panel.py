# ui/panels/chart_panel.py
import tkinter as tk
from tkinter import ttk   # <-- REQUIRED
from ui.components.card import Card
from ui.components.gannt_canvas import GanttCanvas
from ui.theme import colors


class ChartPanel(ttk.Frame):
    """Center panel containing the Gantt canvas and simple controls."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style="Panel.TFrame", **kwargs)
        self.card = Card(self)
        self.card.pack(fill="both", expand=True, padx=8, pady=8)
        ttk.Label(self.card, text="Timeline Visualizer", foreground=colors.TEXT_PRIMARY, background=colors.PANEL_BG).pack(anchor="w")
        self.gantt = GanttCanvas(self.card, height=360)
        self.gantt.pack(fill="both", expand=True, pady=(6,0))
