"""Directional coordination model for H3 (anisotropy).

Models a two-unit system where R_eff decomposes into within-unit and
cross-boundary components via a 2×2 coordination tensor.

Reference: paper §5, §6.1 H3.
"""

from __future__ import annotations

import numpy as np
from .constitutive import r_eff


def coordination_tensor(
    beta: float,
    rho_w: float,
    tau_w: float,
    rho_c: float,
    tau_c: float,
    gamma: float,
) -> np.ndarray:
    """2×2 coordination tensor for a two-unit system.

    Diagonal entries are within-unit R_eff; off-diagonal are cross-boundary R_eff.

    Parameters
    ----------
    rho_w, tau_w : Provenance fidelity and verification rate for within-unit flows.
    rho_c, tau_c : Same for cross-boundary flows.
    beta, gamma  : Shared branching factor and synergy.

    Returns
    -------
    T : (2, 2) float array.
    """
    r_within = r_eff(beta, rho_w, tau_w, gamma)
    r_cross  = r_eff(beta, rho_c, tau_c, gamma)
    return np.array([[r_within, r_cross],
                     [r_cross,  r_within]])


def anisotropy_index(tensor: np.ndarray) -> float:
    """Scalar anisotropy: |R_within − R_cross| / (R_within + R_cross).

    Returns 0 for isotropic systems, 1 for maximally anisotropic.
    """
    r_w = tensor[0, 0]
    r_c = tensor[0, 1]
    denom = r_w + r_c
    if denom == 0.0:
        return 0.0
    return abs(r_w - r_c) / denom


def sweep_cross_boundary(
    beta: float,
    gamma: float,
    rho_w: float = 0.7,
    tau_w: float = 0.7,
    n_points: int = 100,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Sweep cross-boundary (ρ_c, τ_c) jointly from 0 to (ρ_w, τ_w).

    Returns ρ_c, τ_c grids and anisotropy index at each point.
    """
    rho_c_vals = np.linspace(0.0, rho_w, n_points)
    tau_c_vals = np.linspace(0.0, tau_w, n_points)
    rho_c_grid, tau_c_grid = np.meshgrid(rho_c_vals, tau_c_vals)
    ai = np.vectorize(
        lambda rc, tc: anisotropy_index(
            coordination_tensor(beta, rho_w, tau_w, rc, tc, gamma)
        )
    )(rho_c_grid, tau_c_grid)
    return rho_c_grid, tau_c_grid, ai
