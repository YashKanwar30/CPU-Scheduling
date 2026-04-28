# ui/components/labeled_entry.py
import tkinter as tk
from tkinter import ttk
from typing import Optional
from ui.theme import colors

class LabeledEntry(ttk.Frame):
    """Reusable label + entry widget with optional unit label."""
    def __init__(self, parent, label: str, width: int = 8, unit: Optional[str] = None, **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        self.columnconfigure(1, weight=1)
        self.lbl = ttk.Label(self, text=label, foreground=colors.TEXT_PRIMARY, background=colors.PANEL_BG)
        self.lbl.grid(row=0, column=0, sticky="w", padx=(6,4))
        self.var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, width=width)
        self.entry.grid(row=0, column=1, sticky="e", padx=(0,6))
        if unit:
            self.unit_lbl = ttk.Label(self, text=unit, foreground=colors.TEXT_MUTED, background=colors.PANEL_BG)
            self.unit_lbl.grid(row=0, column=2, sticky="w", padx=(4,6))
