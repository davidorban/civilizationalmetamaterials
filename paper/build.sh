#!/usr/bin/env bash
# Build the paper PDF from the repo root.
# Usage: bash paper/build.sh
set -euo pipefail

PAPER_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$PAPER_DIR/.." && pwd)"
TEX="civilizational-metamaterials-agi26-r3"

cd "$REPO_ROOT"

pdflatex -interaction=nonstopmode -output-directory="$PAPER_DIR" "paper/$TEX.tex"
bibtex "$PAPER_DIR/$TEX"
pdflatex -interaction=nonstopmode -output-directory="$PAPER_DIR" "paper/$TEX.tex"
pdflatex -interaction=nonstopmode -output-directory="$PAPER_DIR" "paper/$TEX.tex"

cp "$PAPER_DIR/$TEX.pdf" "$PAPER_DIR/preprint/$TEX.pdf"
echo "Built paper/preprint/$TEX.pdf"
