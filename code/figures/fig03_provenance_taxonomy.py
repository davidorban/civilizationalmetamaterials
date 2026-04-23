"""Figure 3: Three-Class Provenance Taxonomy.

Composites the layered PNGs from figures/layers/fig03-layers/ into a PDF.

Usage
-----
    python code/figures/fig03_provenance_taxonomy.py
    python code/figures/fig03_provenance_taxonomy.py --out figures/fig03-provenance-taxonomy.pdf
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _composite import composite_layers

_REPO   = Path(__file__).resolve().parents[2]
_LAYERS = _REPO / "figures" / "layers" / "fig03-layers"


def build_fig(out_path: str | None = None) -> None:
    dest = Path(out_path) if out_path else _REPO / "figures" / "fig03-provenance-taxonomy.pdf"
    composite_layers(_LAYERS, dest, fig_size=(6.5, 5.0))


def main() -> None:
    p = argparse.ArgumentParser(description="Reproduce Figure 3 (provenance taxonomy).")
    p.add_argument("--out", default=None)
    args = p.parse_args()
    build_fig(args.out)


if __name__ == "__main__":
    main()
