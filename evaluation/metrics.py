# evaluation/metrics.py
from typing import List, Tuple, Dict
from core.task import Task
from core.simulation_result import SimulationResult
from evaluation.energy_model import compute_energy, DEFAULT_ENERGY_PARAMS

TimelineEntry = Tuple[int, int, str]

def compute_active_cycles(timeline: List[TimelineEntry]) -> int:
    """Sum total time the CPU was executing non-IDLE entries."""
    total = 0
    for s, e, pid in timeline:
        if pid != "IDLE":
            total += (e - s)
    return total

def evaluate_simulation(tasks: List[Task], timeline: List[TimelineEntry], context_switches: int, idle_cycles: int, scheduler_name: str) -> SimulationResult:
    # Compute per-task metrics
    n = len(tasks)
    total_wait = 0
    total_turnaround = 0
    for task in tasks:
        if task.completion_time is None:
            # Should not happen for well-formed schedulers, but be robust
            task.completion_time = max(t[1] for t in timeline)
        turnaround = task.completion_time - task.arrival
        wait = (task.start_time - task.arrival) if task.start_time is not None else 0
        total_turnaround += turnaround
        total_wait += wait

    avg_wait = total_wait / n if n else 0.0
    avg_turnaround = total_turnaround / n if n else 0.0
    throughput = n / (max(e for _, e, _ in timeline) - min(s for s, _, _ in timeline)) if timeline else 0.0

    active_steps = compute_active_cycles(timeline)
    energy = compute_energy(active_steps, context_switches, idle_cycles, DEFAULT_ENERGY_PARAMS)

    metrics: Dict[str, float] = {
        "avg_wait": avg_wait,
        "avg_turnaround": avg_turnaround,
        "throughput": throughput,
        "total_tasks": n,
        "active_steps": active_steps,
        "timeline_length": max((e for _, e, _ in timeline), default=0)
    }

    return SimulationResult(timeline=timeline, context_switches=context_switches, idle_cycles=idle_cycles, metrics=metrics, energy=energy)
