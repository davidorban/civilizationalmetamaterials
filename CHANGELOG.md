# Changelog

All notable revisions to the paper and the repository are recorded here. The
paper's revision history reflects the AGI-26 peer-review rounds.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/),
adapted for an academic repository.

---

## [Unreleased]

---

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
