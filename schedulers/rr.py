# schedulers/round_robin.py
from typing import List, Deque
from collections import deque
from schedulers.base import Scheduler
from core.task import Task
from core.simulation_result import SimulationResult
from evaluation.metrics import evaluate_simulation

class RoundRobin(Scheduler):
    name = "RoundRobin"

    def __init__(self, quantum: int = 2):
        self.quantum = quantum

    def run(self, tasks: List[Task]) -> SimulationResult:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        time = 0
        idx = 0
        ready: Deque[Task] = deque()
        timeline = []
        context_switches = 0
        idle_cycles = 0

        while idx < len(tasks) or ready:
            while idx < len(tasks) and tasks[idx].arrival <= time:
                ready.append(tasks[idx])
                idx += 1

            if not ready:
                next_arrival = tasks[idx].arrival
                idle_cycles += (next_arrival - time)
                timeline.append((time, next_arrival, "IDLE"))
                time = next_arrival
                continue

            task = ready.popleft()
            context_switches += 1
            start = time
            run_for = min(self.quantum, task.remaining)
            end = start + run_for
            timeline.append((start, end, task.pid))
            if task.start_time is None:
                task.start_time = start
            task.remaining -= run_for
            time = end

            # Push newly arrived tasks during quantum
            while idx < len(tasks) and tasks[idx].arrival <= time:
                ready.append(tasks[idx])
                idx += 1

            if task.remaining > 0:
                ready.append(task)
            else:
                task.completion_time = time

        return evaluate_simulation(tasks, timeline, context_switches, idle_cycles, self.name)
