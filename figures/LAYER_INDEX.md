# Civilizational Metamaterials - Figure Layers

## Figure 2: Phase Transition Diagram

**Directory**: `fig02-layers/`  
**Dimensions**: 6.5 × 5.5 inches (1950 × 1650 px @ 300 DPI)  
**Format**: PNG with RGBA transparency  

| Layer | File | Description |
|-------|------|-------------|
| 00 | `00_composite_preview.png` | All layers combined on white background (preview) |
| 01 | `01_axes_frame.png` | Axes, ticks, grid, labels (ρ, τ) |
| 02 | `02_heatmap.png` | Diverging colormap contourf (256 levels, blue→white→red) |
| 03 | `03_phase_boundary.png` | Bold black R_eff = 1.0 contour line with label |
| 04 | `04_region_labels.png` | Region text: "Damped" (blue), "Turbulent" (red) |
| 05 | `05_marker_points.png` | Three point markers + dashed green trajectory arrow |
| 06 | `06_colorbar.png` | Standalone colorbar (R_eff scale) |
| 07 | `07_inset.png` | Inset axes showing critical boundaries for β=5,10,50 |

**Computation**:
- R_eff = β(1−ρ)(1−τ)(1+γρτ) with β=10, γ=1
- 300×300 grid over ρ∈[0,1], τ∈[0,1]
- Phase boundary at R_eff=1.0 (scipy.optimize.brentq)

---

## Figure 3: Three-Class Provenance Taxonomy

**Directory**: `fig03-layers/`  
**Dimensions**: 6.5 × 5.0 inches (1950 × 1500 px @ 300 DPI)  
**Format**: PNG with RGBA transparency  

| Layer | File | Description |
|-------|------|-------------|
| 00 | `00_composite_preview.png` | All layers combined on white background (preview) |
| 01 | `01_layer_a.png` | Class A box (cryptographic, light blue) |
| 02 | `02_layer_b.png` | Class B box (institutional, light amber) |
| 03 | `03_layer_c.png` | Class C box (context binding, light green) + NOVEL badge |
| 04 | `04_annotations_right.png` | Right-side Q&A annotations for each class |
| 05 | `05_warning_callout.png` | Top warning callout (light red) |
| 06 | `06_connecting_bracket.png` | Left vertical bracket + "Complementary layers" label |

**Layout**:
- Class A: y=0.02–0.28 (bottom)
- Class B: y=0.30–0.56 (middle)
- Class C: y=0.58–0.84 (top) with NOVEL badge
- Annotations: x=0.74–0.98 (right side)
- Warning: y=0.88–0.97 (top)

---

## Compositing Layers

### Python (PIL/Pillow)
```python
from PIL import Image

base = Image.open('01_axes_frame.png').convert('RGBA')
for layer_file in ['02_heatmap.png', '03_phase_boundary.png', ...]:
    overlay = Image.open(layer_file).convert('RGBA')
    base = Image.alpha_composite(base, overlay)
base.save('final_figure.png')
```

### Command Line (ImageMagick)
```bash
convert 01_axes_frame.png 02_heatmap.png 03_phase_boundary.png \
        -composite final_figure.png
```

---

## Color Constants

All figures use:
- DARK_BLUE: #1B4F72
- SEC_BLUE: #2E86C1
- AMBER: #D68910
- RED: #C0392B
- GREEN: #1E8449
- GRAY: #7F8C8D
- LIGHT_GRAY: #BDC3C7

---

## Technical Notes

- All PNGs: 8-bit RGBA, non-interlaced
- DPI: 300 (publication quality)
- Font: serif, mathtext fontset: cm
- Subplot adjustments ensure pixel-perfect alignment
- Transparent backgrounds enable flexible composition

Generated 2026-04-12 via matplotlib 3.x + scipy
