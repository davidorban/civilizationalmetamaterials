"""Sensitivity analysis for R_eff.

Provides one-at-a-time (OAT) sweeps and Sobol first-order + total indices
via SALib. Used by figures/fig05_sensitivity_analysis.py.
"""

from __future__ import annotations

import numpy as np
try:
    from SALib.sample.sobol import sample as sobol_sample   # SALib >= 1.5.1
except ImportError:
    from SALib.sample.saltelli import sample as sobol_sample  # SALib < 1.5.1
from SALib.analyze import sobol

from .constitutive import r_eff


# Default parameter bounds for sensitivity analysis (matching paper §7.3)
DEFAULT_PROBLEM = {
    "num_vars": 4,
    "names": ["beta", "rho", "tau", "gamma"],
    "bounds": [[1, 50], [0, 1], [0, 1], [0, 3]],
}

# Design point used in OAT sweeps (β=10, γ=1, from paper)
DEFAULT_BASE = {"beta": 10.0, "rho": 0.5, "tau": 0.5, "gamma": 1.0}


def oat_sweep(
    param: str,
    n_points: int = 200,
    base: dict | None = None,
    problem: dict | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """One-at-a-time sweep of *param*, holding all others at their base value.

    Returns
    -------
    x_vals : Parameter values swept.
    r_vals : Corresponding R_eff values.
    """
    b = {**(base or DEFAULT_BASE)}
    p = problem or DEFAULT_PROBLEM
    idx = p["names"].index(param)
    lo, hi = p["bounds"][idx]
    x_vals = np.linspace(lo, hi, n_points)
    r_vals = np.array([
        r_eff(**{**b, param: float(x)}) for x in x_vals
    ])
    return x_vals, r_vals


def sobol_indices(
    n_samples: int = 1024,
    problem: dict | None = None,
    seed: int = 42,
) -> dict:
    """Compute Sobol first-order (S1) and total (ST) sensitivity indices.

    Parameters
    ----------
    n_samples : Base sample count (actual samples = n_samples * (num_vars + 2)).
    problem   : SALib problem dict (default: 4-parameter default).
    seed      : RNG seed for Saltelli sampler.

    Returns
    -------
    dict with keys 'S1', 'ST', 'S1_conf', 'ST_conf', 'names'.
    """
    prob = problem or DEFAULT_PROBLEM
    np.random.seed(seed)
    param_values = sobol_sample(prob, n_samples, calc_second_order=False)
    Y = np.array([
        r_eff(row[0], row[1], row[2], row[3]) for row in param_values
    ])
    Si = sobol.analyze(prob, Y, calc_second_order=False, print_to_console=False)
    return {
        "names":   prob["names"],
        "S1":      Si["S1"],
        "ST":      Si["ST"],
        "S1_conf": Si["S1_conf"],
        "ST_conf": Si["ST_conf"],
    }
