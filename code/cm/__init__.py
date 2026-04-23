"""Civilizational Metamaterials — reference implementation."""
from .constitutive import r_eff, tau_star, phase_boundary
from .branching import simulate

__all__ = ["r_eff", "tau_star", "phase_boundary", "simulate"]
