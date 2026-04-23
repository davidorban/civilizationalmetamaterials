# Statistical Analysis Plan (SAP) v0.1

**Study:** Civilizational Metamaterials — Stepped-Wedge CRT
**Version:** 0.1 (pre-specified, not yet locked)
**Date:** 2026-04-23

> This SAP will be locked on OSF before primary data collection begins.
> Any post-hoc analysis will be labelled as exploratory.

---

## 1. Primary analysis — H1

### Outcome
Binary: did the panel's empirical R_eff cross 1 during the observation period?

R_eff is estimated as:
```
R_eff_hat = beta_hat × (1 − rho_hat) × (1 − tau_hat) × (1 + gamma_hat × rho_hat × tau_hat)
```
where β_hat is estimated from the panel's mean AI-generated decision branching
factor (observable from the logging system), ρ_hat from provenance fidelity,
τ_hat from verification rate, and γ_hat from OLS regression of joint effects
on R_eff reduction.

**Crossing** is defined as: estimated R_eff_hat < 1 in ≥ 2 of the 4 weekly
estimates within the period.

### Model
Mixed-effects logistic regression (GLMM):

```
logit(P(crossing_ij)) = α + β_1 × treatment_ij + β_2 × period_j + u_i
```

where i indexes panel (cluster), j indexes period, treatment_ij is 1 in
intervention periods, and u_i ~ N(0, σ²_u) is the random cluster effect.

### Estimator
`glmer()` in R with `family = binomial(link = "logit")`.
Maximum likelihood via adaptive Gauss-Hermite quadrature (nAGQ = 20).

### Inference
Primary estimate: β_1 (log-OR of crossing in intervention vs. control periods).
95% CI by Wald. Two-sided p-value at α = 0.05.

### Sensitivity analyses
1. Replace GLMM with GEE (exchangeable correlation) as a robustness check.
2. Repeat with ICC ∈ {0.01, 0.05, 0.10} (mis-specification sensitivity).
3. Exclude calibration-only periods.

---

## 2. Secondary analysis — H2 (synergy)

### Outcome
Superadditivity: does the joint effect of ρ and τ exceed the sum of
individual effects?

### Method
If factorial sub-allocation is feasible (panels randomized to ρ-only,
τ-only, or joint), estimate:
```
H2: β_joint > β_ρ + β_τ   (i.e., interaction term > 0)
```
via logistic regression with interaction term and Wald test on the interaction.

If factorial sub-allocation is not feasible, estimate synergy from the
continuous correlation between observed (ρ, τ) pairs and R_eff reduction,
testing whether γ_hat > 0 with a one-sided t-test.

---

## 3. Secondary analysis — H3 (anisotropy)

### Outcome
Directional asymmetry: within-panel coordination improvement ≠ cross-panel
coordination improvement.

### Method
Estimate:
```
R_eff_within = r_eff(β, ρ_within, τ_within, γ)
R_eff_cross  = r_eff(β, ρ_cross,  τ_cross,  γ)
```
from logged data (within-panel and cross-panel decisions are tagged separately
by the scaffolding system). Test H3: |R_within − R_cross| > 0 via a
paired t-test on within- and cross-boundary R_eff estimates.

---

## 4. Secondary analysis — H4 (hysteresis)

### Outcome
Asymmetric recovery: panels take longer to recover post-withdrawal than the
original improvement took.

### Method
If an extension phase (post-step) is feasible, measure:
- τ_improvement: weeks from crossing start to R_eff < 1
- τ_recovery: weeks from crossing end to R_eff > 1

Test H4: τ_recovery > τ_improvement via a one-sided Wilcoxon signed-rank test
on matched panel pairs.

This analysis is opportunistic (feasible only if Cohort A has an extension
period) and is marked as exploratory.

---

## 5. Handling of missing data

- If ≥ 25% of weekly estimates are missing for a panel-period, that period is
  excluded from the analysis.
- Multiple imputation (m = 20, predictive mean matching) for partially observed
  covariates.
- A sensitivity analysis with complete-case only is pre-specified.

---

## 6. Multiple comparisons

No adjustment for multiple testing across H1–H4 (the four hypotheses are
pre-specified as distinct a priori predictions, not a family). However, H2–H4
are explicitly labelled secondary/exploratory and are not used to claim
primary efficacy.

---

## 7. Interim analysis and stopping rules

No formal interim analysis is planned. If a safety concern arises (e.g., any
panel shows sustained R_eff > 10), the panel chair may request unblinding.

---

## 8. Software

R ≥ 4.3 with `lme4` (≥ 1.1), `gee` (≥ 4.13), `mice` (≥ 3.16).
Python scripts in `analysis/` reproduce results using `statsmodels` and
`scipy`.
