# ui/main_window.py
import tkinter as tk
from tkinter import ttk
from ui.theme import colors
from ui.panels.input_panel import InputPanel
from ui.panels.chart_panel import ChartPanel
from ui.panels.metrics_panel import MetricsPanel
from core.simulation_engine import SimulationEngine
from schedulers.fcfs import FCFS
from schedulers.sjf import SJF
from schedulers.rr import RoundRobin
from schedulers.priority import PriorityScheduler
from evaluation.energy_model import EnergyParams, DEFAULT_ENERGY_PARAMS
from typing import List
from core.task import Task

from schedulers.energy_aware import EnergyAwareScheduler


def _make_color_map(tasks: List[Task]) -> dict:
    """Create stable mapping from pid to color for Gantt bars."""
    palette = colors.ACCENT_PALETTE
    mapping = {}
    pids = [t.pid for t in tasks]
    unique = list(dict.fromkeys(pids))
    for i, pid in enumerate(unique):
        mapping[pid] = palette[i % len(palette)]
    return mapping

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Energy-Efficient CPU Scheduler — Simulator")
        self.configure(bg=colors.BG_PRIMARY)
        self.geometry("1100x650")
        self.style = ttk.Style(self)
        self._apply_styles()

        # top frame
        top = ttk.Frame(self, style="Panel.TFrame")
        top.pack(fill="both", expand=True, padx=10, pady=(10,6))

        # left input panel
        self.input_panel = InputPanel(top, on_run=self.on_run_request, on_load_sample=self.on_load_sample)
        self.input_panel.pack(side="left", fill="y", padx=(0,8))

        # center chart
        self.chart_panel = ChartPanel(top)
        self.chart_panel.pack(side="left", fill="both", expand=True, padx=(0,8))

        # right metrics
        self.metrics_panel = MetricsPanel(top)
        self.metrics_panel.pack(side="left", fill="y")

        # status bar
        self.status = ttk.Label(self, text="Ready", background=colors.STATUS_BG, foreground=colors.STATUS_TEXT, anchor="w")
        self.status.pack(side="bottom", fill="x")

    def _apply_styles(self):
        self.style.configure("TFrame", background=colors.BG_PRIMARY)
        self.style.configure("Panel.TFrame", background=colors.PANEL_BG)
        self.style.configure("Card.TFrame", background=colors.CARD_BG)
        self.style.configure("TLabel", background=colors.PANEL_BG, foreground=colors.TEXT_PRIMARY)

    def on_load_sample(self):
        # populate sample workload into input panel
        sample = [
            Task(pid="P1", arrival=0, burst=5, priority=2),
            Task(pid="P2", arrival=2, burst=3, priority=1),
            Task(pid="P3", arrival=4, burst=1, priority=3),
            Task(pid="P4", arrival=6, burst=7, priority=2),
        ]
        # clear existing and feed into listbox
        self.input_panel._tasks = []
        self.input_panel.task_listbox.delete(0, "end")
        for t in sample:
            self.input_panel._tasks.append(t)
            self.input_panel.task_listbox.insert("end", f"{t.pid} | arrival={t.arrival} | burst={t.burst} | prio={t.priority}")
        self._set_status("Loaded sample workload.")

    def _set_status(self, text: str):
        self.status.configure(text=text)

    def on_run_request(self, tasks: List[Task], config: dict):
        """
        Main orchestration: run selected scheduler(s) and render results.
        For fairness, each scheduler uses SimulationEngine which clones tasks.
        """
        # set energy params in evaluation module (temporary override)
        from evaluation.energy_model import DEFAULT_ENERGY_PARAMS, EnergyParams
        alpha, beta, gamma = config["alpha"], config["beta"], config["gamma"]
        # patch default params (simple approach)
        DEFAULT_ENERGY_PARAMS = EnergyParams(alpha=alpha, beta=beta, gamma=gamma)
        # update compute_energy calls by monkeypatching if necessary - simpler approach:
        # we'll pass params via evaluate_simulation by temporarily modifying DEFAULT_ENERGY_PARAMS in module
        import importlib, evaluation.energy_model as em
        em.DEFAULT_ENERGY_PARAMS = EnergyParams(alpha=alpha, beta=beta, gamma=gamma)

        algo = config["algorithm"]
        schedulers = []
        if algo == "FCFS":
            schedulers = [FCFS()]
        elif algo == "SJF":
            schedulers = [SJF()]
        elif algo == "RoundRobin":
            schedulers = [RoundRobin(quantum=config.get("quantum", 2))]
        elif algo == "Priority":
            schedulers = [PriorityScheduler()]
        
        elif algo == "EnergyAware":
            schedulers = [EnergyAwareScheduler()]
        else:
            schedulers = [FCFS()]

        # clear UI outputs
        self.metrics_panel.clear()
        # Prebuild color map from tasks to ensure consistent colors
        color_map = _make_color_map(tasks)
        # run each scheduler
        for s in schedulers:
            engine = SimulationEngine(s)
            res = engine.run(tasks)
            # render timeline
            # build a simple pid->color map based on tasks
            self.chart_panel.gantt.draw_timeline(res.timeline, color_map)
            # display metrics
            self.metrics_panel.display_result(s.name, res)
            self._set_status(f"Completed: {s.name} — Energy: {res.energy:.3f}")
