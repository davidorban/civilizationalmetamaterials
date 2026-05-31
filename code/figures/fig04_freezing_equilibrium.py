"""Figure 4: Freezing Equilibrium — Nash payoffs under r4 specification.

Visualizes the 3-action population game introduced in §1 of the r4 paper:
each agent chooses among {ACT-blind, ACT-verified, WAIT} in response to
a claim that is legitimate with prior probability p. Payoffs are:

    u(ACT-blind)    = p · U_act − (1 − p) · L
    u(ACT-verified) = p · U_act − C_ver
    u(WAIT)         = 0

The figure shows two regimes side by side:
- Left:  "Without Scaffolding"   — high C_ver, low p  → all-WAIT is Nash.
- Right: "With Scaffolding"      — low C_ver, high p  → ACT-verified is Nash.

Replaces the prior layer-composite version (which used a 2-player
Act/Wait 2×2 matrix from r1/r2). The r4 specification requires three
actions per agent and explicit payoffs.

Usage
-----
    python code/figures/fig04_freezing_equilibrium.py
    python code/figures/fig04_freezing_equilibrium.py --out figures/fig04-freezing-equilibrium.pdf
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


# ── Colours (from cm.plotting palette) ───────────────────────────────────
NAVY = "#1B4F72"
AMBER = "#D68910"
ALERT_RED = "#C0392B"
SUCCESS_GREEN = "#1E8449"
NEUTRAL_GRAY = "#7F8C8D"
LIGHT_GRAY = "#BDC3C7"


@dataclass(frozen=True)
class Regime:
    """A parameter regime for the Freezing-Equilibrium game.

    All payoffs are in arbitrary utility units, scaled so that
    WAIT (utility = 0) is the natural reference.
    """

    label: str
    p: float          # legitimacy prior
    U_act: float      # value of acting correctly
    L: float          # loss from acting on a false claim
    C_ver: float      # cost of verification

    def u_act_blind(self) -> float:
        return self.p * self.U_act - (1.0 - self.p) * self.L

    def u_act_verified(self) -> float:
        return self.p * self.U_act - self.C_ver

    def u_wait(self) -> float:
        return 0.0

    def nash_action(self) -> str:
        payoffs = {
            "ACT-blind": self.u_act_blind(),
            "ACT-verified": self.u_act_verified(),
            "WAIT": self.u_wait(),
        }
        return max(payoffs, key=payoffs.get)


# ── Illustrative regimes ────────────────────────────────────────────────
# Without scaffolding: legitimacy prior low (population includes many
# AI-fabricated claims), verification expensive, loss heavy.
WITHOUT = Regime(
    label="Without Scaffolding",
    p=0.30,
    U_act=1.0,
    L=2.0,
    C_ver=0.50,
)

# With scaffolding: provenance raises p (Class C context binding cheap to
# check), verification cost collapses to O(1) per claim.
WITH = Regime(
    label=r"With Scaffolding ($C_{\mathrm{ver}}\!\downarrow$, $p\!\uparrow$)",
    p=0.70,
    U_act=1.0,
    L=2.0,
    C_ver=0.15,
)


def _draw_panel(ax: plt.Axes, regime: Regime) -> None:
    """Render one regime as a horizontal payoff bar chart."""
    actions = ["ACT-blind", "ACT-verified", "WAIT"]
    payoffs = [
        regime.u_act_blind(),
        regime.u_act_verified(),
        regime.u_wait(),
    ]
    nash = regime.nash_action()
    y_positions = [2, 1, 0]

    # Highlight the Nash row with a faint background band so the equilibrium
    # is visible even when the Nash action's bar has zero length (WAIT).
    nash_idx = actions.index(nash)
    nash_y = y_positions[nash_idx]
    nash_payoff = payoffs[nash_idx]
    nash_colour = SUCCESS_GREEN if nash_payoff >= 0 else ALERT_RED
    ax.axhspan(nash_y - 0.42, nash_y + 0.42,
               color=nash_colour, alpha=0.10, zorder=0)

    # Colour rule: Nash action highlighted, others muted.
    colours: list[str] = []
    for action, value in zip(actions, payoffs):
        if action == nash:
            colours.append(nash_colour)
        else:
            colours.append(LIGHT_GRAY)

    ax.barh(y_positions, payoffs, color=colours, edgecolor="white",
            linewidth=0.8, height=0.62, zorder=2)

    # Marker for the Nash action at u = 0 (visible even when bar has zero
    # length, i.e. when WAIT is the equilibrium).
    ax.plot([0], [nash_y], marker="D", markersize=7,
            markeredgecolor=nash_colour, markerfacecolor="white",
            markeredgewidth=1.4, zorder=4, clip_on=False)

    # Reference line at u = 0 (WAIT baseline)
    ax.axvline(0, color=NEUTRAL_GRAY, linewidth=0.7, linestyle="--",
               alpha=0.6, zorder=1)

    # Payoff labels at bar ends (skip the trivial 0.00 for WAIT)
    for y, value in zip(y_positions, payoffs):
        if abs(value) < 1e-9:
            continue
        offset = 0.04 if value >= 0 else -0.04
        ha = "left" if value >= 0 else "right"
        ax.text(value + offset, y, f"{value:+.2f}",
                va="center", ha=ha, fontsize=9, color=NEUTRAL_GRAY,
                zorder=3)

    # Action labels — Nash row gets bold colour + "(Nash)" suffix
    ax.set_yticks(y_positions)
    labels: list[str] = []
    for action in actions:
        if action == nash:
            labels.append(f"{action}\n(Nash)")
        else:
            labels.append(action)
    ax.set_yticklabels(labels, fontsize=10)
    for label, action in zip(ax.get_yticklabels(), actions):
        if action == nash:
            label.set_color(nash_colour)
            label.set_fontweight("bold")

    # X axis
    ax.set_xlim(-1.6, 0.85)
    ax.set_xlabel("Expected utility", fontsize=9, color=NEUTRAL_GRAY)
    ax.tick_params(axis="x", labelsize=8, colors=NEUTRAL_GRAY)
    ax.tick_params(axis="y", length=0)

    # Spines
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(NEUTRAL_GRAY)
        ax.spines[spine].set_linewidth(0.6)

    # Title: regime label + parameter readout on a second line
    param_text = (
        rf"$p = {regime.p:.2f}$,  "
        rf"$U_{{\mathrm{{act}}}} = {regime.U_act:.1f}$,  "
        rf"$L = {regime.L:.1f}$,  "
        rf"$C_{{\mathrm{{ver}}}} = {regime.C_ver:.2f}$"
    )
    ax.set_title(f"{regime.label}\n", fontsize=11, color=NAVY, pad=22)
    ax.text(0.5, 1.04, param_text, transform=ax.transAxes,
            ha="center", va="bottom", fontsize=8, color=NEUTRAL_GRAY,
            fontstyle="italic")

    # Nash signalling lives in the y-tick label and the green band+diamond+bar.
    # No separate callout — the visual cues are already redundant enough.


def build_fig(out_path: str | None = None) -> Path:
    """Render the figure and write it as a PDF.

    Returns the resolved output path.
    """
    plt.rcParams.update({
        "font.family": "serif",
        "mathtext.fontset": "cm",
        "axes.unicode_minus": False,
    })

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.72, bottom=0.20, wspace=0.50)

    _draw_panel(axes[0], WITHOUT)
    _draw_panel(axes[1], WITH)

    # Suptitle and shared legend area
    fig.suptitle(
        "Freezing Equilibrium: Nash payoffs under the r4 specification",
        fontsize=12, color=NAVY, y=0.97,
    )
    fig.text(
        0.5, 0.04,
        r"Payoffs: $u(\mathrm{ACT\text{-}blind}) = p\,U_{\mathrm{act}} - (1-p)\,L$  ·  "
        r"$u(\mathrm{ACT\text{-}verified}) = p\,U_{\mathrm{act}} - C_{\mathrm{ver}}$  ·  "
        r"$u(\mathrm{WAIT}) = 0$",
        ha="center", va="bottom", fontsize=8, color=NEUTRAL_GRAY,
    )

    repo = Path(__file__).resolve().parents[2]
    dest = Path(out_path) if out_path else repo / "figures" / "fig04-freezing-equilibrium.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(dest, format="pdf", bbox_inches="tight")
    plt.close(fig)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reproduce Figure 4 (Freezing Equilibrium, r4 Nash spec)."
    )
    parser.add_argument("--out", default=None,
                        help="Output path (default: figures/fig04-freezing-equilibrium.pdf).")
    args = parser.parse_args()
    dest = build_fig(args.out)
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
