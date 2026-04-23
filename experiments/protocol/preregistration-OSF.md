# OSF Pre-Registration Template

> Paste this into OSF → My Projects → New Registration → AsPredicted.
> Fill in the bracketed fields before registering.

---

## 1. Have data collection begun for this study?

No.

## 2. What is the main question being asked?

Does deploying a Class A/B/C provenance scaffolding system in grant review
panels cause those panels to cross from the turbulent regime (R_eff > 1) to
the self-healing regime (R_eff < 1) of the constitutive law
R_eff = β(1−ρ)(1−τ)(1+γρτ)?

## 3. Describe each planned hypothesis

**H1 (primary):** Panels receiving the intervention will have a significantly
higher probability of crossing R_eff = 1 during the intervention period
compared to panels in the control condition, with a log-odds ratio > 0.

**H2 (secondary):** The joint effect of ρ and τ interventions on R_eff
reduction is superadditive (synergy term γ_hat > 0 with p < 0.05, one-sided).

**H3 (secondary):** Coordination improvement will be directionally asymmetric:
within-panel R_eff reduction will exceed cross-panel R_eff reduction.

**H4 (exploratory):** If an extension phase is available, recovery time
post-intervention removal will exceed improvement time (hysteresis).

## 4. Describe the key dependent variable(s)

Binary primary outcome: whether the panel's estimated R_eff crossed from > 1
to < 1 during the observation period (see SAP.md for the crossing criterion).

Secondary: continuous R_eff_hat estimates per period; within- and cross-panel
R_eff estimates.

## 5. Describe exactly which analyses will be conducted

See `experiments/protocol/SAP.md`. Primary analysis: GLMM with logit link,
period fixed effects, cluster random effects. Inferential criterion: two-sided
p < 0.05 on the treatment coefficient.

## 6. Describe exactly what exclusion criteria will be used

- Panels with < 10 reviews per period excluded from that period.
- Panel-periods with > 25% missing weekly estimates excluded.
- Calibration-only periods excluded from primary analysis.

## 7. How many observations will be collected?

Target: 9 panels × 4 periods × ~20 reviews/period = ~720 review-level observations.
Statistical power: 80% at OR = 2.5, ICC = 0.05 (see power_curves.pdf).

## 8. Anything else to pre-register?

The synthetic data generator (`experiments/synthetic/generate_synthetic_panels.py`)
and analysis scripts (`experiments/analysis/`) are committed at
[COMMIT HASH BEFORE REGISTRATION] on
https://github.com/davidorban/civilizationalmetamaterials.

The SAP hash (SHA-256 of `experiments/protocol/SAP.md`) is:
[COMPUTE AND INSERT BEFORE REGISTERING]

---

*Registration date: [DATE]*
*OSF registration URL: [URL]*
