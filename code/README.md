# Code — Reference Implementation

This directory contains the reference implementation of the R_eff constitutive law,
the branching-process simulator, and all figure scripts. Every figure in the paper
can be reproduced from source.

## Structure

```
code/
├── cm/                       # Importable Python package
│   ├── constitutive.py       # r_eff(), tau_star(), phase_boundary()
│   ├── branching.py          # Monte Carlo branching-process simulator
│   ├── sensitivity.py        # OAT sweeps + Sobol indices (SALib)
│   ├── anisotropy.py         # Directional coordination tensor
│   └── plotting.py           # Shared style: colors, LNCS sizing, fonts
├── figures/                  # One script per figure
│   ├── fig02_phase_transition.py
│   └── fig05_sensitivity_analysis.py
├── tests/                    # pytest suite (≥ 90% coverage target)
│   ├── test_constitutive.py
│   ├── test_branching.py
│   ├── test_sensitivity.py
│   ├── test_anisotropy.py
│   └── test_plotting.py
├── notebooks/                # Exploratory Jupyter notebooks
├── pyproject.toml
└── requirements.txt
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest --cov=cm

# Reproduce figures
python figures/fig02_phase_transition.py --out ../figures/fig02-phase-transition.pdf
python figures/fig05_sensitivity_analysis.py --out ../figures/fig05-sensitivity-analysis.pdf
```

All figure scripts accept `--out <path>` to write a PDF and print the path.
Without `--out` they open an interactive matplotlib window.

## Constitutive law

```python
from cm import r_eff, tau_star, phase_boundary
import numpy as np

# Scalar: R_eff at β=10, ρ=0.5, τ=0.5, γ=1
print(r_eff(10, 0.5, 0.5, 1.0))   # → 3.125

# Critical verification rate where R_eff = 1
print(tau_star(10, 0.5, 1.0))

# Phase boundary over a ρ grid
rho = np.linspace(0, 1, 100)
tau_crit = phase_boundary(10, 1.0, rho)
```

## Reproducing all figures

Once Phase 4 figure scripts are committed, `make figures` (from the repo root)
rebuilds all ten figure PDFs.
