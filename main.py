# main.py
from core.task import Task
from core.simulation_engine import SimulationEngine
from schedulers.fcfs import FCFS
from schedulers.sjf import SJF
from schedulers.rr import RoundRobin
from schedulers.priority import PriorityScheduler

def sample_workload():
    return [
        Task(pid="P1", arrival=0, burst=5, priority=2),
        Task(pid="P2", arrival=2, burst=3, priority=1),
        Task(pid="P3", arrival=4, burst=1, priority=3),
        Task(pid="P4", arrival=6, burst=7, priority=2),
    ]

def run_race(tasks):
    schedulers = [
        FCFS(),
        SJF(),
        RoundRobin(quantum=2),
        PriorityScheduler()
    ]

    results = {}
    for s in schedulers:
        engine = SimulationEngine(s)
        res = engine.run(tasks)
        results[s.name] = res
        print(f"=== {s.name} ===")
        print(f"Energy: {res.energy:.3f}")
        print(f"Avg Wait: {res.metrics['avg_wait']:.3f}, Avg Turnaround: {res.metrics['avg_turnaround']:.3f}")
        print(f"Context Switches: {res.context_switches}, Idle Cycles: {res.idle_cycles}")
        print("Timeline:", res.timeline)
        print()

    return results

if __name__ == "__main__":
    tasks = sample_workload()
    run_race(tasks)
