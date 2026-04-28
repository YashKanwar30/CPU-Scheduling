# core/simulation_engine.py
from typing import List
from core.task import Task
from schedulers.base import Scheduler
from core.simulation_result import SimulationResult
import copy

class SimulationEngine:
    """
    Runs one Scheduler on a *fresh clone* of the provided task list to ensure
    fairness when comparing multiple schedulers.
    """
    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler

    def run(self, tasks: List[Task]) -> SimulationResult:
        # Clone tasks so each run is independent
        tasks_clone = [t.clone() for t in tasks]
        return self.scheduler.run(tasks_clone)
