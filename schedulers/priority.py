# schedulers/priority_nonpreemptive.py
from typing import List
import heapq
from schedulers.base import Scheduler
from core.task import Task
from core.simulation_result import SimulationResult
from evaluation.metrics import evaluate_simulation

class PriorityScheduler(Scheduler):
    name = "Priority"

    def run(self, tasks: List[Task]) -> SimulationResult:
        tasks = sorted(tasks, key=lambda t: t.arrival)
        idx = 0
        time = 0
        ready = []
        timeline = []
        context_switches = 0
        idle_cycles = 0

        while idx < len(tasks) or ready:
            while idx < len(tasks) and tasks[idx].arrival <= time:
                # lower number -> higher priority (adjust as you wish)
                heapq.heappush(ready, (tasks[idx].priority, idx, tasks[idx]))
                idx += 1

            if not ready:
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
