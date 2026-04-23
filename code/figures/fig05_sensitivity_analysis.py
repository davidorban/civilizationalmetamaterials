"""Figure 5: Sensitivity Analysis.

OAT sweeps and Sobol first-order / total indices for R_eff.
Reproduces figures/fig05-sensitivity-analysis.pdf from source.

Usage
-----
    python code/figures/fig05_sensitivity_analysis.py
    python code/figures/fig05_sensitivity_analysis.py --out figures/fig05-sensitivity-analysis.pdf
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cm.sensitivity import oat_sweep, sobol_indices, DEFAULT_PROBLEM, DEFAULT_BASE
from cm.constitutive import tau_star
from cm.plotting import (apply_lncs_style, DARK_BLUE, SEC_BLUE, AMBER, RED,
                          LNCS_FULL_W, LNCS_ASPECT)


# β=10, γ values from paper §7.3 (r3 correction)
BETA     = 10.0
GAMMAS   = [0.0, 0.5, 1.0, 2.0]
GAMMA_LBL = {0.0: "γ=0", 0.5: "γ=0.5", 1.0: "γ=1", 2.0: "γ=2"}
COLORS   = [DARK_BLUE, SEC_BLUE, AMBER, RED]


def build_fig(out_path: str | None = None, sobol_n: int = 512) -> None:
    apply_lncs_style()

    fig = plt.figure(figsize=(LNCS_FULL_W, LNCS_FULL_W * 1.4))
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ── Panel A: OAT sweep of τ for multiple γ ───────────────────────────
    ax_a = fig.add_subplot(gs[0, :])
    for gamma, col in zip(GAMMAS, COLORS):
        x, r = oat_sweep("tau", base={**DEFAULT_BASE, "beta": BETA, "gamma": gamma})
        ax_a.plot(x, r, color=col, label=GAMMA_LBL[gamma], linewidth=1.2)
    ax_a.axhline(1.0, color="k", linestyle="--", linewidth=0.8, label=r"$R_\mathrm{eff}=1$")
    ax_a.set_xlabel(r"Verification rate $\tau$")
    ax_a.set_ylabel(r"$R_\mathrm{eff}$")
    ax_a.set_title(r"OAT sweep: $\tau$ with $\beta=10$, $\rho=0.5$", fontsize=9)
    ax_a.legend(fontsize=7, ncol=2)
    ax_a.set_xlim(0, 1)

    # ── Panel B: OAT sweep of ρ ──────────────────────────────────────────
    ax_b = fig.add_subplot(gs[1, 0])
    for gamma, col in zip(GAMMAS, COLORS):
        x, r = oat_sweep("rho", base={**DEFAULT_BASE, "beta": BETA, "gamma": gamma})
        ax_b.plot(x, r, color=col, label=GAMMA_LBL[gamma], linewidth=1.2)
    ax_b.axhline(1.0, color="k", linestyle="--", linewidth=0.8)
    ax_b.set_xlabel(r"Provenance fidelity $\rho$")
    ax_b.set_ylabel(r"$R_\mathrm{eff}$")
    ax_b.set_title(r"OAT: $\rho$", fontsize=9)
    ax_b.set_xlim(0, 1)

    # ── Panel C: Critical τ* vs ρ for multiple γ ─────────────────────────
    ax_c = fig.add_subplot(gs[1, 1])
    rho_grid = np.linspace(0.01, 0.99, 200)
    for gamma, col in zip(GAMMAS, COLORS):
        ts = np.array([tau_star(BETA, float(r), gamma) or np.nan for r in rho_grid])
        ax_c.plot(rho_grid, ts, color=col, label=GAMMA_LBL[gamma], linewidth=1.2)
    ax_c.set_xlabel(r"Provenance fidelity $\rho$")
    ax_c.set_ylabel(r"Critical $\tau^*$")
    ax_c.set_title(r"Design threshold $\tau^*(\rho)$", fontsize=9)
    ax_c.set_xlim(0, 1)
    ax_c.set_ylim(0, 1)

    # ── Panel D+E: Sobol indices ──────────────────────────────────────────
    ax_d = fig.add_subplot(gs[2, 0])
    ax_e = fig.add_subplot(gs[2, 1])

    try:
        si = sobol_indices(n_samples=sobol_n, seed=42)
        names = si["names"]
        x_pos = np.arange(len(names))
        ax_d.bar(x_pos, si["S1"], yerr=si["S1_conf"], color=SEC_BLUE,
                 capsize=3, width=0.5)
        ax_d.set_xticks(x_pos)
        ax_d.set_xticklabels(
            [r"$\beta$", r"$\rho$", r"$\tau$", r"$\gamma$"], fontsize=8)
        ax_d.set_ylabel("First-order index $S_1$")
        ax_d.set_title("Sobol $S_1$", fontsize=9)
        ax_d.set_ylim(0, 1)

        ax_e.bar(x_pos, si["ST"], yerr=si["ST_conf"], color=RED,
                 capsize=3, width=0.5)
        ax_e.set_xticks(x_pos)
        ax_e.set_xticklabels(
            [r"$\beta$", r"$\rho$", r"$\tau$", r"$\gamma$"], fontsize=8)
        ax_e.set_ylabel("Total index $S_T$")
        ax_e.set_title("Sobol $S_T$", fontsize=9)
        ax_e.set_ylim(0, 1)
    except Exception as e:
        ax_d.text(0.5, 0.5, f"SALib error:\n{e}", transform=ax_d.transAxes,
                  ha="center", va="center", fontsize=7)
        ax_e.set_visible(False)

    if out_path:
        fig.savefig(out_path)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce Figure 5 (sensitivity analysis).")
    p.add_argument("--out", default=None, help="Output PDF path.")
    p.add_argument("--sobol-n", type=int, default=512,
                   help="Saltelli base sample count (actual = n*(k+2)).")
    args = p.parse_args()
    build_fig(args.out, sobol_n=args.sobol_n)


if __name__ == "__main__":
    main()
