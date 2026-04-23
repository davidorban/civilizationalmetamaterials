# Experiments — Proposed Trial Scaffolding

> **Status: PROPOSED, NOT YET REGISTERED.**
> No IRB application has been filed. No real participants have been enrolled.
> All analysis scripts run against synthetic data only.

This directory contains everything a collaborating institution needs to pilot
the stepped-wedge cluster-randomized trial described in §Empirical of the paper.

See [`COLLABORATION.md`](../COLLABORATION.md) if you are interested in running
the protocol with real grant review panels.

---

## Structure

```
experiments/
├── protocol/
│   ├── protocol-v0.1.md          — Full protocol draft
│   ├── consent-form-template.md  — Informed consent template
│   ├── SAP.md                    — Statistical analysis plan
│   └── preregistration-OSF.md   — OSF pre-registration template (ready to paste)
├── power/
│   ├── power_analysis.py         — ICC assumptions, cluster×period sizing
│   └── power_curves.pdf          — Publication-quality power curves (pre-generated)
├── instruments/
│   ├── data-dictionary.md        — Variable definitions
│   ├── provenance-checklist.pdf  — Class A/B/C rubric for reviewers
│   └── verification-timer-app/  — Lightweight web timer for τ measurement
├── synthetic/
│   ├── generate_synthetic_panels.py  — Generates fixtures/
│   └── fixtures/                 — Synthetic panel-level datasets
└── analysis/
    ├── primary_endpoint.py       — H1: phase-transition crossing
    ├── secondary_h2_h4.py        — H2 synergy, H3 anisotropy, H4 hysteresis
    └── simulate_trial.py         — Monte Carlo under null / alternative
```

## Quick start (synthetic data only)

```bash
cd experiments

# Generate synthetic panel data
python synthetic/generate_synthetic_panels.py

# Run power analysis
python power/power_analysis.py --out power/power_curves.pdf

# Run analyses against synthetic data
python analysis/primary_endpoint.py  --data synthetic/fixtures/panels_h1.csv
python analysis/secondary_h2_h4.py   --data synthetic/fixtures/panels_h234.csv
python analysis/simulate_trial.py
```

## The proposed design

**Design:** 12-week stepped-wedge CRT.
**Units:** Government grant review panels (≥ 6 panels required).
**Intervention:** Class A/B/C provenance scaffolding system.
**Primary endpoint:** Binary — did the panel's decision process cross R_eff = 1 during
the observation window?
**Secondary endpoints:** Synergy (H2), anisotropy (H3), hysteresis (H4).

Full details: [`protocol/protocol-v0.1.md`](protocol/protocol-v0.1.md).
