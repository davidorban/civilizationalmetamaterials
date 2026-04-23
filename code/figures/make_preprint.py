"""Build the preprint PDF: full-bleed cover + paper body.

Produces paper/preprint/civilizational-metamaterials-preprint.pdf
(author's preprint version — distinct from the camera-ready submission).

Usage
-----
    python code/figures/make_preprint.py
    python code/figures/make_preprint.py \
        --cover  docs/assets/img/cover.jpg \
        --paper  paper/preprint/civilizational-metamaterials-agi26-r3.pdf \
        --out    paper/preprint/civilizational-metamaterials-preprint.pdf
"""

import argparse
import io
import sys
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter

# A4 at 300 dpi
A4_W_PX = 2480
A4_H_PX = 3508
A4_DPI  = 300

_REPO = Path(__file__).resolve().parents[2]


def cover_to_pdf(cover_path: Path) -> bytes:
    """Render the cover JPEG as a full-bleed A4 PDF page (in memory)."""
    img = Image.open(cover_path).convert("RGB")
    img = img.resize((A4_W_PX, A4_H_PX), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PDF", resolution=A4_DPI)
    return buf.getvalue()


def merge(cover_pdf_bytes: bytes, paper_path: Path, out_path: Path) -> None:
    writer = PdfWriter()

    cover_reader = PdfReader(io.BytesIO(cover_pdf_bytes))
    writer.add_page(cover_reader.pages[0])

    paper_reader = PdfReader(paper_path)
    for page in paper_reader.pages:
        writer.add_page(page)

    # Preserve paper metadata
    meta = paper_reader.metadata or {}
    writer.add_metadata({
        "/Title":   meta.get("/Title",   "Civilizational Metamaterials"),
        "/Author":  meta.get("/Author",  "David Orban"),
        "/Subject": "Preprint — AGI-26 submission with cover",
        "/Creator": "make_preprint.py",
    })

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        writer.write(f)


def main() -> None:
    p = argparse.ArgumentParser(description="Build preprint PDF with bleed cover.")
    p.add_argument("--cover", default=str(_REPO / "docs/assets/img/cover.jpg"))
    p.add_argument("--paper", default=str(_REPO / "paper/preprint/civilizational-metamaterials-agi26-r3.pdf"))
    p.add_argument("--out",   default=str(_REPO / "paper/preprint/civilizational-metamaterials-preprint.pdf"))
    args = p.parse_args()

    cover_path = Path(args.cover)
    paper_path = Path(args.paper)
    out_path   = Path(args.out)

    if not cover_path.exists():
        sys.exit(f"Cover not found: {cover_path}")
    if not paper_path.exists():
        sys.exit(f"Paper PDF not found: {paper_path}")

    print(f"Cover:  {cover_path}")
    print(f"Paper:  {paper_path}  ({paper_path.stat().st_size // 1024} KB)")
    cover_bytes = cover_to_pdf(cover_path)
    merge(cover_bytes, paper_path, out_path)
    print(f"Out:    {out_path}  ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
