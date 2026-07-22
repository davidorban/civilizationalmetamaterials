# Civilizational Metamaterials

**Engineering Coordination Under Capability Gradients and Structural Turbulence**

David Orban · [ORCID 0009-0004-4954-1147](https://orcid.org/0009-0004-4954-1147) · Independent Researcher

Status: **Published in the AGI-26 proceedings** ([Springer, LNCS vol 16855, pp. 118–136](https://doi.org/10.1007/978-3-032-33195-3_10)). Preprint: [arXiv:2606.00235](https://arxiv.org/abs/2606.00235).

Website: <https://metamaterials.davidorban.com>

---

## What this paper argues

Governance must transition from a normative discipline to an engineering discipline. Artificial General Intelligence increases decision velocity while human verification capacity stays bounded. When verification cost exceeds the expected utility of action, rational agents wait — a stable but catastrophic Nash equilibrium this paper calls the **Freezing Equilibrium**.

Drawing on metamaterials, where emergent macro-properties arise from designed microstructure, the paper proposes a phenomenological constitutive law for institutional coordination:

```
R_eff = β · (1 − ρ) · (1 − τ) · (1 − γ ρ τ)
```

where β is the decision branching factor, ρ is provenance fidelity, τ is the verification rate, and γ ∈ [0, 1] is the correlated-detection coefficient (provenance and verification target overlapping failure modes). A sharp phase transition separates **self-healing** (`R_eff < 1`) from **self-destabilizing** (`R_eff > 1`) regimes, and the sub-critical condition can be engineered by institutional design.

## Four contributions

1. A phenomenological constitutive law for institutional coordination, parameterized by designable features, with a sharp phase transition.
2. A three-class provenance taxonomy — cryptographic, institutional, and *context binding* (the novel third class).
3. Treatment of AI agents as *synthetic principals* requiring distinct governance primitives.
4. Four falsifiable hypotheses with a concrete 12-week stepped-wedge cluster-randomized trial design for government grant review panels.

## Four falsifiable hypotheses

| ID | Prediction | What would falsify it |
|---|---|---|
| H1 | Panels crossing `R_eff = 1` exhibit a sharp regime change | No regime change observed at threshold |
| H2 | Coordination response is anisotropic (within-unit vs. cross-boundary differ) | Isotropic response; no directional difference |
| H3 | Combined ρ and τ interventions cross `R_eff = 1` where neither single one does (threshold-crossing) | A single intervention also crosses, or high–high fails to |
| H4 | Withdrawal of interventions is asymmetrically costly (hysteresis) | Symmetric recovery on withdrawal |

Full details: [arXiv:2606.00235](https://arxiv.org/abs/2606.00235) · [`paper/civilizational-metamaterials-agi26-r4.pdf`](paper/)

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

BibTeX:

```bibtex
@inproceedings{orban2026civilizationalmetamaterials,
  author        = {David Orban},
  title         = {Civilizational Metamaterials:
                   Engineering Coordination Under Capability Gradients and Structural Turbulence},
  booktitle     = {Artificial General Intelligence. AGI 2026},
  series        = {Lecture Notes in Computer Science},
  volume        = {16855},
  pages         = {118--136},
  publisher     = {Springer, Cham},
  year          = {2026},
  doi           = {10.1007/978-3-032-33195-3_10},
  isbn          = {978-3-032-33195-3},
  eprint        = {2606.00235},
  archivePrefix = {arXiv},
  primaryClass  = {physics.soc-ph},
  url           = {https://doi.org/10.1007/978-3-032-33195-3_10}
}
```

A machine-readable citation is in [`CITATION.cff`](CITATION.cff). Springer DOI: [10.1007/978-3-032-33195-3_10](https://doi.org/10.1007/978-3-032-33195-3_10). arXiv: [2606.00235](https://arxiv.org/abs/2606.00235). Zenodo archival DOI: [10.5281/zenodo.19710482](https://doi.org/10.5281/zenodo.19710482).

## Collaboration

The 12-week stepped-wedge cluster-randomized trial described in §Empirical is a *proposed* experimental design, not a registered trial. Institutions interested in piloting the protocol should read [`COLLABORATION.md`](COLLABORATION.md) and open an issue with the `collaboration` label.

## Licenses

- Code (everything under `code/` and `experiments/*.py`): [MIT](LICENSE-CODE)
- Paper, figures, protocols, documentation: [CC-BY 4.0](LICENSE-CONTENT)

## Contact

David Orban · <david@davidorban.com> · [davidorban.com](https://davidorban.com)
