# schedulers/base.py
from typing import List
from core.task import Task
from core.simulation_result import SimulationResult

class Scheduler:
    """
    Base scheduler interface. Implementations must run on a list of Task clones
    and return a SimulationResult describing the execution.
    """
    name = "BaseScheduler"

    def run(self, tasks: List[Task]) -> SimulationResult:
        raise NotImplementedError("Scheduler subclasses must implement run()")
