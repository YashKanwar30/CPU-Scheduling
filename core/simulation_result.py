# core/simulation_result.py
from dataclasses import dataclass
from typing import List, Tuple, Dict

# timeline entries: (start_time, end_time, pid) - end_time is exclusive
TimelineEntry = Tuple[int, int, str]

@dataclass
class SimulationResult:
    timeline: List[TimelineEntry]
    context_switches: int
    idle_cycles: int
    metrics: Dict[str, float]
    energy: float
