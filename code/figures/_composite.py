"""Shared compositor: stack RGBA PNG layers → PDF via matplotlib.

Used by fig03, fig04, fig06, fig07, fig08, fig09, fig10.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def composite_layers(
    layer_dir: Path,
    out_path: Path | None,
    dpi: int = 300,
    fig_size: tuple[float, float] = (6.5, 5.5),
) -> None:
    """Alpha-composite all numbered layer PNGs and save as PDF.

    Layer files are discovered by the pattern ``NN_*.png`` (NN is a 2-digit
    number), sorted numerically.  File ``00_*.png`` is skipped — that is the
    composite preview, not a layer.

    Parameters
    ----------
    layer_dir : Directory containing the layer PNGs.
    out_path  : Destination PDF path.  Prints to screen if None.
    dpi       : Resolution for rasterization embedded in the PDF.
    fig_size  : Matplotlib figure size in inches (width, height).
    """
    layer_files = sorted(
        p for p in layer_dir.glob("*.png")
        if p.stem[:2].isdigit() and not p.stem.startswith("00")
    )
    if not layer_files:
        raise FileNotFoundError(f"No layer PNGs found in {layer_dir}")

    # Load and alpha-composite onto a white base
    first = Image.open(layer_files[0]).convert("RGBA")
    composite = Image.new("RGBA", first.size, (255, 255, 255, 255))
    for lf in layer_files:
        layer = Image.open(lf).convert("RGBA")
        composite = Image.alpha_composite(composite, layer)

    composite_rgb = composite.convert("RGB")

    fig, ax = plt.subplots(figsize=fig_size)
    ax.imshow(np.asarray(composite_rgb))
    ax.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if out_path:
        fig.savefig(str(out_path), dpi=dpi, bbox_inches="tight", pad_inches=0)
        print(f"Saved: {out_path}")
    else:
        plt.show()
    plt.close(fig)
