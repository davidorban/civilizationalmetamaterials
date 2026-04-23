"""Constitutive law: R_eff = β(1−ρ)(1−τ)(1+γρτ).

All functions are fully vectorized via NumPy broadcasting.
"""

import numpy as np
from scipy.optimize import brentq


def r_eff(
    beta: float | np.ndarray,
    rho: float | np.ndarray,
    tau: float | np.ndarray,
    gamma: float | np.ndarray,
) -> float | np.ndarray:
    """Effective reproduction number for unverified decisions.

    Parameters
    ----------
    beta  : Decision branching factor (≥ 1).
    rho   : Provenance fidelity ∈ [0, 1].
    tau   : Verification rate ∈ [0, 1].
    gamma : Provenance–verification synergy (≥ 0).

    Returns
    -------
    R_eff ≥ 0. System is self-healing when R_eff < 1, self-destabilizing when > 1.
    """
    beta = np.asarray(beta, dtype=float)
    rho  = np.asarray(rho,  dtype=float)
    tau  = np.asarray(tau,  dtype=float)
    gamma = np.asarray(gamma, dtype=float)
    return beta * (1.0 - rho) * (1.0 - tau) * (1.0 + gamma * rho * tau)


def tau_star(
    beta: float,
    rho: float,
    gamma: float,
    *,
    tol: float = 1e-10,
) -> float | None:
    """Critical verification rate τ* such that R_eff = 1.

    Returns None if the system cannot be made self-healing at this (β, ρ, γ)
    — i.e. when R_eff(τ=1) ≥ 1 or R_eff(τ=0) ≤ 1.
    """
    f = lambda t: r_eff(beta, rho, t, gamma) - 1.0  # noqa: E731
    r0 = r_eff(beta, rho, 0.0, gamma)
    r1 = r_eff(beta, rho, 1.0, gamma)
    if r0 <= 1.0:
        return 0.0
    if r1 >= 1.0:
        return None
    return float(brentq(f, 0.0, 1.0, xtol=tol))


def phase_boundary(
    beta: float,
    gamma: float,
    grid: np.ndarray,
) -> np.ndarray:
    """τ* values along a ρ grid, vectorized over ρ.

    Parameters
    ----------
    beta  : Decision branching factor.
    gamma : Synergy coefficient.
    grid  : 1-D array of ρ values ∈ [0, 1].

    Returns
    -------
    tau_values : Same shape as *grid*. NaN where no critical τ* exists
                 (system cannot reach R_eff = 1 by increasing τ alone).
    """
    grid = np.asarray(grid, dtype=float)
    out = np.full_like(grid, np.nan)
    for i, rho in enumerate(grid):
        t = tau_star(beta, float(rho), gamma)
        if t is not None:
            out[i] = t
    return out
