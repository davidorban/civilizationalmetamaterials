# Civilizational Metamaterials — Progress Tracker

## Paper status

| Milestone | Status | Date | Notes |
|---|---|---|---|
| r0 initial submission | ✅ Done | 2026 | AGI-26 EasyChair |
| r1 revision | ✅ Done | 2026 | Addressed C1–C4, I1–I4 |
| r2 revision | ✅ Done | 2026 | Camera-ready improvements; reviewer score 1→2 |
| r3 revision | ✅ Done | 2026-04-15 | Corrected sensitivity analysis; locked |
| AGI-26 decision | ✅ Accepted | 2026 | Single-blind review |
| r4 camera-ready | ✅ Submitted | 2026-05-29 | Final camera-ready for Springer proceedings (`r4.tex`/`.pdf`, `r4-source.zip`); LNCS proceedings form filed |
| Springer proceedings | ⏳ Pending | — | Fill journal ref + DOI when issued |

---

## Repository — github.com/davidorban/civilizationalmetamaterials

| Phase | Status | Commit | Notes |
|---|---|---|---|
| Phase 0 — skeleton | ✅ Done | `4a10c2d` | Licenses, CITATION.cff, empty tree |
| Phase 1 — paper + figures | ✅ Done | `61147ed` | r3 TeX, 10 figure PDFs, peer review, CI |
| Phase 2 — website | ✅ Done | `dd8da1b` | MathJax, R_eff widget, hero PNG |
| Phase 3 — reference impl | ✅ Done | `0e4f2cf` | cm/ package, 52 tests, 97% coverage |
| Phase 4 — figure scripts | ✅ Done | `5b73106` | All 10 figure scripts |
| Phase 5 — experiments | ✅ Done | `adcf392` | Protocol, SAP, power, instruments, analysis |
| Phase 6 — v1.0.0 tag | ✅ Done | `dccff6d` | Annotated tag created |

---

## Publication artefacts

| Artefact | Status | Value / URL |
|---|---|---|
| GitHub repo | ✅ Live | https://github.com/davidorban/civilizationalmetamaterials |
| GitHub Release | ✅ Live | v1.0.0 |
| Zenodo DOI | ✅ Minted | 10.5281/zenodo.19710482 |
| Website | ✅ Live | https://metamaterials.davidorban.com |
| Preprint PDF (with cover) | ✅ Live | /civilizational-metamaterials-preprint.pdf |
| Submission PDF (no cover) | ✅ Live | /civilizational-metamaterials-agi26-r3.pdf |
| arXiv submission | ⏳ On hold | submit/7513752 — announced within 24h of 2026-04-23 |
| arXiv permanent ID | ⏳ Pending | update when announced |
| arXiv URL | ⏳ Pending | update when announced |

---

## Remaining to-do

### When arXiv ID is assigned
- [ ] Update `docs/index.html` — `#arxiv-link` button href + remove "(pending)" label
- [ ] Update `CITATION.cff` — add `arXiv:XXXX.XXXXX` to `identifiers:` block
- [ ] Update `README.md` — BibTeX `note` field with arXiv ID
- [ ] Optionally add arXiv ID as related identifier on the Zenodo record

### When AGI-26 decision arrives (acceptance)
- [ ] Flip `CITATION.cff` `status:` → `"Accepted, AGI-26. To appear in Springer LNCS/LNAI."`
- [ ] Uncomment and fill `preferred-citation:` block in `CITATION.cff`
- [ ] Submit arXiv v2 with "Accepted at AGI-26" note
- [ ] Add Springer proceedings DOI to `CITATION.cff` and `docs/index.html`
- [ ] Cut `v1.1.0` tag → triggers new Zenodo version record

### Ongoing
- [ ] Fix SSH: `ssh-add ~/.ssh/id_ed25519` + verify with `ssh -T git@github.com`
- [ ] Check if arXiv 2507.06398 ("Jolting Technologies") is cited in r3 bibliography
- [ ] Notebooks: write `code/notebooks/01_phase_diagram_walkthrough.ipynb`
- [ ] Instruments: create `experiments/instruments/provenance-checklist.pdf`

---

## Key identifiers (quick reference)

```
GitHub:  https://github.com/davidorban/civilizationalmetamaterials
Website: https://metamaterials.davidorban.com
DOI:     10.5281/zenodo.19710482
Zenodo:  https://zenodo.org/records/19710482
arXiv:   submit/7513752 (permanent ID pending)
ORCID:   0009-0004-4954-1147
```

---

## Related papers by the author on arXiv

| ID | Title |
|---|---|
| 2507.06398 | Jolting Technologies: Superexponential Acceleration in AI Capabilities and Implications for AGI |
