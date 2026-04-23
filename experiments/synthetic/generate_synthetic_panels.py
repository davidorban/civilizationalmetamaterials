"""Generate synthetic panel-level datasets for method validation.

Produces plausible stepped-wedge CRT panel outcomes under H0 and H1
so the analysis scripts can be unit-tested end-to-end.

Outputs (in experiments/synthetic/fixtures/):
  panels_h1.csv     — Primary endpoint data (crossing binary outcome)
  panels_h234.csv   — Secondary endpoint data (R_eff estimates, within/cross)

Usage
-----
    python experiments/synthetic/generate_synthetic_panels.py
    python experiments/synthetic/generate_synthetic_panels.py --seed 99
"""

import argparse
import pathlib
import sys

import numpy as np
import pandas as pd

# Allow import from repo root
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "code"))
from cm.constitutive import r_eff

_FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"

# Trial design constants
N_PANELS   = 9
N_COHORTS  = 3
N_PERIODS  = 4
N_REVIEWS  = 20   # per panel-period
BETA       = 10.0
GAMMA      = 1.0


def _treatment_matrix() -> np.ndarray:
    """Returns (N_PANELS, N_PERIODS) binary treatment matrix.

    Stepped-wedge: 3 cohorts of 3 panels each.
    Cohort A crosses at period 2, B at period 3, C at period 4.
    """
    tx = np.zeros((N_PANELS, N_PERIODS), dtype=int)
    for cohort_idx, cross_period in enumerate([1, 2, 3]):  # 0-indexed crossing
        for panel_in_cohort in range(3):
            panel = cohort_idx * 3 + panel_in_cohort
            tx[panel, cross_period:] = 1
    return tx


def generate_h1(rng: np.random.Generator, effect_or: float = 3.0) -> pd.DataFrame:
    """Panel-period binary crossing outcomes under H1 (true positive).

    effect_or: odds ratio of crossing in intervention vs. control.
    """
    tx = _treatment_matrix()
    rows = []
    for panel in range(N_PANELS):
        cohort = chr(ord('A') + panel // 3)
        for period in range(N_PERIODS):
            treatment = int(tx[panel, period])
            # Baseline crossing probability ~20%; intervention raises it
            p_control = 0.20
            p_treat   = p_control * effect_or / (1 - p_control + p_control * effect_or)
            p         = p_treat if treatment else p_control
            crossed   = int(rng.binomial(1, p))
            # Simulate R_eff_hat: control panels near 2.0, treated near 0.7
            rho_base = rng.uniform(0.2, 0.5)
            tau_base = rng.uniform(0.2, 0.5)
            if treatment:
                rho_obs = rng.uniform(0.7, 0.95)
                tau_obs = rng.uniform(0.7, 0.95)
            else:
                rho_obs = rho_base
                tau_obs = tau_base
            r_hat = r_eff(BETA, rho_obs, tau_obs, GAMMA)
            rows.append({
                "panel_id":   f"P{panel+1:03d}",
                "cohort":     cohort,
                "period":     period + 1,
                "treatment":  treatment,
                "rho_hat":    round(rho_obs, 3),
                "tau_hat":    round(tau_obs, 3),
                "r_eff_hat":  round(r_hat, 4),
                "crossed":    crossed,
            })
    return pd.DataFrame(rows)


def generate_h234(rng: np.random.Generator) -> pd.DataFrame:
    """Panel-period R_eff estimates for secondary endpoints (H2, H3, H4).

    Includes within- and cross-panel R_eff estimates to test anisotropy (H3).
    """
    tx = _treatment_matrix()
    rows = []
    for panel in range(N_PANELS):
        cohort = chr(ord('A') + panel // 3)
        for period in range(N_PERIODS):
            treatment = int(tx[panel, period])
            if treatment:
                rho_w = rng.uniform(0.75, 0.95)
                tau_w = rng.uniform(0.75, 0.95)
                rho_c = rng.uniform(0.40, 0.65)  # cross-boundary lower → anisotropic
                tau_c = rng.uniform(0.40, 0.65)
            else:
                rho_w = rho_c = rng.uniform(0.20, 0.45)
                tau_w = tau_c = rng.uniform(0.20, 0.45)
            r_within = r_eff(BETA, rho_w, tau_w, GAMMA)
            r_cross  = r_eff(BETA, rho_c, tau_c, GAMMA)
            rows.append({
                "panel_id":   f"P{panel+1:03d}",
                "cohort":     cohort,
                "period":     period + 1,
                "treatment":  treatment,
                "rho_within": round(rho_w, 3),
                "tau_within": round(tau_w, 3),
                "rho_cross":  round(rho_c, 3),
                "tau_cross":  round(tau_c, 3),
                "r_eff_within": round(r_within, 4),
                "r_eff_cross":  round(r_cross, 4),
            })
    return pd.DataFrame(rows)


def main(seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    _FIXTURES.mkdir(parents=True, exist_ok=True)

    df_h1 = generate_h1(rng)
    df_h1.to_csv(_FIXTURES / "panels_h1.csv", index=False)
    print(f"Written: {_FIXTURES / 'panels_h1.csv'}  ({len(df_h1)} rows)")

    df_h234 = generate_h234(rng)
    df_h234.to_csv(_FIXTURES / "panels_h234.csv", index=False)
    print(f"Written: {_FIXTURES / 'panels_h234.csv'}  ({len(df_h234)} rows)")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    main(args.seed)
