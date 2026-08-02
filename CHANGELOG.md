# Changelog

All notable revisions to the paper and the repository are recorded here. The
paper's revision history reflects the AGI-26 peer-review rounds.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/),
adapted for an academic repository.

---

## [Unreleased]

---

## Phase 8 — 2026-08-02  (v1.1.0, published record)

The publication phase. No changes to the paper's content: this release marks
the transition from accepted preprint to formally published chapter, and
records the artifacts produced around the AGI-26 presentation.

### Publication

- **Springer proceedings chapter published** 2026-07-22:
  [10.1007/978-3-032-33195-3_10](https://doi.org/10.1007/978-3-032-33195-3_10)
  (*Artificial General Intelligence. AGI 2026*, LNCS vol 16855, pp. 118–136,
  Springer Cham, ISBN 978-3-032-33195-3). This is now the preferred citation.
- `CITATION.cff` `preferred-citation` activated as a `conference-paper` entry;
  `version` reconciled from the pre-release `0.1.0-r4` to `1.1.0`.
- README and minisite BibTeX upgraded from `@misc` to `@inproceedings`.

### Minisite

- Added the recorded AGI-26 talk (15 minutes,
  [youtu.be/nPN5nLvphx4](https://youtu.be/nPN5nLvphx4)) as an embedded section,
  with a "Watch the talk" link in the masthead.
- Springer chapter button added to the masthead.

### Presentation

- The paper was presented at AGI-26, San Francisco, 27–30 July 2026 (poster,
  with an A0 poster kit and A4 handout in `poster/`).

---

## Phase 7 — 2026-05-29  (v1.0.1, r4 / AGI-26 camera-ready)

The paper was accepted at AGI-26 for poster presentation. This phase
incorporates substantive revisions in response to the three peer reviews,
plus the H3 algebra correction Reviewer 3 identified, and prepares the
camera-ready bundle that was uploaded to EasyChair on 2026-05-29.

### Framework changes

- **H3 sign correction.** The synergy term in the constitutive law was changed
  from `(1+γρτ)` to `(1−γρτ)`, with `γ ∈ [0, 1]` reinterpreted as a
  correlated-detection coefficient. Reviewer 3 identified that the published
  form algebraically *amplified* `R_eff`, contradicting the paper's claim that
  combined provenance and verification interventions outperform singletons.
  Numerical check: at `β=10, γ=1, ρ=τ=0.7`, the old form gave a joint
  reduction of 6.84 vs a sum-of-singletons reduction of 10.58. The corrected
  form preserves the threshold-crossing claim of H3 (only the high-ρ, high-τ
  condition crosses below `R_eff = 1` in moderate-β regimes).
- **H3 prediction reformulated** from "outperforms the sum of singleton
  interventions" (which is impossible for any multiplicative model) to a
  threshold-crossing claim: only the high-ρ, high-τ condition produces
  self-healing cascade behaviour at moderate `β`.
- **Tier-2 substantive additions** in the manuscript:
  - Formal Nash specification of the Freezing Equilibrium with explicit
    payoffs (Reviewer 1).
  - Structural-vs-heuristic classification of the four hypotheses against
    metamaterial physics (Reviewers 1 and 3).
  - Relation to W3C Verifiable Credentials in the Class C section
    (Reviewer 3).
  - AI-assisted verification paragraph addressing the human-bounded
    `C_ver` assumption (Reviewer 2).
  - Hawthorne-effect mitigation and operational `ρ`, `τ`, `γ` measurement
    in the pilot design (Reviewers 1, 2).

### Code changes

- `code/cm/constitutive.py`: `r_eff()` sign flip; γ docstring updated to
  `∈ [0, 1]` (correlated-detection convention).
- `code/tests/test_constitutive.py`: hardcoded expected value at
  `β=10, ρ=τ=0.5, γ=1` updated from 3.125 to 1.875; corner-case docstrings
  reflect the new sign. All 14 tests pass; full `cm/` test pass.
- `code/figures/fig02_phase_transition.py`: docstring sign updated; rendered
  figure regenerated under the new convention.
- `code/figures/fig05_sensitivity_analysis.py` and rendered figure: `τ*`
  values recomputed under the new sign — bilinear 0.860 → 0.694, additive
  0.882 → 0.570, quadratic 0.829 → 0.766. Sensitivity-analysis prose in the
  paper now honestly reports the wider spread.

### Paper / repository structure

- `paper/civilizational-metamaterials-agi26-r3.tex` and `references-r3.bib`
  moved to `drafts/r3/` to preserve the historical revision alongside r1, r2.
- `paper/` now holds the r4 sources: `.tex`, `references-r4.bib`,
  `.bbl`, compiled `.pdf`.
- `paper/Makefile` and `paper/build.sh`: `TEX` variable updated to
  `civilizational-metamaterials-agi26-r4`.
- `paper/preprint/`: r3 PDF removed; `civilizational-metamaterials-agi26.pdf`
  (generic name, r4 content) and `civilizational-metamaterials-preprint.pdf`
  (r4 content) in place.
- `docs/civilizational-metamaterials-agi26-r3.pdf` renamed to
  `civilizational-metamaterials-agi26.pdf` (r4 content); `preprint.pdf` and
  `paper.pdf` overwritten with r4 content.
- `docs/index.html`: cover-image link and visible filename text updated to
  the generic `civilizational-metamaterials-agi26.pdf`.
- `paper/arxiv/`: unchanged in this commit. arXiv submission was updated
  in-place via the arXiv web UI (submission `submit/7513752` still on hold
  as of this commit; replaced with r4 source bundle on 2026-05-29).

### Bibliography

- 8 entries added: W3C Verifiable Credentials, Hussey & Hughes 2007
  (stepped-wedge design effect), Dafoe 2018, Critch & Krueger 2020 (ARCHES),
  Carlsmith 2022, Drexler 2019 (CAIS), Orban 2025 (Jolting Technologies,
  arXiv:2507.06398), Orban 2025 (AI Paradox Report).
- 1 entry removed: Rao 2010 (Ribbonfarm blog) — Reviewer 1 flagged as
  non-peer-reviewed; replaced with primary citation Scott 1998 which was
  already in the bibliography.
- DOIs / URLs added to every previously bare arXiv preprint and to every
  journal article with a known DOI. 30 of 36 entries in r4's bibliography
  now carry a clickable link in the rendered PDF (the remaining 6 are books
  and IETF Internet-Drafts identified by their canonical non-DOI
  identifiers).
- Dafoe and Drexler entries cite via Internet Archive snapshots because the
  original `fhi.ox.ac.uk` host is defunct after FHI's 2024 closure.

### Typesetting

- All overfull `hbox` warnings cleared. The 41.8pt overrun in the Nash
  formalization paragraph on page 2 was eliminated by pulling the payoffs
  into an `align*` block and dropping the unbreakable `$a_i \in \{...\}$`
  math group. Smaller overfulls cleared by adding `\setlength{\emergencystretch}{2em}`
  and `\usepackage[protrusion=true,expansion=false]{microtype}` to the
  preamble.
- Page count: r3 was 17 pages; r4 is 19 pages (body 16.7 + references 2.3).
  The 2-page increase reflects the Tier-2 additions.

### Citation

- `CITATION.cff`: `version` bumped from `0.1.0-r3` to `0.1.0-r4`;
  `date-released` set to 2026-05-29; `status` updated to "Accepted for
  poster presentation at AGI-26. To appear in Springer LNAI."; arXiv
  identifier added (currently `submit/7513752`, to be updated to the
  permanent ID on approval).

### Manual steps remaining

1. When arXiv approves the submission, update `CITATION.cff` `identifiers`
   entry and `docs/index.html` `#arxiv-link` with the permanent arXiv ID.
2. When Springer publishes the LNAI volume and assigns a DOI, uncomment the
   `preferred-citation` block in `CITATION.cff` and fill the DOI.
3. (Optional) Regenerate `paper/arxiv/civilizational-metamaterials-agi26-r4-arxiv.tar.gz`
   if the Makefile `arxiv` target should be re-run for the new revision.

## Phase 6 — 2026-04-23  (v1.0.0)

### Added / Changed

- Final README polish: fixed COLLABORATION.md link, up-to-date repository map.
- CHANGELOG.md: all six phases documented.
- `v1.0.0` tag created on main. On push, Zenodo will mint the archival DOI.
- Once the DOI is available: update `CITATION.cff` (`doi:` field),
  update `docs/index.html` (`#doi-placeholder`), and push arXiv v1.

### Manual steps remaining for the author

1. Push the tag: `git push origin v1.0.0`
2. Enable the Zenodo–GitHub webhook at https://zenodo.org/account/settings/github/
3. Copy the Zenodo DOI into `CITATION.cff` (`doi:`) and `docs/index.html` (`#doi-placeholder`).
4. Flip `CITATION.cff` `status:` to `"Accepted, AGI-26. To appear in Springer LNCS/LNAI."` on acceptance.
5. Submit arXiv preprint; update `docs/index.html` `#arxiv-link` with the real URL.

## Phase 5 — 2026-04-23

### Added

- `experiments/README.md` — trial overview and quick-start guide.
- `experiments/protocol/protocol-v0.1.md` — full stepped-wedge CRT protocol draft.
- `experiments/protocol/consent-form-template.md` — informed consent template.
- `experiments/protocol/SAP.md` — pre-specified statistical analysis plan.
- `experiments/protocol/preregistration-OSF.md` — OSF/AsPredicted template, ready to paste.
- `experiments/power/power_analysis.py` — ICC sensitivity, design effect, power curves.
- `experiments/power/power_curves.pdf` — pre-generated power curves (ICC ∈ {0.01,0.05,0.10,0.15}).
- `experiments/instruments/data-dictionary.md` — variable definitions.
- `experiments/instruments/verification-timer-app/index.html` — standalone browser timer for τ measurement.
- `experiments/synthetic/generate_synthetic_panels.py` — generates synthetic panel-level fixtures.
- `experiments/synthetic/fixtures/panels_h1.csv` and `panels_h234.csv` — pre-generated synthetic data.
- `experiments/analysis/primary_endpoint.py` — H1 logistic regression analysis.
- `experiments/analysis/secondary_h2_h4.py` — H2 synergy, H3 anisotropy, H4 hysteresis.
- `experiments/analysis/simulate_trial.py` — Monte Carlo under null/alternative; reports type-I error, power, bias.

All scripts marked as **proposed, not registered** — no IRB filing has been made.

## Phase 4 — 2026-04-23

### Added

- `code/figures/fig01_decision_verification_gap.py` — wrapper that compiles `fig01_decision_verification_gap.tex` via pdflatex.
- `code/figures/fig01_decision_verification_gap.tex` — TikZ standalone source for Fig. 1.
- `code/figures/_composite.py` — shared PIL layer compositor (alpha-composites numbered PNG layers → PDF).
- `code/figures/fig03_provenance_taxonomy.py` — composites `figures/layers/fig03-layers/`.
- `code/figures/fig04_freezing_equilibrium.py` — composites `figures/layers/fig04-layers/`.
- `code/figures/fig06_coordination_anisotropy.py` — composites `figures/layers/fig06-layers/`.
- `code/figures/fig07_trial_design.py` — composites `figures/layers/fig07-layers/`.
- `code/figures/fig08_trust_anchors.py` — composites `figures/layers/fig08-layers/`.
- `code/figures/fig09_metamaterial_analogy.py` — composites `figures/layers/fig09-layers/`.
- `code/figures/fig10_synthetic_principals.py` — composites `figures/layers/fig10-layers/`.
- `paper/Makefile` — `make figures` target updated to rebuild all 10 figures.
- `.github/workflows/figures.yml` — updated to regenerate all 10 figures on CI.

## Phase 3 — 2026-04-23

### Added

- `code/cm/constitutive.py` — `r_eff()`, `tau_star()`, `phase_boundary()`, fully vectorized.
- `code/cm/branching.py` — Monte Carlo branching-process simulator with population cap.
- `code/cm/sensitivity.py` — OAT sweeps and Sobol first-order + total indices (SALib).
- `code/cm/anisotropy.py` — Directional coordination tensor and anisotropy index.
- `code/cm/plotting.py` — Shared LNCS style, color constants, figure factory.
- `code/cm/__init__.py` — Package entry point.
- `code/tests/test_constitutive.py`, `test_branching.py`, `test_sensitivity.py`,
  `test_anisotropy.py`, `test_plotting.py` — 52 tests, 97% coverage on `cm/`.
- `code/figures/fig02_phase_transition.py` — Reproduces Fig. 2 computationally.
- `code/figures/fig05_sensitivity_analysis.py` — Reproduces Fig. 5 computationally.
- `code/pyproject.toml`, `code/requirements.txt`, `code/README.md`.
- `.github/workflows/tests.yml` — pytest + coverage ≥ 90% on push to `code/**`.
- `.github/workflows/figures.yml` — Regenerates fig02 and fig05, uploads artifacts.

## Phase 2 — 2026-04-23

### Added

- `docs/index.html` — one-page website with masthead, abstract, formula (MathJax),
  hero figure, four-contribution cards, hypotheses table, experiment section,
  BibTeX block with copy button, reproduce block, and footer.
- `docs/assets/css/style.css` — responsive styles, dark-mode via prefers-color-scheme,
  system font stack, no tracking, <100 kB total.
- `docs/assets/js/reff-explorer.js` — interactive slider widget for R_eff phase diagram.
- `docs/assets/img/fig02-phase-transition.png` — hero PNG exported from PDF at 150 dpi.
- `docs/assets/img/og-card.png` — Open Graph / Twitter card image.
- `docs/CNAME` — custom domain `metamaterials.davidorban.com`.
- `.github/workflows/pages.yml` — deploys docs/ to GitHub Pages via actions/deploy-pages@v4;
  runs lychee link-check and html-validate.

## Phase 1 — 2026-04-23

### Added

- `paper/civilizational-metamaterials-agi26-r3.tex` — r3 camera-ready TeX source.
- `paper/references-r3.bib`, `paper/llncs.cls`, `paper/splncs04.bst` — vendored bibliography and Springer class files for a hermetic build.
- `paper/build.sh` and `paper/Makefile` — one-shot build (`make paper`) and clean (`make clean`).
- `paper/preprint/civilizational-metamaterials-agi26-r3.pdf` — committed build artifact.
- `figures/` — all ten canonical figure PDFs (fig01–fig10).
- `figures/fig01-tikz.pdf` — the TikZ figure referenced by the paper TeX source.
- `figures/layers/fig0{1–10}-layers/` — layered PNG assets for all figures.
- `figures/LAYER_INDEX.md` — layer inventory and color constants.
- `drafts/r1/` and `drafts/r2/` — prior TeX and BibTeX revisions kept for provenance.
- `peer-review/` — full review thread and author rebuttals (all five files).
- `.github/workflows/build-paper.yml` — CI: compile on push to `paper/**` or `figures/**`; attach PDF to tagged releases; refresh `docs/paper.pdf`.
- `.github/ISSUE_TEMPLATE/errata.md` and `replication.md` — structured issue templates.
- `.github/PULL_REQUEST_TEMPLATE.md` and `.github/CODEOWNERS`.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1), `COLLABORATION.md`.
- `docs/CNAME` — custom domain `metamaterials.davidorban.com`.

---

## Paper revision r3 — 2026-04-15 *(current submission)*

Corrections to computational artefacts. No substantive content changes from r2.

### Fixed

- Sensitivity analysis: corrected synergy formulas and τ* values (`β = 10`,
  `γ ∈ {0, 0.5, 1, 2}` cases). Qualitative conclusions unchanged.

---

## Paper revision r2 — addressing R1 reviewer suggestions

All five R1 suggestions incorporated in camera-ready style.

### Added

- Institutional grounding for the bandgap mechanism (H1): periodic-structure
  analog explicitly mapped to institutional review cadences.
- Directional R_eff decomposition formalised for H2: within-unit vs.
  cross-boundary components written out.
- Worked numerical example in the sensitivity analysis section.
- Ostrom citation in the Contributions paragraph.

### Fixed

- OMB reference correction.

### Context

- Reviewer score 1 → 2, confidence 3 → 4. Decision outlook: accept with
  camera-ready improvements.

---

## Paper revision r1 — addressing R0 (initial) review

Substantive revisions addressing the four critical issues (C1–C4) and four
important issues (I1–I4) raised in the first review.

### Added

- **§2 (new opening paragraph)**: situates R_eff in the branching-process and
  cascade-failure literature (Anderson & May 1991; Hethcote 2000;
  Watts 2002; Buldyrev et al. 2010). Recalibrates the novelty claim to the
  *institutional parameterization* (designable β, governance-specific
  ρ/τ decomposition, measurable provenance taxonomy).
- **§1 (new paragraph)**: distinguishes the metamaterial analogy's heuristic
  function (organizing disparate phenomena) from its generative function
  (importing structural predictions absent from plain branching models).
- **§2.1**: R_eff reframed as a phenomenological ansatz (in the sense of
  Hooke's law or Ohm's law); multiplicative structure justified via a
  sequential-filter argument; synergy term γρτ justified as the simplest
  bilinear interaction vanishing when either ρ or τ is zero.
- **§6.1**: H1, H2, H4 sharpened to show what the analogy adds beyond generic
  branching.
  - H1 (Bandgap): predicts exponential-tail cutoff vs. power-law tails.
  - H2 (Anisotropy): within-unit vs. cross-boundary directional R_eff
    — a tensor concept absent from scalar branching.
  - H4 (Hysteresis): moderated to acknowledge as the weakest analogical
    import.
- **§6.3 (new)**: Ethical safeguards for the experimental design. Tracer
  errors target synthetic calibration applications, not real submissions;
  IRB approval required; informed consent with post-hoc debriefing; no real
  applicant disadvantaged.
- **§1 (after Eq. 1)**: Worked example for the Freezing Equilibrium using
  environmental-regulatory permit review.
- **§4**: Citations to Chan et al. (2024) on AI agent visibility and
  Shavit et al. (2023) on AI delegation chains; situated synthetic principals
  within emerging multi-agent literature.
- **§3 (new paragraph)**: Provenance taxonomy mapped onto NIST AI RMF and
  ISO 42001, showing where context binding extends existing controls.
- **§6.2 (expanded)**: Explicit power-analysis assumptions (ICC = 0.05,
  CV = 0.3, design effect), sensitivity table for ICC ∈ {0.01, 0.05, 0.10, 0.15},
  panel stratification discussion.
- **§7.3 (new)**: Sensitivity analysis showing how the critical threshold
  shifts under alternative synergy specifications.

### Context

- Reviewer score on initial submission: 1 (Weak Accept). Upgraded to 2 on r1.

---

## Paper revision r0 — initial AGI-26 submission

First submission to the AGI-26 review process.
