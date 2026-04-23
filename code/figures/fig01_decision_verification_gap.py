"""Figure 1: Decision–Verification Gap.

Thin Python wrapper that compiles the TikZ standalone source
code/figures/fig01_decision_verification_gap.tex via pdflatex.
Output is copied to the canonical path figures/fig01-tikz.pdf (or --out).

Usage
-----
    python code/figures/fig01_decision_verification_gap.py
    python code/figures/fig01_decision_verification_gap.py --out figures/fig01-tikz.pdf
"""

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TEX  = _HERE / "fig01_decision_verification_gap.tex"


def build_fig(out_path: str | None = None) -> None:
    if not _TEX.exists():
        sys.exit(f"TikZ source not found: {_TEX}")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        tex_copy = tmp / _TEX.name
        shutil.copy(_TEX, tex_copy)

        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", tex_copy.name],
            cwd=tmp,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
            sys.exit("pdflatex failed — is TeX Live installed?")

        pdf = tmp / tex_copy.with_suffix(".pdf").name
        if not pdf.exists():
            sys.exit("pdflatex ran but no PDF was produced")

        dest = Path(out_path) if out_path else _HERE.parents[1] / "figures" / "fig01-tikz.pdf"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(pdf, dest)
        print(f"Saved: {dest}")


def main() -> None:
    p = argparse.ArgumentParser(description="Compile Figure 1 (TikZ).")
    p.add_argument("--out", default=None, help="Output PDF path.")
    args = p.parse_args()
    build_fig(args.out)


if __name__ == "__main__":
    main()
