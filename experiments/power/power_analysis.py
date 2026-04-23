"""Power analysis for the stepped-wedge CRT.

Estimates power to detect H1 (phase-transition crossing) under varying
assumptions about ICC, cluster size, and effect size. Produces
power_curves.pdf when invoked with --out.

Assumptions follow paper §6.2:
  - ICC range: 0.01, 0.05, 0.10, 0.15
  - CV of cluster sizes: 0.3
  - m̄ (mean reviews/period): 20
  - 9 clusters, 4 periods, 3 steps
  - OR = 2.5 as minimum detectable effect

Usage
-----
    python experiments/power/power_analysis.py
    python experiments/power/power_analysis.py --out experiments/power/power_curves.pdf
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

# ── Design constants ──────────────────────────────────────────────────────
N_CLUSTERS  = 9
N_PERIODS   = 4
M_BAR       = 20     # mean reviews per cluster-period
CV          = 0.3    # coefficient of variation of cluster sizes
P0          = 0.20   # baseline crossing probability (control)
ALPHA       = 0.05
ICC_VALS    = [0.01, 0.05, 0.10, 0.15]
OR_VALS     = np.linspace(1.0, 5.0, 100)


def design_effect(icc: float, m: float = M_BAR) -> float:
    """Stepped-wedge design effect (Hussey & Hughes 2007 approximation)."""
    return 1 + (m - 1) * icc


def effective_n(n_clusters: int, n_periods: int, m: float, icc: float) -> float:
    """Effective number of observations after accounting for clustering."""
    total = n_clusters * n_periods * m
    deff  = design_effect(icc, m)
    return total / deff


def power_for_or(or_: float, icc: float, alpha: float = ALPHA) -> float:
    """Approximate power for a log-OR test in a stepped-wedge CRT.

    Uses normal approximation to the test statistic.
    """
    p1  = P0 * or_ / (1 - P0 + P0 * or_)
    n   = effective_n(N_CLUSTERS, N_PERIODS, M_BAR, icc)
    # Pooled SE for log-OR under H0
    p_bar = (P0 + p1) / 2
    se  = np.sqrt(4 / (n * p_bar * (1 - p_bar)))
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta  = abs(np.log(or_)) / se - z_alpha
    return float(stats.norm.cdf(z_beta))


def build_power_table() -> None:
    """Print power for the design-point OR = 2.5 across ICC values."""
    print(f"{'ICC':<8}{'Eff. N':<12}{'Design Effect':<16}{'Power (OR=2.5)'}")
    print("-" * 50)
    for icc in ICC_VALS:
        en  = effective_n(N_CLUSTERS, N_PERIODS, M_BAR, icc)
        de  = design_effect(icc)
        pwr = power_for_or(2.5, icc)
        print(f"{icc:<8.2f}{en:<12.0f}{de:<16.2f}{pwr:.3f}")


def build_fig(out_path: str | None = None) -> None:
    build_power_table()

    colors = ["#1B4F72", "#2E86C1", "#D68910", "#C0392B"]
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.0))

    # Panel A: power curves vs OR
    ax = axes[0]
    for icc, col in zip(ICC_VALS, colors):
        powers = [power_for_or(or_, icc) for or_ in OR_VALS]
        ax.plot(OR_VALS, powers, color=col, label=f"ICC={icc}", linewidth=1.4)
    ax.axhline(0.80, color="k", linestyle="--", linewidth=0.8, label="80% power")
    ax.axvline(2.5,  color="gray", linestyle=":", linewidth=0.8, label="OR=2.5")
    ax.set_xlabel("Odds ratio (treatment vs. control)")
    ax.set_ylabel("Power")
    ax.set_title("Power vs. effect size", fontsize=9)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=7)

    # Panel B: power sensitivity to ICC at OR = 2.5
    ax2 = axes[1]
    icc_range = np.linspace(0.001, 0.25, 200)
    pwr_range = [power_for_or(2.5, icc) for icc in icc_range]
    ax2.plot(icc_range, pwr_range, color="#1B4F72", linewidth=1.4)
    ax2.axhline(0.80, color="k", linestyle="--", linewidth=0.8)
    ax2.axvline(0.05, color="gray", linestyle=":", linewidth=0.8, label="ICC=0.05")
    for icc in ICC_VALS:
        ax2.scatter([icc], [power_for_or(2.5, icc)], s=30, zorder=5, color="#C0392B")
    ax2.set_xlabel("ICC")
    ax2.set_ylabel("Power (OR = 2.5)")
    ax2.set_title("Power sensitivity to ICC", fontsize=9)
    ax2.set_ylim(0, 1)

    plt.tight_layout()
    if out_path:
        fig.savefig(out_path)
        print(f"\nSaved: {out_path}")
    else:
        plt.show()
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="Power analysis for the stepped-wedge CRT.")
    p.add_argument("--out", default=None, help="Output PDF path for power curves.")
    args = p.parse_args()
    build_fig(args.out)


if __name__ == "__main__":
    main()
