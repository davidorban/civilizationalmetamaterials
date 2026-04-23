"""Branching-process Monte Carlo simulator.

Each generation, every unverified decision independently spawns offspring
according to a Poisson(β) process. An offspring is "verified" (and thus
absorbed) with probability τ·ρ (both provenance present and checked); the
residual probability (1−τ)(1−ρ) + cross terms collapse to the effective
offspring mean R_eff per the constitutive law.

We simulate extinction probability empirically and compare with the analytic
prediction: P(extinction) = 1 when R_eff ≤ 1, < 1 when R_eff > 1.
"""

from __future__ import annotations

import numpy as np
from .constitutive import r_eff as analytic_reff


def simulate(
    beta: float,
    rho: float,
    tau: float,
    gamma: float,
    *,
    depth: int = 50,
    n_trials: int = 10_000,
    seed: int | None = None,
) -> dict:
    """Run Monte Carlo branching-process trials.

    Each trial starts with one unverified decision and propagates through
    *depth* generations. A trial is "extinct" if the unverified count reaches 0.

    Parameters
    ----------
    beta      : Mean offspring per unverified decision.
    rho       : Provenance fidelity (fraction with verifiable origin).
    tau       : Verification rate (fraction checked per generation).
    gamma     : Synergy coefficient (shifts effective verification probability).
    depth     : Maximum number of generations before capping a trial.
    n_trials  : Number of independent Monte Carlo trials.
    seed      : RNG seed for reproducibility.

    Returns
    -------
    dict with keys:
        empirical_extinction : Fraction of trials that went extinct.
        analytic_reff        : R_eff from the constitutive law.
        cascade_sizes        : 1-D int array of total cascade sizes per trial.
    """
    rng = np.random.default_rng(seed)
    r = analytic_reff(beta, rho, tau, gamma)

    # Effective per-offspring survival probability (probability offspring is *not*
    # absorbed). Derived so that mean survivors = R_eff.
    # We model each offspring as surviving with p_survive = R_eff / beta.
    # Offspring count per decision ~ Poisson(beta); surviving offspring ~ Poisson(R_eff).
    p_survive = min(max(r / beta, 0.0), 1.0)

    sizes = np.zeros(n_trials, dtype=np.int64)
    extinct = 0

    # Cap population to avoid Poisson overflow (Numpy limit ≈ 10^17)
    _MAX_POP = 10_000

    for trial in range(n_trials):
        current = 1  # one seed decision
        total = 0
        for _ in range(depth):
            if current == 0:
                break
            lam = beta * min(current, _MAX_POP)
            offspring = int(rng.poisson(lam))
            survivors = int(rng.binomial(offspring, p_survive)) if offspring > 0 else 0
            total += survivors
            current = survivors
        if current == 0:
            extinct += 1
        sizes[trial] = total

    return {
        "empirical_extinction": extinct / n_trials,
        "analytic_reff": float(r),
        "cascade_sizes": sizes,
    }
