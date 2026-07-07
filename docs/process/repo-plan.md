# Plan: Populating `github.com/davidorban/civilizationalmetamaterials`

Target: a public, citable companion repo for *Civilizational Metamaterials: Engineering Coordination Under Capability Gradients and Structural Turbulence* (AGI-26, David Orban), serving (a) a one-page website via GitHub Pages, (b) the paper source and PDF, (c) all figures and the code that generates them, (d) a reference implementation of the R_eff constitutive law, and (e) scaffolding for the proposed stepped-wedge cluster-randomized trial.

---

## 1. Target repository layout

```
civilizationalmetamaterials/
├── README.md                      # repo landing, mirrors key points of the website
├── LICENSE-CODE                   # code license (proposed: MIT)
├── LICENSE-CONTENT                # paper/figures license (proposed: CC-BY 4.0)
├── CITATION.cff                   # machine-readable citation
├── CHANGELOG.md                   # revision history r1 → r2 → r3 → postprint
├── .gitignore                     # ignores .aux, .log, .bbl, .out, .venv, __pycache__, node_modules
├── .gitattributes                 # mark PDFs/PNGs as binary; LFS opt-in for large assets
│
├── docs/                          # GitHub Pages source (served from /docs on main)
│   ├── index.html                 # one-page site
│   ├── assets/
│   │   ├── css/style.css
│   │   ├── js/reff-explorer.js    # tiny interactive widget for the phase diagram
│   │   ├── img/og-card.png        # social card
│   │   └── img/fig02-phase-transition.png  # hero figure (PNG export)
│   ├── paper.pdf                  # symlink or copy of latest paper build
│   └── CNAME                      # (optional) custom domain
│
├── paper/
│   ├── civilizational-metamaterials-agi26-r3.tex   # current camera-ready source
│   ├── references-r3.bib
│   ├── llncs.cls                  # vendored Springer class
│   ├── splncs04.bst               # vendored Springer bib style
│   ├── build.sh                   # one-shot: pdflatex → bibtex → pdflatex × 2
│   ├── Makefile                   # same, plus `make clean`, `make figures`
│   └── preprint/
│       └── civilizational-metamaterials-agi26-r3.pdf   # committed build artifact
│
├── figures/                       # all final PDFs + PNG exports
│   ├── fig01-decision-verification-gap.pdf
│   ├── fig02-phase-transition.pdf
│   ├── fig03-provenance-taxonomy.pdf
│   ├── fig04-freezing-equilibrium.pdf
│   ├── fig05-sensitivity-analysis.pdf
│   ├── fig06-coordination-anisotropy.pdf
│   ├── fig07-trial-design.pdf
│   ├── fig08-trust-anchors.pdf
│   ├── fig09-metamaterial-analogy.pdf
│   ├── fig10-synthetic-principals.pdf
│   ├── png/                       # 300-dpi PNG mirrors for the web
│   └── layers/                    # composited layer PNGs (existing fig0{3,4,6,9,10}-layers/)
│
├── code/
│   ├── pyproject.toml             # single Python project for all analysis
│   ├── README.md                  # how to reproduce every figure from scratch
│   ├── requirements.txt           # pinned; numpy, scipy, matplotlib, pillow
│   ├── cm/                        # importable package
│   │   ├── __init__.py
│   │   ├── constitutive.py        # R_eff(β, ρ, τ, γ), phase boundary, τ* solver
│   │   ├── branching.py           # branching-process Monte Carlo simulator
│   │   ├── sensitivity.py         # one-at-a-time + Sobol indices for Fig. 5
│   │   ├── anisotropy.py          # directional coordination model for Fig. 6
│   │   └── plotting.py            # shared style: colors, fonts, LNCS sizing
│   ├── figures/                   # one script per figure — each produces the same PDF
│   │   ├── fig01_decision_verification_gap.py    # TikZ → pdflatex standalone
│   │   ├── fig01_decision_verification_gap.tex
│   │   ├── fig02_phase_transition.py
│   │   ├── fig03_provenance_taxonomy.py          # PIL composite from layers/
│   │   ├── fig04_freezing_equilibrium.py
│   │   ├── fig05_sensitivity_analysis.py
│   │   ├── fig06_coordination_anisotropy.py
│   │   ├── fig07_trial_design.py
│   │   ├── fig08_trust_anchors.py
│   │   ├── fig09_metamaterial_analogy.py
│   │   └── fig10_synthetic_principals.py
│   ├── tests/
│   │   ├── test_constitutive.py   # known values, critical τ*, monotonicity
│   │   └── test_branching.py      # simulation vs analytic R_eff agreement
│   └── notebooks/
│       ├── 01_phase_diagram_walkthrough.ipynb
│       ├── 02_sensitivity_sobol.ipynb
│       └── 03_anisotropy_gallery.ipynb
│
├── experiments/                   # scaffolding for the proposed 12-week trial
│   ├── README.md                  # trial overview, linking back to §Empirical in paper
│   ├── protocol/
│   │   ├── protocol-v0.1.md       # stepped-wedge CRT protocol draft
│   │   ├── consent-form-template.md
│   │   ├── SAP.md                 # statistical analysis plan
│   │   └── preregistration-OSF.md # OSF/AsPredicted template, ready to paste
│   ├── power/
│   │   ├── power_analysis.py      # ICC assumptions, clusters × periods sizing
│   │   └── power_curves.pdf
│   ├── instruments/
│   │   ├── provenance-checklist.pdf    # Class A/B/C rubric used by reviewers
│   │   ├── verification-timer-app/     # lightweight web timer for τ measurement
│   │   └── data-dictionary.md
│   ├── synthetic/                 # synthetic datasets for method validation
│   │   ├── generate_synthetic_panels.py
│   │   └── fixtures/
│   └── analysis/
│       ├── primary_endpoint.py    # hypothesis H1 (phase transition crossing)
│       ├── secondary_h2_h4.py     # H2 synergy, H3 anisotropy, H4 hysteresis
│       └── simulate_trial.py      # end-to-end trial simulation under null/alt
│
├── drafts/                        # prior revisions kept for provenance
│   ├── r1/{.tex, .bib}
│   └── r2/{.tex, .bib}
│
├── peer-review/                   # public post-acceptance review thread
│   ├── peer-review-agi26.md
│   ├── peer-review-agi26-r1.md
│   ├── peer-review-agi26-r2.md
│   └── author-rebuttal-agi26{,-r1}.md
│
└── .github/
    ├── workflows/
    │   ├── build-paper.yml        # tectonic/latexmk build on push; upload artifact
    │   ├── figures.yml            # re-run figure scripts, diff against committed PDFs
    │   ├── tests.yml              # pytest on code/
    │   └── pages.yml              # deploy docs/ to Pages
    ├── ISSUE_TEMPLATE/
    │   ├── errata.md
    │   └── replication.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── CODEOWNERS
```

---

## 2. One-page website (`docs/index.html`)

Single static HTML page, served by GitHub Pages from `/docs` on `main`. No framework — inline CSS, one small JS file. Section list, top to bottom:

1. **Masthead.** Title, author, ORCID, affiliation, AGI-26 badge, "Paper (PDF)" and "arXiv" buttons, BibTeX copy button.
2. **One-paragraph abstract** (the paper's abstract, lightly edited for web reading).
3. **The central claim in one sentence + the constitutive law** rendered in MathJax: `R_eff = β·(1−ρ)·(1−τ)·(1−γρτ)`.
4. **Hero figure** — Fig. 2 phase transition, PNG, with a small interactive slider widget (`reff-explorer.js`) that lets a visitor drag β, ρ, τ, γ and see whether the system is in the damped or turbulent regime. Fallback: static image.
5. **Four contributions** (as titled blocks, not bullets): constitutive law, three-class provenance taxonomy, synthetic principals, falsifiable trial.
6. **The four hypotheses (H1–H4)** and a sentence each on what would falsify them.
7. **Experiment** — one paragraph + a link to `experiments/` with the protocol, SAP, and OSF preregistration template.
8. **Cite this work** — BibTeX block, copy button, DOI placeholder.
9. **Reproduce** — a 3-line `git clone` / `make paper` / `make figures` block.
10. **Footer** — license (CC-BY 4.0 content, MIT code), contact, last-updated timestamp, link to the GitHub repo.

Design constraints: no tracking, no external fonts (system font stack), renders on mobile, <100 kB HTML + CSS + JS excluding the hero PNG, dark-mode via `prefers-color-scheme`. Open Graph / Twitter card metadata with a pre-rendered 1200×630 `og-card.png`.

---

## 3. Figures — what exists vs. what needs to be written

Current state in `submission/figures/`: ten final PDFs plus layered PNG directories for figures 3, 4, 6, 9, 10 (LAYER_INDEX.md documents each). The Python scripts that produced the layers and the computational figures are not in the repo.

Plan per figure:

| Fig | Type | Action |
|---|---|---|
| 01 | TikZ (name is `fig01-tikz.pdf`) | Commit the TikZ source as `code/figures/fig01_decision_verification_gap.tex` + a tiny Python wrapper that runs `pdflatex` |
| 02 | Computational (contourf + phase boundary via `scipy.optimize.brentq`) | Rewrite as `fig02_phase_transition.py` using `cm.constitutive`; output must byte-match committed PDF (tolerance ≈ fonts) |
| 03 | Layered composite | `fig03_provenance_taxonomy.py` draws each labelled box/arrow with matplotlib; layers in `figures/layers/fig03-layers/` kept for editability |
| 04 | Layered composite | Same pattern as fig03 |
| 05 | Computational (sensitivity sweeps) | `fig05_sensitivity_analysis.py` calls `cm.sensitivity` (OAT + Sobol indices) |
| 06 | Layered composite | Same pattern as fig03 |
| 07 | Stepped-wedge schedule | `fig07_trial_design.py` — parametric, so `experiments/protocol/` can re-render if cluster counts change |
| 08 | Layered / diagram | Same pattern as fig03 |
| 09 | Layered composite (physical↔institutional mapping) | Same pattern as fig03 |
| 10 | Layered composite (synthetic principals tree) | Same pattern as fig03 |

Each figure script has a stable CLI: `python figures/figXX_*.py --out ../figures/figXX-*.pdf`. A `make figures` target runs them all. A CI job re-runs every script and diffs pixel output against the committed PDF; any drift must be an intentional commit.

Shared `cm/plotting.py` holds the color constants already documented in LAYER_INDEX.md (`#1B4F72`, `#2E86C1`, `#D68910`, `#C0392B`, `#1E8449`), LNCS text-width sizing, and font defaults.

---

## 4. Paper build

- Vendor `llncs.cls` and `splncs04.bst` so the build is hermetic.
- `paper/Makefile`: `make paper` → `latexmk -pdf -interaction=nonstopmode`; `make clean` removes `.aux .log .bbl .blg .out`.
- `build-paper.yml` GitHub Action uses `xu-cheng/latex-action@v3` on every push that touches `paper/**` or `figures/**`; uploads the PDF as a workflow artifact and (on tagged releases) attaches it to a GitHub Release.
- The `docs/paper.pdf` served by Pages is refreshed by the same workflow so the website's "Paper (PDF)" button always points at the latest build.

---

## 5. Reference implementation (`code/cm/`)

Deliberately small, with the goal of being readable alongside the paper, not a framework:

- `constitutive.py`: `r_eff(beta, rho, tau, gamma)`, `tau_star(beta, rho, gamma)`, `phase_boundary(beta, gamma, grid)` — all vectorized.
- `branching.py`: `simulate(beta, rho, tau, gamma, depth, n_trials, seed)` returns cascade-size distribution; validates analytic R_eff against empirical extinction probability.
- `sensitivity.py`: OAT + Sobol (via `SALib`); produces the arrays consumed by `fig05_*.py`.
- `anisotropy.py`: directional coordination tensor for §Anisotropy; produces fig06 data.

Testing: `pytest` enforces (i) known closed-form values of R_eff at corners, (ii) monotonicity in ρ and τ, (iii) Monte Carlo agreement with analytic R_eff to within 3σ at n=10⁴ trials. Coverage target 90% on `cm/`.

---

## 6. Experiment scaffolding (`experiments/`)

The paper proposes a 12-week stepped-wedge cluster-randomized trial in government grant review panels. The repo should give a prospective replicator everything they need short of IRB and funding:

- **Protocol** (`protocol-v0.1.md`) — stepped-wedge design, cluster and period counts, randomization procedure, intervention description (Class A/B/C provenance scaffolding), primary endpoint (binary: panel crosses R_eff = 1), secondary endpoints (H2 synergy, H3 anisotropy, H4 hysteresis), adverse-event handling.
- **Statistical analysis plan** (`SAP.md`) — mixed-effects logistic model with period fixed effects and cluster random effects; pre-specified sensitivity analyses.
- **Power analysis** (`power/power_analysis.py`) — ICC range 0.01–0.10, detectable effect sizes, publication-quality `power_curves.pdf`.
- **Preregistration template** (`preregistration-OSF.md`) — ready to paste into OSF, with every field filled except the registration date.
- **Instruments** — the provenance-class rubric as a PDF reviewers can print, and a minimal web timer (static HTML + JS) to measure τ at the panel node.
- **Synthetic data generator** — produces plausible panel-level outcomes under H0/H1 so the analysis scripts can be unit-tested end-to-end.
- **Analysis scripts** (`analysis/*.py`) — runnable today against synthetic fixtures; swap in real data later.
- **Trial simulator** (`simulate_trial.py`) — Monte Carlo under null and alternative, reports type-I error, power, and bias of the primary-endpoint estimator.

This is a scaffolding, not a registered trial — the README makes that clear.

---

## 7. Licensing, citation, governance

- **Code**: MIT (permissive, replication-friendly). Proposal — flag for your decision.
- **Paper text, figures, protocols**: CC-BY 4.0 (attribution, derivatives allowed). Proposal — flag for your decision.
- **`CITATION.cff`**: includes DOI once assigned (Zenodo auto-mint on first tagged release), ORCID `0009-0004-4954-1147`, preferred-citation pointing at the AGI-26 proceedings entry once live.
- **Zenodo integration**: enable the Zenodo–GitHub webhook so every tagged release mints an archival DOI; embed that DOI in the README and the website.
- **Issue templates**: `errata.md` for corrections to the paper, `replication.md` for attempts to reproduce the model or (eventually) the trial.
- **Code of Conduct**: Contributor Covenant v2.1.
- **`CONTRIBUTING.md`**: how to open errata, how to submit an independent replication, how to propose a figure fix.

---

## 8. CI / CD

Four workflows, all on `ubuntu-latest`:

1. `build-paper.yml` — triggers on changes under `paper/**` or `figures/**`. TeXLive via `xu-cheng/latex-action@v3`. Uploads PDF; on tag, attaches to Release and copies to `docs/paper.pdf` via a commit from `github-actions[bot]`.
2. `figures.yml` — triggers on changes under `code/**`. Installs Python deps, runs every `code/figures/figXX_*.py`, diffs each output against `figures/figXX-*.pdf` at the pixel level (tolerance for font rasterization), fails on unexpected drift.
3. `tests.yml` — triggers on changes under `code/**`. `pytest` with coverage; fails under 90%.
4. `pages.yml` — triggers on `main`. Deploys `docs/` to GitHub Pages via `actions/deploy-pages@v4`. Also runs `lychee` link-check and `html-validate`.

---

## 9. Phased rollout

Keeps the public repo credible at each step rather than landing as a giant unreviewed drop.

**Phase 0 — Skeleton (1 day).** Create repo, push `README.md`, `LICENSE-CODE`, `LICENSE-CONTENT`, `CITATION.cff`, `.gitignore`, `.gitattributes`, empty directory structure with `.gitkeep` files. No Pages yet.

**Phase 1 — Paper + figures as-is (1 day).** Commit the r3 TeX, bib, class files, vendored BibTeX style, all ten figure PDFs, the existing `fig0{3,4,6,9,10}-layers/` directories, and `LAYER_INDEX.md`. Commit the compiled PDF to `paper/preprint/`. Add `build-paper.yml`. The repo is now citable.

**Phase 2 — Website (1–2 days).** Write `docs/index.html`, styles, and `reff-explorer.js`. Enable Pages from `/docs` on `main`. Add `pages.yml`. The repo now has a public front door.

**Phase 3 — Reference implementation (3–5 days).** Port/write `cm/` package with tests. Reproduce `fig02` and `fig05` computationally; commit the scripts. Add `tests.yml` and `figures.yml`. The key results are now independently reproducible.

**Phase 4 — Remaining figure scripts (2–3 days).** Write scripts for figs 1, 3, 4, 6, 7, 8, 9, 10 — the composited ones reconstruct their layers with matplotlib so future edits don't require the original design tool.

**Phase 5 — Experiment scaffolding (3–5 days).** Protocol draft, SAP, power analysis, preregistration template, synthetic data generator, analysis scripts, trial simulator. Marked clearly as "proposed, not yet registered."

**Phase 6 — Polish + v1.0.0 tag (1 day).** Fill in peer-review thread, push final README, enable Zenodo webhook, cut `v1.0.0`, let the archival DOI mint, update `CITATION.cff` and the website with the DOI.

Total: about two focused weeks, or 3–4 calendar weeks at a lighter cadence.

---

## 10. Decisions (locked in)

1. **Code license** — MIT.
2. **Content license** — CC-BY 4.0.
3. **Figure-source strategy** — fully source-driven. Every figure (TikZ, matplotlib, or layered composite) has a script under `code/figures/` that produces the PDF from scratch; `make figures` rebuilds all ten; CI diffs outputs against committed PDFs.
4. **Custom domain** — `metamaterials.davidorban.com` (CNAME already propagating). Add `docs/CNAME` with that hostname; enable "Enforce HTTPS" in repo Pages settings once the Let's Encrypt cert provisions.
5. **Preprint mirror** — arXiv now, primary `cs.CY`, cross-lists `cs.MA` and `cs.AI`. No SSRN. Add `paper/arxiv/` with a make target that produces an arXiv-ready tarball. Post v1 on arXiv once r3 is locked; push v2 with "Accepted, AGI-26" on decision.
6. **Experiments scope** — (b) theoretical scaffolding + open for collaboration. Add `COLLABORATION.md` with how institutions can pilot the protocol and a contact flow; the protocol and SAP remain marked "proposed, not registered" until a partner takes it on.

**Review state:** AGI-26 review is single-blind (confirmed by the committee chair). The named version is the live submission on EasyChair; the anonymized tree (`*-anon.tex`, `*-anon.*` outputs, `de-anonymization-plan.md`) is deprecated and is explicitly excluded from the repo.

**R3 is locked.** arXiv v1 can go up immediately as part of Phase 1; arXiv v2 follows on acceptance.

**Visibility:** public from day one. No private dev phase. Commits serve as the public changelog.

## 11. Phase shuffle given single-blind review

- The repo can be public from Phase 0; no reason to hold it private for anonymity.
- arXiv moves from Phase 6 into Phase 1 as an optional concurrent step — runnable the moment r3 is finalized.
- `CITATION.cff` starts with `status: "Under review at AGI-26"`; acceptance day flips it to `status: "Accepted, AGI-26. To appear in Springer LNCS/LNAI."` and backfills the DOI.
- Phase 6 becomes lighter: cut `v1.0.0`, let Zenodo mint the archival DOI, push arXiv v2 with the acceptance note, update the website buttons.
