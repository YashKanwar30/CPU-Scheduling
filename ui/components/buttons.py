# ui/components/action_button.py
import tkinter as tk
from tkinter import ttk
from ui.theme import colors

class ActionButton(ttk.Frame):
    """Prominent pill-shaped button with hover effect."""
    def __init__(self, parent, text: str, command=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.btn = tk.Button(self, text=text, relief="flat", command=command,
                             bg=colors.BUTTON_BG, fg=colors.TEXT_PRIMARY,
                             activebackground=colors.BUTTON_HOVER, padx=12, pady=6,
                             font=("Segoe UI", 10, "bold"), bd=0, highlightthickness=0)
        self.btn.pack(fill="both", expand=True)
