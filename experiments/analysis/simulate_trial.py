"""End-to-end trial simulator under null and alternative hypotheses.

Runs Monte Carlo over the full 12-week stepped-wedge design.
Reports type-I error, power, and bias of the primary-endpoint estimator.

Usage
-----
    python experiments/analysis/simulate_trial.py
    python experiments/analysis/simulate_trial.py --n-sims 1000 --effect-or 2.5
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

# ── Design ─────────────────────────────────────────────────────────────────
N_CLUSTERS = 9
N_PERIODS  = 4
P0_BASE    = 0.20   # baseline crossing probability
ICC        = 0.05
ALPHA      = 0.05


def _treatment_matrix() -> np.ndarray:
    tx = np.zeros((N_CLUSTERS, N_PERIODS), dtype=int)
    for cohort_idx, cp in enumerate([1, 2, 3]):
        for pi in range(3):
            panel = cohort_idx * 3 + pi
            tx[panel, cp:] = 1
    return tx


def _or_to_p1(p0: float, or_: float) -> float:
    return p0 * or_ / (1 - p0 + p0 * or_)


def _simulate_one(rng: np.random.Generator, or_: float) -> float:
    """Simulate one trial. Returns the treatment log-OR estimate."""
    tx = _treatment_matrix()
    records = []
    u = rng.normal(0, np.sqrt(ICC), N_CLUSTERS)  # cluster random effects

    for panel in range(N_CLUSTERS):
        for period in range(N_PERIODS):
            p_base = P0_BASE + 0.05 * u[panel]  # random cluster baseline
            p_base = max(0.01, min(0.99, p_base))
            p = _or_to_p1(p_base, or_) if tx[panel, period] else p_base
            p = max(0.01, min(0.99, p))
            records.append({
                "treatment": tx[panel, period],
                "period":    period,
                "crossed":   rng.binomial(1, p),
            })

    df = pd.DataFrame(records)
    n1 = df[df["treatment"] == 1]
    n0 = df[df["treatment"] == 0]
    p1_hat = n1["crossed"].mean() if len(n1) > 0 else 0.5
    p0_hat = n0["crossed"].mean() if len(n0) > 0 else 0.5
    p1_hat = np.clip(p1_hat, 0.001, 0.999)
    p0_hat = np.clip(p0_hat, 0.001, 0.999)
    return np.log(p1_hat / (1 - p1_hat)) - np.log(p0_hat / (1 - p0_hat))


def run_simulation(n_sims: int, or_: float, seed: int = 42) -> dict:
    rng = np.random.default_rng(seed)
    true_log_or = np.log(or_)
    estimates = np.array([_simulate_one(rng, or_) for _ in range(n_sims)])

    # Wald test: reject if |estimate / SE| > z_{α/2}
    se_est = np.std(estimates, ddof=1)
    z_stats = estimates / (se_est + 1e-10)
    rejections = np.mean(np.abs(z_stats) > stats.norm.ppf(1 - ALPHA / 2))

    return {
        "n_sims":       n_sims,
        "or":           or_,
        "true_log_or":  true_log_or,
        "mean_estimate": float(np.mean(estimates)),
        "bias":          float(np.mean(estimates) - true_log_or),
        "se":            float(se_est),
        "rejection_rate": float(rejections),
        "type_I_or_power": "power" if or_ > 1.0 else "type-I error",
    }


def main() -> None:
    p = argparse.ArgumentParser(description="End-to-end trial simulator.")
    p.add_argument("--n-sims",    type=int,   default=500,  help="Monte Carlo replications")
    p.add_argument("--effect-or", type=float, default=2.5,  help="True OR under alternative")
    p.add_argument("--seed",      type=int,   default=42)
    args = p.parse_args()

    print(f"Running {args.n_sims} simulations per scenario (seed={args.seed})")
    print("=" * 60)

    for or_val, label in [(1.0, "H0 (null)"), (args.effect_or, "H1 (alternative)")]:
        r = run_simulation(args.n_sims, or_val, args.seed)
        print(f"\nScenario: {label}  (OR = {or_val})")
        print(f"  Mean log-OR estimate:  {r['mean_estimate']:.3f}  (true: {r['true_log_or']:.3f})")
        print(f"  Bias:                  {r['bias']:.3f}")
        print(f"  SE of estimates:       {r['se']:.3f}")
        print(f"  {r['type_I_or_power']:15}: {r['rejection_rate']:.3f}")


if __name__ == "__main__":
    main()
