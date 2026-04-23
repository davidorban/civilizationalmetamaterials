# Civilizational Metamaterials

**Engineering Coordination Under Capability Gradients and Structural Turbulence**

David Orban · [ORCID 0009-0004-4954-1147](https://orcid.org/0009-0004-4954-1147) · Independent Researcher

Status: **Under review at AGI-26** (Springer LNCS/LNAI). Revision 3.

Website: <https://metamaterials.davidorban.com>

---

## What this paper argues

Governance must transition from a normative discipline to an engineering discipline. Artificial General Intelligence increases decision velocity while human verification capacity stays bounded. When verification cost exceeds the expected utility of action, rational agents wait — a stable but catastrophic Nash equilibrium this paper calls the **Freezing Equilibrium**.

Drawing on metamaterials, where emergent macro-properties arise from designed microstructure, the paper proposes a phenomenological constitutive law for institutional coordination:

```
R_eff = β · (1 − ρ) · (1 − τ) · (1 + γ ρ τ)
```

where β is the decision branching factor, ρ is provenance fidelity, τ is the verification rate, and γ captures provenance–verification synergy. A sharp phase transition separates **self-healing** (`R_eff < 1`) from **self-destabilizing** (`R_eff > 1`) regimes, and the sub-critical condition can be engineered by institutional design.

## Four contributions

1. A phenomenological constitutive law for institutional coordination, parameterized by designable features, with a sharp phase transition.
2. A three-class provenance taxonomy — cryptographic, institutional, and *context binding* (the novel third class).
3. Treatment of AI agents as *synthetic principals* requiring distinct governance primitives.
4. Four falsifiable hypotheses with a concrete 12-week stepped-wedge cluster-randomized trial design for government grant review panels.

## Four falsifiable hypotheses

| ID | Prediction | What would falsify it |
|---|---|---|
| H1 | Panels crossing `R_eff = 1` exhibit a sharp regime change | No regime change observed at threshold |
| H2 | Combined ρ and τ interventions are superadditive | Additive or sub-additive effects only |
| H3 | Coordination improvements are directional (anisotropic) | Isotropic response to interventions |
| H4 | Withdrawal of interventions is asymmetrically costly (hysteresis) | Symmetric recovery on withdrawal |

Full details: [`paper/preprint/civilizational-metamaterials-agi26-r3.pdf`](paper/preprint/) · [arXiv link pending]

## Repository map

- [`paper/`](paper/) — TeX source, bibliography, Springer LNCS class files, compiled PDF, arXiv prep
- [`figures/`](figures/) — all ten final figure PDFs, PNG mirrors, layered PNG assets
- [`code/`](code/) — reference implementation of R_eff, branching-process simulator, sensitivity analysis, and one script per figure
- [`experiments/`](experiments/) — proposed trial protocol, statistical analysis plan, power analysis, preregistration template, synthetic data generator, analysis scripts
- [`docs/`](docs/) — one-page website deployed to <https://metamaterials.davidorban.com>
- [`drafts/`](drafts/) — prior revisions (r1, r2) kept for provenance
- [`peer-review/`](peer-review/) — review thread and author rebuttals

## Reproduce

```bash
git clone https://github.com/davidorban/civilizationalmetamaterials.git
cd civilizationalmetamaterials
make paper     # build the PDF
make figures   # regenerate every figure from source
make test      # run the reference-implementation test suite
```

Python 3.11+, a TeXLive distribution (tested with 2024), and `make` are required. Figure scripts pin dependencies in `code/requirements.txt`.

## Cite this work

BibTeX (under-review placeholder):

```bibtex
@misc{orban2026civilizationalmetamaterials,
  author       = {David Orban},
  title        = {Civilizational Metamaterials:
                  Engineering Coordination Under Capability Gradients and Structural Turbulence},
  year         = {2026},
  howpublished = {Manuscript under review at AGI-26},
  note         = {Revision 3},
  url          = {https://github.com/davidorban/civilizationalmetamaterials}
}
```

A machine-readable citation is in [`CITATION.cff`](CITATION.cff). On acceptance, the `status` field flips to `Accepted, AGI-26. To appear in Springer LNCS/LNAI`, a Zenodo DOI is minted, and an arXiv identifier is added.

## Collaboration

The 12-week stepped-wedge cluster-randomized trial described in §Empirical is a *proposed* experimental design, not a registered trial. Institutions interested in piloting the protocol should read [`COLLABORATION.md`](COLLABORATION.md) (coming in Phase 5) and open an issue with the `replication` template.

## Licenses

- Code (everything under `code/` and `experiments/*.py`): [MIT](LICENSE-CODE)
- Paper, figures, protocols, documentation: [CC-BY 4.0](LICENSE-CONTENT)

## Contact

David Orban · <david@davidorban.com> · [davidorban.com](https://davidorban.com)
