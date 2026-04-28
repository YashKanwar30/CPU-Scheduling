# core/task.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    pid: str
    arrival: int
    burst: int
    priority: int = 0
    remaining: int = field(init=False)
    start_time: Optional[int] = None
    completion_time: Optional[int] = None

    def __post_init__(self):
        self.remaining = self.burst

    def clone(self) -> "Task":
        """Return a shallow copy suitable for independent simulations."""
        t = Task(self.pid, self.arrival, self.burst, self.priority)
        return t
