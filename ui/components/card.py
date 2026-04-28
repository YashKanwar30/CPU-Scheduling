# ui/components/card.py
import tkinter as tk
from tkinter import ttk
from ui.theme import colors

class Card(ttk.Frame):
    """Simple elevated card used as container for panels/metrics."""
    def __init__(self, parent, padding=(8,8), **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        self["padding"] = padding
        self.configure(style="Card.TFrame")
