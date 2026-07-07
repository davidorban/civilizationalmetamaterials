# Poster Kit — Civilizational Metamaterials (AGI-26)

A self-contained, modular SVG kit for assembling the A0 poster in Claude Design.
Every module is a standalone, scalable SVG (real `viewBox`, no external assets —
figures are embedded as base64, the QR is a vector path). Hand the whole folder to
the design tool, or drop in individual modules and scale them freely.

## What's here

```
poster-kit/
├─ poster-master.svg            ← fully composed A0 poster, self-contained (start here)
├─ manifest.json                ← machine-readable layout: canvas, palette, type, placements
├─ README-FOR-CLAUDE-DESIGN.md  ← this file
├─ modules/                     ← 7 granular, independently scalable SVG blocks
│   ├─ 00-header.svg            (841 × 120 mm, bleeds)
│   ├─ 01-central-claim.svg     (791 × 116 mm)
│   ├─ 02-column-problem.svg    (247 × 352 mm, embeds Fig 1)
│   ├─ 03-column-phase.svg      (247 × 360 mm, embeds Fig 2 — dominant graphic)
│   ├─ 04-column-framework.svg  (247 × 300 mm)
│   ├─ 05-testing-band.svg      (791 × 238 mm, embeds Fig 7 + H1–H4)
│   └─ 06-footer.svg            (841 × 237 mm, bleeds, vector QR)
└─ figures/                     ← source assets (already inlined into the modules)
    ├─ fig1.png  fig2.png  fig7.png   (raster, 320 DPI)
    └─ qr.svg                          (true vector → metamaterials.davidorban.com)
```

## Coordinate system

- **Units: millimetres. Canvas: A0 portrait = 841 × 1189 mm. Origin: top-left, y increases downward.**
- Each module's `viewBox` is `0 0 <w> <h>` in mm, so it scales to any frame with no distortion.
- The master places each module at the `x_mm`/`y_mm` in `manifest.json` using a nested `<svg>` — change those numbers to recompose.

## The grid (how the page is built)

| Band | y (mm, from top) | Notes |
|---|---|---|
| Header | 0 – 120 | full-bleed dark band |
| Central claim | 135 – 251 | full content width (25 mm side margins) |
| 3 columns | 270 – ~630 | 3 × 247 mm wide, 25 mm gutters |
| Testing band | 705 – 943 | full content width |
| Footer | 952 – 1189 | full-bleed dark band |

Body content lives inside a **25 mm side margin** (791 mm usable width). Columns 1/2/3 start at x = 25 / 297 / 569 mm. Header and footer intentionally bleed to the trim edge — add **3 mm bleed** there before printing.

## Design tokens (also in manifest.json)

**Palette** — dark blue `#1B4F72` · amber `#D68910` · red `#C0392B` · green `#1E8449` · secondary blue `#2E86C1` · gray `#7F8C8D` · light `#F4F6F7` · ink `#1A1A1A`. Each column is keyed to a color (Problem = red, Phase = blue, Framework = green) and the four hypotheses reuse them.

**Type** — serif throughout (STIX Two Text; falls back to Times/Georgia). Real point sizes: title 78 · equation 58 · AGI lockup 40 · subtitle 33 · central body 27 · column headers 24 · sub-heads 23 · body 20 · captions 16. All text is **live `<text>`** — edit copy directly; outline/embed fonts before final print.

## How to use in Claude Design

1. **Fastest:** open `poster-master.svg` — it is the finished A0 poster in one file. Resize, restyle, or move blocks.
2. **Modular:** import any `modules/*.svg` as an object. Because each has a mm `viewBox`, scaling preserves proportions and text stays vector. Re-place using the `manifest.json` coordinates, or rearrange freely.
3. **Recompose:** to change the layout, edit the `x_mm`/`y_mm`/`w_mm`/`h_mm` for each module in `manifest.json` and reflow — the modules are independent.

## Scaling & format notes

- Text, shapes, and the QR are **resolution-independent** — scale without limit.
- `fig1/fig2/fig7` are **raster** (a heatmap and composites where raster is the right call), embedded at 320 DPI — crisp at the intended A0 size. To go fully vector, re-export those plots as SVG from their matplotlib sources and replace the `<image>` in the relevant module.
- `fig1.png` is the **V_d-corrected** composite (the curve keeps climbing — do not substitute the older plateau version).

## Accuracy locked in (do not alter)

- Equation: **R_eff = β (1−ρ)(1−τ)(1+γρτ)**
- Worked threshold: **τ\* ≈ 0.86** (post-errata; not 0.833)
- Hypotheses: **H1 Bandgap · H2 Anisotropy · H3 Superadditivity · H4 Hysteresis**
- DOI **10.5281/zenodo.19710482** · metamaterials.davidorban.com · ORCID 0009-0004-4954-1147

## Print handoff

A0 portrait, matte, **print at 100% (no scaling)**. Add 3 mm bleed, embed/outline fonts, convert sRGB → CMYK with the shop's profile (FOGRA39 / GRACoL).
