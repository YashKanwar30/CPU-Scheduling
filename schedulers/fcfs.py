# schedulers/fcfs.py
from typing import List
from schedulers.base import Scheduler
from core.task import Task
from core.simulation_result import SimulationResult
from evaluation.metrics import evaluate_simulation

class FCFS(Scheduler):
    name = "FCFS"

    def run(self, tasks: List[Task]) -> SimulationResult:
        tasks = sorted(tasks, key=lambda t: (t.arrival, t.pid))
        time = 0
        timeline = []
        context_switches = 0
        idle_cycles = 0

        for task in tasks:
            if time < task.arrival:
                idle_cycles += (task.arrival - time)
                timeline.append((time, task.arrival, "IDLE"))
                time = task.arrival

            # context switch (count when switching from IDLE or another task)
            context_switches += 1
            start = time
            end = start + task.burst
            timeline.append((start, end, task.pid))
            task.start_time = start
            task.completion_time = end
            time = end

        return evaluate_simulation(tasks, timeline, context_switches, idle_cycles, self.name)
