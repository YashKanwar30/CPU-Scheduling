# evaluation/energy_model.py
from typing import NamedTuple

class EnergyParams(NamedTuple):
    alpha: float  # cost per active CPU time unit
    beta: float   # cost per context switch
    gamma: float  # cost per idle cycle

# Default weights; you may tune these or expose them as UI controls.
DEFAULT_ENERGY_PARAMS = EnergyParams(alpha=1.0, beta=0.5, gamma=0.2)

def compute_energy(active_steps: int, context_switches: int, idle_cycles: int, params: EnergyParams = DEFAULT_ENERGY_PARAMS) -> float:
    """
    Simple linear energy model:
      E = alpha * active_steps + beta * context_switches + gamma * idle_cycles
    """
    return params.alpha * active_steps + params.beta * context_switches + params.gamma * idle_cycles
