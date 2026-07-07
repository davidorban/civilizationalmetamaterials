#!/usr/bin/env python3
"""
Re-export Fig 2 and Fig 7 as TRUE-VECTOR composites for the AGI-26 poster.

Both figures are authored as z-ordered transparent layers (for PIL compositing).
This driver re-saves each layer as a transparent SVG (Fig 2's dense heatmap layer
stays a high-DPI raster to avoid a multi-thousand-polygon blob), then nests the
layers — with per-figure/per-layer ID namespacing — into a single vector composite:

    fig02-layers/fig2.svg   fig07-layers/fig7.svg

The composites are viewBox-faithful to the approved raster figures (identical layer
geometry), so nothing about the paper's figures is re-derived or drifts. Run with the
project venv:  ../../.venv/bin/python3 make_vector.py
"""
from __future__ import annotations
import importlib.util, os, re, sys, base64

FIGDIR = os.path.dirname(os.path.abspath(__file__))

def load(fname):
    name = fname[:-3]
    spec = importlib.util.spec_from_file_location(name, os.path.join(FIGDIR, fname))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

def make_saver(outdir, dpi, skip_svg_for=()):
    """Return a save fn that writes PNG (original behaviour) + SVG (vector),
    skipping the SVG for layers whose filename contains a skip token (kept raster)."""
    import matplotlib.pyplot as plt
    def saver(fig, filename):
        png = os.path.join(outdir, filename)
        fig.savefig(png, dpi=dpi, transparent=True, pad_inches=0, bbox_inches=None)
        if not any(tok in filename for tok in skip_svg_for):
            fig.savefig(png[:-4] + ".svg", transparent=True, pad_inches=0, bbox_inches=None)
        plt.close(fig)
        print(f"  saved {filename}" + ("" if any(t in filename for t in skip_svg_for) else " + svg"))
    return saver

# ---- ID namespacing so nested layers/figures never collide -------------------
def namespace(svg, tag):
    svg = re.sub(r'id="([^"]+)"', lambda m: f'id="{tag}_{m.group(1)}"', svg)
    svg = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{tag}_{m.group(1)})', svg)
    svg = re.sub(r'(xlink:href|href)="#([^"]+)"',
                 lambda m: f'{m.group(1)}="#{tag}_{m.group(2)}"', svg)
    return svg

def inner_of(svg):
    """Strip xml decl / doctype / outer <svg ...> wrapper, return inner markup + viewBox."""
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    body = re.sub(r'^.*?<svg[^>]*>', '', svg, count=1, flags=re.DOTALL)
    body = re.sub(r'</svg>\s*$', '', body, flags=re.DOTALL)
    return body, vb

def compose(outdir, figtag, layer_order, raster_layer=None):
    """Nest layer SVGs (in z-order) into one composite SVG. `raster_layer` is a
    (filename, png) whose PNG is embedded as a full-canvas <image> instead of SVG."""
    parts = []
    vb = None
    for i, name in enumerate(layer_order):
        base = os.path.join(outdir, name)
        if raster_layer and name == raster_layer:
            png = base + ".png"
            with open(png, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            parts.append(("RASTER", b64))
            continue
        with open(base + ".svg") as f:
            svg = f.read()
        body, this_vb = inner_of(svg)
        vb = vb or this_vb
        parts.append(("SVG", namespace(body, f"{figtag}l{i}")))
    _, _, W, H = map(float, vb.split())
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{W:.2f}pt" height="{H:.2f}pt" viewBox="0 0 {W:.2f} {H:.2f}">']
    for kind, payload in parts:
        if kind == "RASTER":
            out.append(f'<image x="0" y="0" width="{W:.2f}" height="{H:.2f}" '
                       f'preserveAspectRatio="none" '
                       f'xlink:href="data:image/png;base64,{payload}"/>')
        else:
            out.append(f'<g>{payload}</g>')
    out.append('</svg>\n')
    dest = os.path.join(outdir, f"{figtag}.svg")
    with open(dest, "w") as f:
        f.write("\n".join(out))
    kb = os.path.getsize(dest) / 1024
    print(f"  -> {dest} ({kb:.0f} KB, viewBox {W:.0f}x{H:.0f})")
    return dest

# ===================== FIG 2 (hybrid: raster heatmap + vector rest) ===========
print("Fig 2 ...")
m2 = load("fig02_layers.py")
m2.save_layer = make_saver(str(m2.OUTPUT_DIR), m2.DPI, skip_svg_for=("02_heatmap",))
m2.main()
compose(str(m2.OUTPUT_DIR), "fig2",
        ["01_axes_frame", "02_heatmap", "03_phase_boundary", "04_region_labels",
         "05_marker_points", "06_colorbar", "07_inset"],
        raster_layer="02_heatmap")

# ===================== FIG 7 (fully vector) ===================================
print("Fig 7 ...")
m7 = load("fig07_layers.py")
m7._save = make_saver(m7.OUTPUT_DIR, m7.DPI)
m7.main()
compose(m7.OUTPUT_DIR, "fig7",
        ["01_axes_frame", "02_control_bars", "03_scaffolded_bars", "04_cohort_dividers",
         "05_tracer_events", "06_milestone_labels", "07_info_box", "08_legend"])

print("done.")
