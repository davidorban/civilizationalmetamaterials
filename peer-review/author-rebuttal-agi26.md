# Author Rebuttal — AGI 2025 Conference Proceedings

We thank the reviewer for a thorough, constructive, and intellectually engaged review. The careful steelmanning of our contribution and the honest declaration of review limitations reflect the kind of scholarly professionalism we aspire to reciprocate. Below we address each concern systematically.

---

## Phase 1: Paper Context Setup

**Paper Overview:**
- **Title:** Civilizational Metamaterials: Engineering Coordination Under Capability Gradients and Structural Turbulence
- **Field:** AGI governance / institutional design / coordination theory
- **Primary Contribution:** A formal constitutive law (R_eff) that quantifies institutional stability under AGI-accelerated decision velocity, predicting a sharp phase transition between self-healing and self-destabilizing regimes.
- **Secondary Contributions:** (i) A three-class provenance taxonomy identifying context binding as an underserved class; (ii) a treatment of AI agents as "synthetic principals" requiring distinct governance primitives; (iii) four falsifiable hypotheses with a concrete experimental design.
- **Venue:** AGI-26 Conference (Springer LNCS/LNAI proceedings)

**Review Summary:**
- **Overall Sentiment:** Positive but reserved. The reviewer recognizes the paper's intellectual seriousness, falsifiability posture, and the context-binding contribution, while raising substantive concerns about the metamaterial analogy's predictive content and the paper's engagement with prior literature.
- **Common Themes:** (i) Whether the metamaterial framing adds predictive content beyond standard branching-process models; (ii) insufficient engagement with epidemiological and network-cascade literatures; (iii) the constitutive law's functional form is asserted rather than derived; (iv) ethics of the tracer-error experimental methodology.
- **Decision Outlook:** Weak Accept (Score: 1). The paper is above threshold but the concerns, if unaddressed, could tip a borderline PC discussion toward rejection.

---

## Phase 2: Strategic Triage

**Critical Path Analysis:**

1. **The metamaterial analogy's predictive content vs. rhetorical framing** — Reviewer, Sections 2.2, 2.3, 2.4 (Critical Issue #3) — This is potentially fatal because it challenges whether the paper's titular and organizing concept carries analytical weight. If the PC agrees the analogy is purely decorative, the paper's novelty claim collapses to "branching process + provenance taxonomy," which, while publishable, substantially undersells what we believe the framework offers.

2. **Missing engagement with branching-process and cascade-failure literatures** — Reviewer, Section 2.2 (Critical Issue #1) — This matters because it makes the novelty claim appear overcalibrated. The omission is a genuine gap: we should have cited this lineage and explained what our institutional parameterization adds.

3. **Ethics of tracer-error injection** — Reviewer, Sections 2.3, 2.4 (Critical Issue #4) — This could be fatal at the experimental design level. An IRB-unaddressed methodology undermines the paper's claim to empirical accountability.

**Conflicting Reviewer Opinions:** Not applicable (single reviewer).

---

## Phase 3: Reviewer-by-Reviewer Analysis

## Reviewer 1 — Overall Assessment: Score 1 (Weak Accept), Confidence 3

### Major Comments

---

**Reviewer Point #1: The metamaterial analogy does not clearly deliver predictive content beyond a standard branching-process model. The four hypotheses (H1–H4) follow from branching-process mathematics, not from metamaterial physics. The paper should either demonstrate unique predictions imported from metamaterial physics or moderate the claim.**

**Author Response:**

We accept that the current manuscript does not sufficiently distinguish the metamaterial framing's predictive contribution from what a plain branching model yields. This is a fair and important criticism. However, we respectfully submit that the reviewer partially understates what the analogy contributes, and we propose revisions that sharpen the distinction.

The reviewer is correct that the *phase transition itself* (R_eff = 1) is a mathematical property of branching processes in general. We do not claim otherwise, though we accept that the manuscript's presentation blurs this. We will revise Section 2.2 to state explicitly: "The phase transition at R_eff = 1 is inherited from the branching-process model class and is not a novel prediction of the metamaterial framing per se."

What the metamaterial analogy *does* contribute beyond a generic branching model is threefold, and we will make this case more precisely in the revision:

(a) **The bandgap concept imports a structural prediction that generic branching models do not naturally express.** In a standard branching process, sub-critical R_eff means errors decay on average, but rare large cascades remain possible. In metamaterial physics, a bandgap is a *forbidden band*: certain frequencies literally cannot propagate. Hypothesis H1 distinguishes these — it predicts not merely average decay but a *sharp cutoff* in the error propagation depth distribution (exponential decay replacing a power-law tail). This is a stronger prediction than "R_eff < 1," and it is directly testable by comparing tail behavior. We will revise Section 6.1 to make this distinction explicit.

(b) **Anisotropy (H2) is a tensor concept that branching models, which are typically isotropic, do not naturally generate.** The prediction that coordination improvements are directional — that within-unit acceleration can *worsen* cross-boundary coordination — is motivated by the metamaterial concept of anisotropic response (different effective properties in different directions). A generic branching model with a scalar R_eff does not predict directional effects. We will revise Section 6.1 to introduce a directional decomposition of R_eff (within-unit vs. cross-boundary) to formalize this.

(c) **Hysteresis (H4) is motivated by the metamaterial concept of structural memory.** While path dependence exists in many dynamical systems, the specific prediction that withdrawal cost exceeds adoption cost by a factor >3 is motivated by the asymmetry between constructing and destroying microstructure in physical metamaterials. We acknowledge this is the weakest of the three analogical imports and will moderate the claim accordingly.

We will add a new paragraph in Section 1 that explicitly states: "The metamaterial analogy serves two functions: a heuristic one (organizing disparate governance phenomena under a single design language) and a generative one (importing structural predictions — bandgaps, anisotropy, hysteresis — that a plain branching model does not naturally produce). We distinguish these throughout."

*Internal Assessment:* Partially valid. The reviewer correctly identifies that we overclaim in places, but the analogy does carry some genuine predictive content that we have not articulated sharply enough. The fix is better argumentation, not abandonment of the framing.

---

**Reviewer Point #2: The paper does not engage with the well-established branching-process and cascading-failure literatures (Anderson & May, Hethcote, Watts, Buldyrev et al.). The novelty claim is overcalibrated without this context.**

**Author Response:**

The reviewer is correct, and this is an oversight we will fix. The R_eff formulation is indeed a member of the branching-process family, and the paper should have cited Anderson & May (1991), Hethcote (2000), Watts (2002), and Buldyrev et al. (2010) explicitly. The omission was not strategic — it reflects the paper's development trajectory from governance theory rather than mathematical epidemiology, but this is an explanation, not a justification.

In the revision, we will:

1. Add a new paragraph at the beginning of Section 2 situating the constitutive law within the branching-process tradition, citing the epidemiological lineage (Anderson & May 1991, Hethcote 2000) and the network cascade literature (Watts 2002, Buldyrev et al. 2010, Dobson 2024).

2. Articulate explicitly what the institutional parameterization adds beyond domain translation. The key differences are: (i) β is a *design variable* under institutional control, not an exogenous transmission rate — this means the sub-critical condition can be *engineered* rather than merely observed; (ii) the decomposition into ρ and τ with a synergy term γ provides governance-actionable intervention targets, whereas generic cascade models parameterize transmission as a single rate; (iii) the provenance taxonomy (Section 3) provides the institutional content that makes R_eff's parameters measurable in practice.

3. Recalibrate the novelty claim in Section 1 to: "We do not claim novelty for the branching-process framework itself, which has a long history in epidemiology and network science. Our contribution is the institutional interpretation that makes the model's parameters designable and the identification of context binding as a critical gap in current scaffolding."

*Internal Assessment:* Valid. This is a genuine gap in the manuscript. The fix is straightforward and will strengthen the paper.

---

**Reviewer Point #3: The functional form of R_eff (Eq. 2) is intuitively motivated but not derived from first principles. The multiplicative structure and the synergy term (1+γρτ) are ad hoc.**

**Author Response:**

We accept this criticism. The constitutive law is a phenomenological ansatz, not a first-principles derivation, and the manuscript should say so clearly. We will revise Section 2.1 as follows:

1. Add a framing paragraph: "We propose R_eff as a phenomenological constitutive law — a tractable model chosen because its parameters map directly onto designable institutional features, not because it is uniquely derivable from microstructural axioms. Like many constitutive laws in physics (Hooke's law, Ohm's law), its justification is ultimately empirical: the model is useful if its parameters can be estimated and its predictions verified."

2. Justify the multiplicative form more carefully: provenance and verification are modeled as independent sequential filters because, in the institutional architectures we target (hierarchical review panels), a claim passes through a provenance check *and then* a verification check at each node. If either catches the error, propagation halts. This gives the multiplicative (1−ρ)(1−τ) structure as the probability of passing through both filters. We will make this sequential-filter argument explicit.

3. Regarding the synergy term: the reviewer is correct that the specific form γρτ is one of several plausible interaction terms. We chose it as the simplest bilinear interaction that vanishes when either ρ or τ is zero (no synergy without both ingredients). We will note in the revision that the qualitative prediction of superadditivity (H3) is robust to functional form, but that the quantitative threshold values depend on the specific interaction term, which must be determined empirically. We will add a brief sensitivity analysis in the discussion showing how the critical threshold shifts under alternative synergy specifications (γ(ρ+τ), γρ²τ).

*Internal Assessment:* Valid. The paper presents assumption as derivation. The fix is transparency about the model's status as an ansatz plus better justification for the chosen functional form.

---

**Reviewer Point #4: The tracer-error methodology requires ethical review. Inserting false claims into real grant applications could affect real applicants' outcomes. The paper does not discuss IRB requirements or safeguards.**

**Author Response:**

The reviewer raises an important concern. We will add a new subsection (Section 6.3: "Ethical Safeguards") addressing the following:

1. **Tracer errors are injected into synthetic "calibration applications," not real applicants' submissions.** We did not make this sufficiently clear. The pilot design uses fabricated test applications that are reviewed alongside real applications but are flagged in the backend so they cannot affect funding outcomes. This is analogous to "mystery shopper" methodologies in service quality research, which have established IRB precedents.

2. **IRB/ethics board approval is required.** We will state this explicitly and note that the trial design must be reviewed by the participating agencies' research ethics boards before any implementation.

3. **Informed consent.** Reviewers in the scaffolded condition would be informed that the trial includes quality-assurance measures, though the specific nature of tracer errors would be disclosed only after the trial (to avoid invalidating the test). This follows standard deception-in-research protocols with post-hoc debriefing.

4. **No real applicant is disadvantaged.** Tracer errors are confined to synthetic applications; real applications are processed under standard or enhanced (scaffolded) procedures. The stepped-wedge design ensures all panels eventually receive the scaffolding intervention.

We acknowledge that this was a significant omission in the current manuscript.

*Internal Assessment:* Valid. The omission is a real gap, and the fix is substantive, not cosmetic.

---

**Reviewer Point #5: The power analysis lacks detail — effect size assumptions, intra-cluster correlation, and variance estimates are not shown. The assumption of 20 "comparable" panels is strong.**

**Author Response:**

We will expand Section 6.2 with:

1. **Explicit power analysis assumptions:** We assumed an intra-cluster correlation (ICC) of 0.05 (consistent with published ICCs for stepped-wedge trials in administrative settings; see Hemming et al. 2015, "The stepped wedge cluster randomised trial: rationale, design, analysis, and reporting," *BMJ*), a coefficient of variation of 0.3 for baseline cascade depth, and a design effect of 1 + (m−1)×ICC where m = 75 applications per panel.

2. **Panel comparability:** We will add a paragraph discussing stratification by domain (STEM vs. humanities vs. social science), panel size, and historical funding rate. We will also note that the stepped-wedge design partially addresses comparability concerns by using each panel as its own control across time periods.

3. **Sensitivity to ICC:** We will include a table showing required panel counts for ICC values of 0.01, 0.05, 0.10, and 0.15, demonstrating the design's robustness or fragility to this assumption.

*Internal Assessment:* Valid. The power analysis as presented is a sketch, not a protocol-ready specification. The revision will bring it to the expected level of detail.

---

### Minor Comments

**β / β_c notation overlap:** Agreed. We will rename the context-binding strictness parameter to σ_c to avoid confusion with the branching factor β.

**Shadow IT threshold values (5%, 20%):** The reviewer's concern is fair. These are informed by practitioner experience (e.g., Gartner's shadow IT surveys) but are not rigorously derived. We will either cite the Gartner sources or reframe them as "illustrative ranges" rather than precise thresholds.

**Abstract density:** We will add a one-sentence thesis statement before the formalism: "We argue that governance must transition from a normative discipline to an engineering discipline, and we develop a formal framework — inspired by metamaterial physics — to make this transition quantitative and testable."

**Uncited references in .bib:** We will audit the bibliography and either cite these references at appropriate points (ISO 42001 in Section 3, NIST SP 800-53 in Section 5, DoD Systems Engineering Guidebook in Section 2.3) or remove them. Several were used in earlier drafts and should have been pruned.

**Concrete example for the Freezing Equilibrium:** Excellent suggestion. We will add a worked example in Section 1 illustrating the Freezing Equilibrium in a regulatory approval context: an agency receives 10× more AI-generated environmental impact assessments than it can verify, rational staff stop acting on any of them, and development stalls — not from opposition but from verification paralysis.

**Engagement with multi-agent literature (Chan et al. 2024, Shavit et al. 2023):** We will incorporate these references in Section 4 and discuss how the synthetic principals framework relates to emerging work on AI delegation chains and principal hierarchies.

### Reviewer Summary
*(Internal — not for inclusion in final rebuttal)*
This is an excellent review — rigorous, fair, and constructively oriented. The crux question (does the metamaterial analogy carry its own weight?) is the right one to ask, and the reviewer's engagement with the technical details demonstrates genuine expertise in formal modeling and experimental design. The review's self-declared limitations (metamaterial physics, C2PA/SCITT specifics) are honest and appropriate. Every major criticism is actionable.

---

## Phase 4: Consolidated Revision Plan

### Summary of Proposed Changes

| Priority | Change | Triggered By | Location in Manuscript |
|----------|--------|-------------|----------------------|
| Critical | Situate the constitutive law within the branching-process and cascade-failure literature (Anderson & May, Hethcote, Watts, Buldyrev et al.) and recalibrate the novelty claim | Reviewer, Critical Issue #1 | Section 1 (Introduction), Section 2 (new opening paragraph) |
| Critical | Explicitly distinguish the metamaterial analogy's heuristic vs. generative functions; sharpen the case for bandgap, anisotropy, and hysteresis as predictions beyond generic branching models | Reviewer, Critical Issue #3 | Section 1 (new paragraph), Section 6.1 (revised H1, H2, H4 descriptions) |
| Critical | Reframe R_eff as a phenomenological ansatz; justify the multiplicative structure via sequential-filter argument; add sensitivity analysis for the synergy term | Reviewer, Critical Issue #2 | Section 2.1 (new framing paragraph, revised derivation), Section 7.3 (sensitivity analysis) |
| Critical | Add ethical safeguards subsection for the experimental design (synthetic calibration applications, IRB requirements, informed consent, debriefing protocols) | Reviewer, Critical Issue #4 | New Section 6.3 |
| Important | Expand power analysis with explicit ICC, variance, and design effect assumptions; add sensitivity table for ICC values | Reviewer, Section 2.3 | Section 6.2 (expanded) |
| Important | Add a worked example for the Freezing Equilibrium (regulatory approval context) | Reviewer, Minor Suggestion #5 | Section 1 |
| Important | Cite Chan et al. 2024 and Shavit et al. 2023 on AI delegation chains; discuss relation to synthetic principals framework | Reviewer, Minor Suggestion #6 | Section 4 |
| Important | Map the provenance taxonomy onto NIST AI RMF and ISO 42001 controls; discuss in the body where currently only cited in references | Reviewer, Section 2.2 | Section 3 (new paragraph) |
| Minor | Rename context-binding strictness parameter from β_c to σ_c | Reviewer, Minor Suggestion #1 | Section 3.3 |
| Minor | Cite Gartner shadow IT surveys or reframe 5%/20% thresholds as illustrative ranges | Reviewer, Minor Suggestion #2 | Section 7.2 |
| Minor | Add one-sentence thesis to abstract before the formalism | Reviewer, Minor Suggestion #3 | Abstract |
| Minor | Audit bibliography; cite or remove unused references | Reviewer, Minor Suggestion #4 | Bibliography, Sections 2–5 |
| Minor | Introduce directional decomposition of R_eff (within-unit vs. cross-boundary) to formalize anisotropy | Reviewer, Major Comment #1 (sub-point b) | Section 6.1 (H2 description) |

### Changes NOT Made (with Rationale)

| Suggestion | Rationale for Declining |
|-----------|----------------------|
| Derive R_eff from a micro-model of institutional decision-making (offered as alternative to acknowledging it as an ansatz) | We choose the ansatz route. A first-principles derivation would require assumptions about institutional microstructure (agent utility functions, information flows, delegation topology) that would be more controversial than the phenomenological model itself. The ansatz approach — clearly labeled, with empirical calibration as the validation path — is more appropriate for a framework paper at this stage. A micro-founded derivation is valuable future work. |
| Import formal homogenization theory from metamaterial physics | While intellectually appealing, this would require a level of mathematical formalism (effective medium theory, Bloch wave analysis) that would change the paper's character and audience. The AGI-26 venue values accessibility to an interdisciplinary audience. We believe the sharper articulation of what the analogy *does* contribute (bandgap tail behavior, anisotropy as directional decomposition, hysteresis mechanisms) is a better fit for this venue than formal homogenization. We flag this as promising future work in the Discussion. |

---

*We are grateful for the reviewer's careful engagement and believe the proposed revisions substantially strengthen the manuscript while preserving its core contributions.*
