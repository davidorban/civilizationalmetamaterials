"""Figure 7: Stepped-Wedge Trial Design.

Composites the layered PNGs from figures/layers/fig07-layers/ into a PDF.
The underlying layers are parametric in cluster/period counts — to re-render
with different parameters, edit the layer scripts in the source repo and
re-run this compositor.

Usage
-----
    python code/figures/fig07_trial_design.py
    python code/figures/fig07_trial_design.py --out figures/fig07-trial-design.pdf
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _composite import composite_layers

_REPO   = Path(__file__).resolve().parents[2]
_LAYERS = _REPO / "figures" / "layers" / "fig07-layers"


def build_fig(out_path: str | None = None) -> None:
    dest = Path(out_path) if out_path else _REPO / "figures" / "fig07-trial-design.pdf"
    composite_layers(_LAYERS, dest, fig_size=(6.5, 4.5))


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce Figure 7 (trial design).")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    build_fig(args.out)


if __name__ == "__main__":
    main()
