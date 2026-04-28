# ui/panels/input_panel.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

from ui.components.labeled_entry import LabeledEntry
from ui.components.buttons import ActionButton
from ui.components.card import Card
from core.task import Task
from typing import Callable, List
from ui.theme import colors


class InputPanel(ttk.Frame):
    """
    Left-side panel: add tasks manually, generate random tasks,
    select algorithm, set quantum, set energy params, and run.
    """

    def __init__(self, parent, on_run: Callable, on_load_sample: Callable, **kwargs):
        super().__init__(parent, style="Panel.TFrame", **kwargs)

        self.on_run = on_run
        self.on_load_sample = on_load_sample

        # -----------------------------------------
        #  TASK CREATION CARD
        # -----------------------------------------
        self.card = Card(self)
        self.card.pack(fill="x", padx=8, pady=8)

        ttk.Label(
            self.card,
            text="Add Task",
            foreground=colors.TEXT_PRIMARY,
            background=colors.PANEL_BG
        ).pack(anchor="w")

        row = ttk.Frame(self.card)
        row.pack(fill="x", pady=(6, 0))

        self.entry_pid = LabeledEntry(row, "PID", width=6)
        self.entry_pid.grid(row=0, column=0, padx=4)

        self.entry_arrival = LabeledEntry(row, "Arrival", width=6)
        self.entry_arrival.grid(row=0, column=1, padx=4)

        self.entry_burst = LabeledEntry(row, "Burst", width=6)
        self.entry_burst.grid(row=0, column=2, padx=4)

        self.entry_priority = LabeledEntry(row, "Priority", width=6)
        self.entry_priority.grid(row=0, column=3, padx=4)

        add_btn = ActionButton(self.card, text="Add Task", command=self._add_task)
        add_btn.pack(fill="x", pady=(8, 0))

        # -----------------------------------------
        # TASK LIST CARD
        # -----------------------------------------
        self.task_list_card = Card(self)
        self.task_list_card.pack(fill="both", expand=True, padx=8, pady=4)

        ttk.Label(
            self.task_list_card,
            text="Current Tasks",
            foreground=colors.TEXT_PRIMARY,
            background=colors.PANEL_BG
        ).pack(anchor="w")

        self.task_listbox = tk.Listbox(
            self.task_list_card,
            height=10,
            bg=colors.CARD_BG,
            fg=colors.TEXT_PRIMARY
        )
        self.task_listbox.pack(fill="both", expand=True, padx=4, pady=6)

        # Internal storage
        self._tasks: List[Task] = []

        # -----------------------------------------
        # SCHEDULER SELECTION
        # -----------------------------------------
        ctrl_card = Card(self)
        ctrl_card.pack(fill="x", padx=8, pady=4)

        ttk.Label(
            ctrl_card,
            text="Scheduler",
            foreground=colors.TEXT_PRIMARY,
            background=colors.PANEL_BG
        ).pack(anchor="w")

        self.algo_var = tk.StringVar(value="FCFS")
        self.algo_menu = ttk.Combobox(
            ctrl_card,
            textvariable=self.algo_var,
            values=[
                "FCFS",
                "SJF",
                "RoundRobin",
                "Priority",
                "SRTF",
                "EnergyAware"
            ],
            state="readonly"
        )
        self.algo_menu.pack(fill="x", pady=4)

        # QUANTUM (Visible always for simplicity)
        qframe = ttk.Frame(ctrl_card)
        qframe.pack(fill="x", pady=4)

        ttk.Label(
            qframe,
            text="Quantum:",
            foreground=colors.TEXT_PRIMARY,
            background=colors.PANEL_BG
        ).pack(side="left")

        self.quantum_var = tk.IntVar(value=2)
        self.quantum_spin = ttk.Spinbox(
            qframe,
            from_=1,
            to=20,
            width=4,
            textvariable=self.quantum_var
        )
        self.quantum_spin.pack(side="left", padx=6)

        # -----------------------------------------
        # ENERGY PARAMETERS
        # -----------------------------------------
        energy_card = Card(self)
        energy_card.pack(fill="x", padx=8, pady=4)

        ttk.Label(
            energy_card,
            text="Energy Parameters",
            foreground=colors.TEXT_PRIMARY,
            background=colors.PANEL_BG
        ).pack(anchor="w")

        # Sliders for α, β, γ
        self.alpha_var = tk.DoubleVar(value=1.0)
        self.beta_var = tk.DoubleVar(value=0.5)
        self.gamma_var = tk.DoubleVar(value=0.2)

        ttk.Label(energy_card, text="α (active):", background=colors.PANEL_BG, foreground=colors.TEXT_PRIMARY).pack(anchor="w")
        ttk.Scale(energy_card, variable=self.alpha_var, from_=0.1, to=5.0, orient="horizontal").pack(fill="x")

        ttk.Label(energy_card, text="β (context):", background=colors.PANEL_BG, foreground=colors.TEXT_PRIMARY).pack(anchor="w")
        ttk.Scale(energy_card, variable=self.beta_var, from_=0.0, to=3.0, orient="horizontal").pack(fill="x")

        ttk.Label(energy_card, text="γ (idle):", background=colors.PANEL_BG, foreground=colors.TEXT_PRIMARY).pack(anchor="w")
        ttk.Scale(energy_card, variable=self.gamma_var, from_=0.0, to=1.0, orient="horizontal").pack(fill="x")

        # -----------------------------------------
        # BUTTONS: RUN / SAMPLE / RANDOM GENERATION
        # -----------------------------------------
        run_card = Card(self)
        run_card.pack(fill="x", padx=8, pady=4)

        run_btn = ActionButton(run_card, text="▶ Run Simulation", command=self._run)
        run_btn.pack(fill="x", pady=(0, 6))

        sample_btn = ActionButton(run_card, text="Load Sample Workload", command=self._load_sample)
        sample_btn.pack(fill="x")

        gen_btn = ActionButton(run_card, text="Generate Random Tasks", command=self._generate_random)
        gen_btn.pack(fill="x", pady=(6, 0))


    # =========================================================
    #     INTERNAL METHODS
    # =========================================================

    def _add_task(self):
        pid = self.entry_pid.var.get().strip()

        if not pid:
            messagebox.showerror("Error", "PID cannot be empty.")
            return

        try:
            arr = int(self.entry_arrival.var.get())
            burst = int(self.entry_burst.var.get())
            prio = int(self.entry_priority.var.get() or 0)
        except ValueError:
            messagebox.showerror("Error", "Arrival, Burst, Priority must be integers.")
            return

        t = Task(pid=pid, arrival=arr, burst=burst, priority=prio)
        self._tasks.append(t)
        self.task_listbox.insert("end", f"{pid} | arrival={arr} | burst={burst} | prio={prio}")

        # clear fields
        self.entry_pid.var.set("")
        self.entry_arrival.var.set("")
        self.entry_burst.var.set("")
        self.entry_priority.var.set("")

    def _generate_random(self):
        """Generate N random tasks with reasonable ranges."""
        count = simpledialog.askinteger(
            "Generate Tasks",
            "How many random tasks?",
            minvalue=1,
            maxvalue=300
        )
        if not count:
            return

        self._tasks.clear()
        self.task_listbox.delete(0, "end")

        for i in range(count):
            pid = f"P{i+1}"
            arrival = random.randint(0, 30)
            burst = random.randint(1, 15)
            prio = random.randint(1, 5)

            t = Task(pid=pid, arrival=arrival, burst=burst, priority=prio)
            self._tasks.append(t)
            self.task_listbox.insert("end", f"{pid} | arrival={arrival} | burst={burst} | prio={prio}")

    def _run(self):
        """Package tasks + config and send to main window."""
        tasks_copy = [Task(t.pid, t.arrival, t.burst, t.priority) for t in self._tasks]

        config = {
            "algorithm": self.algo_var.get(),
            "quantum": self.quantum_var.get(),
            "alpha": self.alpha_var.get(),
            "beta": self.beta_var.get(),
            "gamma": self.gamma_var.get(),
        }

        self.on_run(tasks_copy, config)

    def _load_sample(self):
        self.on_load_sample()
