"""Shared plotting style for all figure scripts.

Color constants from LAYER_INDEX.md. LNCS text-width sizing.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt

# ── Color palette ─────────────────────────────────────────────────────────
DARK_BLUE   = "#1B4F72"
SEC_BLUE    = "#2E86C1"
AMBER       = "#D68910"
RED         = "#C0392B"
GREEN       = "#1E8449"
GRAY        = "#7F8C8D"
LIGHT_GRAY  = "#BDC3C7"

# ── LNCS column widths (inches) ───────────────────────────────────────────
LNCS_FULL_W   = 4.7       # \textwidth in inches (122 mm at 26 pt margins)
LNCS_HALF_W   = 2.25      # two-column subfigure
LNCS_ASPECT   = 0.75      # default height = width × aspect

# ── Font defaults ──────────────────────────────────────────────────────────
_FONT_SIZE = 9


def apply_lncs_style() -> None:
    """Apply LNCS-compatible matplotlib rcParams globally."""
    mpl.rcParams.update(
        {
            "font.family":       "serif",
            "mathtext.fontset":  "cm",
            "font.size":         _FONT_SIZE,
            "axes.titlesize":    _FONT_SIZE,
            "axes.labelsize":    _FONT_SIZE,
            "xtick.labelsize":   _FONT_SIZE - 1,
            "ytick.labelsize":   _FONT_SIZE - 1,
            "legend.fontsize":   _FONT_SIZE - 1,
            "figure.dpi":        300,
            "savefig.dpi":       300,
            "savefig.bbox":      "tight",
            "savefig.pad_inches": 0.02,
        }
    )


def new_fig(
    width: float = LNCS_FULL_W,
    aspect: float = LNCS_ASPECT,
) -> tuple:
    """Return (fig, ax) with LNCS sizing."""
    apply_lncs_style()
    fig, ax = plt.subplots(figsize=(width, width * aspect))
    return fig, ax
