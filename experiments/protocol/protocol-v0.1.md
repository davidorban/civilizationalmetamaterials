# Protocol v0.1: Stepped-Wedge Cluster-Randomized Trial

**Title:** Civilizational Metamaterials — Phase Transition Detection in
Government Grant Review Panels

**Version:** 0.1 (draft — not registered)
**Date:** 2026-04-23
**Contact:** David Orban <david@davidorban.com>

> This is a **proposed, not registered** protocol. No IRB approval has been
> sought. This document is intended as a template for institutions that wish
> to pilot the design.

---

## 1. Background and rationale

The paper (§Empirical) argues that institutional review panels can be modelled as
branching processes with effective reproduction number
R_eff = β(1−ρ)(1−τ)(1+γρτ). When R_eff > 1, unverified decisions cascade;
when R_eff < 1, they decay. Four hypotheses (H1–H4) predict observable
consequences of crossing the critical threshold.

A stepped-wedge CRT is appropriate because:
- The intervention (provenance scaffolding) is ethically obligatory to deploy
  eventually across all clusters if H1 is supported.
- Temporal trends within panels can be controlled.
- The design provides both within- and between-cluster comparisons.

---

## 2. Objectives

### Primary
Estimate the effect of the Class A/B/C provenance scaffolding intervention
on the binary outcome: does the panel cross R_eff = 1 during the
observation window? (H1)

### Secondary
- H2: Superadditivity of joint ρ and τ improvements.
- H3: Directional asymmetry of coordination improvements (anisotropy).
- H4: Asymmetric recovery on intervention withdrawal (hysteresis).

---

## 3. Design

| Feature | Value |
|---|---|
| Design | Stepped-wedge CRT |
| Clusters | Government grant review panels (target: 9 panels minimum) |
| Steps | 3 steps of 4 weeks each = 12 weeks total |
| Cohorts | 3 cohorts of 3 panels, crossing sequentially |
| Observation periods | 4 per cluster (1 control + 3 post-crossing) |
| Unit of randomization | Panel (cluster) |

### Stepped-wedge schedule

```
Week:       0-4    4-8    8-12
Cohort A:   C      I      I
Cohort B:   C      C      I
Cohort C:   C      C      C
```

C = control (standard panel operation)
I = intervention (provenance scaffolding active)

---

## 4. Participants

### Inclusion criteria
- Government or foundation grant review panel with ≥ 4 active reviewers.
- Panel reviews ≥ 10 applications per 4-week period.
- Panel chair consents to intervention deployment.

### Exclusion criteria
- Panels with ongoing related interventions.
- Panels with < 50% reviewer attendance rate in the prior cycle.

---

## 5. Intervention

The intervention has three layers, deployed simultaneously:

**Class A (cryptographic provenance):** Each AI-generated decision summary is
accompanied by a cryptographic hash and timestamp. Reviewers are notified when
a summary is AI-generated.

**Class B (institutional provenance):** Each summary identifies the source model,
version, and institutional authority that authorized its use.

**Class C (context binding):** AI summaries are bound to the specific application
context — model inputs are logged and linked to the output. Reviewers can inspect
the binding chain.

Implementation: a lightweight browser extension + panel chair dashboard.
See `instruments/verification-timer-app/` for the τ measurement component.

---

## 6. Control condition

Standard panel operation — no provenance labelling, no verification timer.

---

## 7. Outcomes

### Primary outcome
Binary: did the panel's empirical R_eff cross 1 during the period? Estimated
from the proportion of unverified decisions that were subsequently adopted
without further review.

### Secondary outcomes
- **H2 (synergy):** Joint effect of ρ and τ interventions vs. individual effects.
  Measured by comparing panels receiving both components vs. each component alone
  (if factorial sub-allocation is feasible).
- **H3 (anisotropy):** Within-panel vs. cross-panel coordination change.
  Measured via timer data on within-panel and cross-panel decisions.
- **H4 (hysteresis):** Recovery time after intervention removal.
  Measured in Cohort A post-step-back (if feasible in extension period).

### Process measures
- τ (verification rate): fraction of submitted AI summaries reviewed by a human
  before decision (measured via verification timer).
- ρ (provenance fidelity): fraction of summaries with complete Class A/B/C
  attribution (measured from the scaffolding dashboard).

---

## 8. Randomization

Panels are stratified by domain (e.g., life sciences, engineering, social
sciences) and expected review volume. Within strata, panels are randomly
allocated to cohorts using a computer-generated sequence (R: `set.seed(2026)`).

---

## 9. Blinding

Reviewers are not blinded to the intervention (overt provenance labels are the
intervention). Analysts are blinded to cohort allocation until the primary
analysis is complete.

---

## 10. Sample size

See `power/power_analysis.py` and `power/power_curves.pdf`.

Key assumptions (from paper §6.2):
- ICC = 0.05 (intraclass correlation within panels)
- CV = 0.3 (coefficient of variation of cluster sizes)
- Design effect ≈ 1 + (m̄ − 1) × ICC where m̄ ≈ 20 reviews/period
- Target power: 80% at α = 0.05 (two-sided)
- Detectable effect: OR ≥ 2.5 for primary endpoint crossing

With 9 clusters × 4 periods × 3 steps → ~80% power under these assumptions.
Sensitivity table in `power/power_curves.pdf`.

---

## 11. Statistical analysis

See `SAP.md` for the pre-specified analysis plan.

Primary analysis: mixed-effects logistic regression with period fixed effects
and cluster random effects (GLMM). Model:

```
logit(P(crossing)) = α + β_treatment + β_period + u_cluster
```

---

## 12. Ethical considerations

- All panel reviewers provide informed consent before enrolment (see
  `consent-form-template.md`).
- Tracer errors (synthetic calibration applications) target only designated
  calibration slots, not live applications affecting real grant decisions.
- IRB or ethics board approval is required before deployment.
- Informed consent includes post-hoc debriefing about the tracer design.
- No real applicant is disadvantaged: calibration applications are identified
  and excluded from funding decisions.

---

## 13. Timeline

| Week | Milestone |
|------|-----------|
| −4 | IRB submission |
| −2 | Panel chair recruitment and baseline data collection |
| 0  | Randomization |
| 0–4 | Control period (all cohorts) |
| 4  | Cohort A crosses to intervention |
| 8  | Cohort B crosses to intervention |
| 12 | End of follow-up; primary analysis begins |
| 14 | Unblinding; secondary analyses |
| 16 | Report and dissemination |

---

## 14. Registration

This protocol will be registered on OSF before enrolment begins.
See `preregistration-OSF.md` for the draft registration form.

---

## 15. Changes from previous versions

v0.1 (2026-04-23): Initial draft.
