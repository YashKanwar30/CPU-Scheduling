# schedulers/sjf.py
from typing import List
from schedulers.base import Scheduler
from core.task import Task
from core.simulation_result import SimulationResult
from evaluation.metrics import evaluate_simulation
import heapq

class SJF(Scheduler):
    name = "SJF"

    def run(self, tasks: List[Task]) -> SimulationResult:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        ready = []
        time = 0
        idx = 0
        timeline = []
        context_switches = 0
        idle_cycles = 0

        while idx < len(tasks) or ready:
            while idx < len(tasks) and tasks[idx].arrival <= time:
                heapq.heappush(ready, (tasks[idx].burst, idx, tasks[idx]))
                idx += 1

            if not ready:
                # CPU idle until next arrival
                next_arrival = tasks[idx].arrival
                idle_cycles += (next_arrival - time)
                timeline.append((time, next_arrival, "IDLE"))
                time = next_arrival
                continue

            _, _, task = heapq.heappop(ready)
            context_switches += 1
            start = time
            end = start + task.burst
            timeline.append((start, end, task.pid))
            task.start_time = start
            task.completion_time = end
            time = end

        return evaluate_simulation(tasks, timeline, context_switches, idle_cycles, self.name)
