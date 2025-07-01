"""
Environmental Quantum Field Effects (EQFE) Package

A rigorous investigation of environmental scalar field effects on quantum correlations.
"""

__version__ = "1.0.0"
__author__ = "EQFE Research Team"
__email__ = "eqfe@research.org"

from .simulations.core.field_simulator import EnvironmentalFieldSimulator
from .simulations.core.quantum_correlations import CHSHExperimentSimulator

__all__ = [
    "EnvironmentalFieldSimulator",
    "CHSHExperimentSimulator",
]
