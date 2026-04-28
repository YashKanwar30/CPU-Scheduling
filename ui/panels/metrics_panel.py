# ui/panels/metrics_panel.py
import tkinter as tk
from tkinter import ttk
from ui.components.card import Card
from ui.theme import colors
from typing import Dict

class MetricsPanel(ttk.Frame):
    """Right-side metrics and comparison panel."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, style="Panel.TFrame", **kwargs)
        self.card = Card(self)
        self.card.pack(fill="both", expand=True, padx=8, pady=8)
        ttk.Label(self.card, text="Metrics & Energy", foreground=colors.TEXT_PRIMARY, background=colors.PANEL_BG).pack(anchor="w")
        self.metrics_text = tk.Text(self.card, bg=colors.CARD_BG, fg=colors.TEXT_PRIMARY, height=20, wrap="word")
        self.metrics_text.pack(fill="both", expand=True, pady=6)
        self.metrics_text.configure(state="disabled")

    def display_result(self, name: str, result):
        """Append a simulation result (SimulationResult) to text area."""
        self.metrics_text.configure(state="normal")
        txt = f"--- {name} ---\n"
        txt += f"Energy: {result.energy:.3f}\n"
        for k, v in result.metrics.items():
            txt += f"{k}: {v}\n"
        txt += f"Context Switches: {result.context_switches}\n"
        txt += f"Idle Cycles: {result.idle_cycles}\n"
        txt += "Timeline:\n"
        for s, e, pid in result.timeline:
            txt += f"  [{s},{e}) -> {pid}\n"
        txt += "\n"
        self.metrics_text.insert("end", txt)
        self.metrics_text.configure(state="disabled")

    def clear(self):
        self.metrics_text.configure(state="normal")
        self.metrics_text.delete("1.0", "end")
        self.metrics_text.configure(state="disabled")
