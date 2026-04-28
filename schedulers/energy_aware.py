# schedulers/energy_aware.py
from typing import List
import heapq
from schedulers.base import Scheduler
from core.task import Task
from core.simulation_result import SimulationResult
from evaluation.metrics import evaluate_simulation

class EnergyAwareScheduler(Scheduler):
    name = "EnergyAware"

    def __init__(self, switch_penalty=2, idle_penalty=1):
        self.switch_penalty = switch_penalty
        self.idle_penalty = idle_penalty

    def run(self, tasks: List[Task]) -> SimulationResult:
        # Sort tasks by arrival
        tasks = sorted(tasks, key=lambda t: t.arrival)
        n = len(tasks)
        idx = 0
        time = 0

        # Ready queue is a min-heap based on score
        ready = []
        timeline = []
        context_switches = 0
        idle_cycles = 0
        current = None
        current_start = None

        def score(task: Task):
            # energy-based score:
            # weight short tasks slightly more
            return (0.6 * task.remaining +
                    0.3 * self.switch_penalty +
                    0.1 * self.idle_penalty)

        while idx < n or ready or current:
            # Add arriving tasks
            while idx < n and tasks[idx].arrival <= time:
                heapq.heappush(ready, (score(tasks[idx]), idx, tasks[idx]))
                idx += 1

            if current is None:
                # CPU idle
                if not ready:
                    if idx < n:
                        next_arr = tasks[idx].arrival
                        idle_cycles += (next_arr - time)
                        timeline.append((time, next_arr, "IDLE"))
                        time = next_arr
                        continue
                else:
                    _, _, current = heapq.heappop(ready)
                    current_start = time
                    if current.start_time is None:
                        current.start_time = time
                    context_switches += 1

            # Predict next arrival
            next_arrival = tasks[idx].arrival if idx < n else None
            finish_time = time + current.remaining

            if next_arrival is None or next_arrival >= finish_time:
                # Execute fully
                timeline.append((time, finish_time, current.pid))
                time = finish_time
                current.remaining = 0
                current.completion_time = time
                current = None
                current_start = None
            else:
                # Execute until arrival
                run_for = next_arrival - time
                timeline.append((time, next_arrival, current.pid))
                current.remaining -= run_for
                time = next_arrival
                # New tasks arrive, and preemption check happens next loop

        return evaluate_simulation(tasks, timeline, context_switches, idle_cycles, self.name)
