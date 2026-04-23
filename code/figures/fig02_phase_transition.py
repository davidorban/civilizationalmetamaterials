"""Figure 2: Phase Transition Diagram.

R_eff = β(1−ρ)(1−τ)(1+γρτ) with β=10, γ=1.
Reproduces figures/fig02-phase-transition.pdf from source.

Usage
-----
    python code/figures/fig02_phase_transition.py
    python code/figures/fig02_phase_transition.py --out figures/fig02-phase-transition.pdf
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import TwoSlopeNorm

# Allow running from repo root or from code/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cm.constitutive import r_eff, phase_boundary
from cm.plotting import apply_lncs_style, DARK_BLUE, RED, LNCS_FULL_W, LNCS_ASPECT


BETA  = 10.0
GAMMA = 1.0
GRID  = 300


def build_fig(out_path: str | None = None) -> None:
    apply_lncs_style()

    rho_v = np.linspace(0, 1, GRID)
    tau_v = np.linspace(0, 1, GRID)
    RHO, TAU = np.meshgrid(rho_v, tau_v)
    Z = r_eff(BETA, RHO, TAU, GAMMA)

    fig, ax = plt.subplots(figsize=(LNCS_FULL_W, LNCS_FULL_W * LNCS_ASPECT))

    norm = TwoSlopeNorm(vcenter=1.0, vmin=0, vmax=float(Z.max()))
    cf = ax.contourf(RHO, TAU, Z, levels=256, cmap="RdBu_r", norm=norm)

    # Phase boundary R_eff = 1
    pb = phase_boundary(BETA, GAMMA, rho_v)
    valid = ~np.isnan(pb)
    ax.plot(rho_v[valid], pb[valid], "k-", linewidth=1.5, label=r"$R_\mathrm{eff}=1$")

    # Region labels
    ax.text(0.12, 0.15, "Turbulent\n" r"$R_\mathrm{eff}>1$",
            ha="center", va="center", fontsize=8, color="white", fontweight="bold")
    ax.text(0.75, 0.75, "Damped\n" r"$R_\mathrm{eff}<1$",
            ha="center", va="center", fontsize=8, color=DARK_BLUE, fontweight="bold")

    # Marker points (Low, Mid, High from paper)
    markers = [
        (0.1, 0.1, "Low"),
        (0.5, 0.5, "Mid"),
        (0.85, 0.85, "High"),
    ]
    for rx, tx, lbl in markers:
        ax.scatter(rx, tx, s=30, color="k", zorder=5)
        ax.annotate(lbl, (rx, tx), xytext=(rx + 0.05, tx - 0.05),
                    fontsize=7, ha="left")

    cbar = fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r"$R_\mathrm{eff}$", fontsize=8)
    cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))

    ax.set_xlabel(r"Provenance fidelity $\rho$")
    ax.set_ylabel(r"Verification rate $\tau$")
    ax.set_title(fr"Phase transition ($\beta={BETA:.0f}$, $\gamma={GAMMA:.0f}$)", fontsize=9)
    ax.legend(loc="upper left", fontsize=7)

    # Inset: critical τ* for multiple β values
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    axins = inset_axes(ax, width="38%", height="38%", loc="lower right",
                       bbox_to_anchor=(-0.02, 0.02, 1, 1),
                       bbox_transform=ax.transAxes)
    rho_ins = np.linspace(0, 1, 200)
    for b, ls in [(5, "--"), (10, "-"), (50, ":")]:
        pb_ins = phase_boundary(b, GAMMA, rho_ins)
        m = ~np.isnan(pb_ins)
        axins.plot(rho_ins[m], pb_ins[m], ls, linewidth=1,
                   label=rf"$\beta={b}$", color="k")
    axins.set_xlim(0, 1)
    axins.set_ylim(0, 1)
    axins.tick_params(labelsize=6)
    axins.set_xlabel(r"$\rho$", fontsize=6)
    axins.set_ylabel(r"$\tau^*$", fontsize=6)
    axins.legend(fontsize=5, loc="upper right")

    plt.tight_layout()
    if out_path:
        fig.savefig(out_path)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce Figure 2 (phase transition).")
    p.add_argument("--out", default=None, help="Output PDF path.")
    args = p.parse_args()
    build_fig(args.out)


if __name__ == "__main__":
    main()
