"""Figure 6: Coordination Anisotropy.

Composites the layered PNGs from figures/layers/fig06-layers/ into a PDF.

Usage
-----
    python code/figures/fig06_coordination_anisotropy.py
    python code/figures/fig06_coordination_anisotropy.py --out figures/fig06-coordination-anisotropy.pdf
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _composite import composite_layers

_REPO   = Path(__file__).resolve().parents[2]
_LAYERS = _REPO / "figures" / "layers" / "fig06-layers"


def build_fig(out_path: str | None = None) -> None:
    dest = Path(out_path) if out_path else _REPO / "figures" / "fig06-coordination-anisotropy.pdf"
    composite_layers(_LAYERS, dest, fig_size=(6.5, 4.5))


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce Figure 6 (coordination anisotropy).")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    build_fig(args.out)


if __name__ == "__main__":
    main()
