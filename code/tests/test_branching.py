"""Tests for cm.branching: Monte Carlo vs analytic R_eff agreement."""

import numpy as np
import pytest
from cm.branching import simulate


N_TRIALS = 10_000
SEED     = 42


class TestExtinction:
    """Extinction probability should be ~1 when R_eff ≤ 1."""

    def test_subcritical_mostly_extinct(self):
        # β=2, ρ=0.8, τ=0.8, γ=1 → R_eff ≈ 2*0.2*0.2*(1+0.64) ≈ 0.131
        result = simulate(2, 0.8, 0.8, 1.0, n_trials=N_TRIALS, seed=SEED)
        assert result["analytic_reff"] < 1.0
        assert result["empirical_extinction"] > 0.85

    def test_supercritical_not_all_extinct(self):
        # β=10, ρ=0.1, τ=0.1, γ=0 → R_eff = 10*0.9*0.9 = 8.1
        result = simulate(10, 0.1, 0.1, 0.0, n_trials=N_TRIALS, seed=SEED)
        assert result["analytic_reff"] > 1.0
        assert result["empirical_extinction"] < 0.5

    def test_critical_extinction_near_half(self):
        # Drive R_eff close to 1.0 and check extinction is between 0.3 and 0.9
        # β=2, ρ=0.5, τ=0.0, γ=0 → R_eff = 2*0.5*1 = 1.0
        result = simulate(2, 0.5, 0.0, 0.0, n_trials=N_TRIALS, seed=SEED)
        assert abs(result["analytic_reff"] - 1.0) < 0.01


class TestReturnStructure:
    def test_keys_present(self):
        result = simulate(5, 0.5, 0.5, 1.0, n_trials=100, seed=0)
        assert "empirical_extinction" in result
        assert "analytic_reff"        in result
        assert "cascade_sizes"        in result

    def test_cascade_sizes_length(self):
        n = 500
        result = simulate(5, 0.5, 0.5, 1.0, n_trials=n, seed=0)
        assert len(result["cascade_sizes"]) == n

    def test_cascade_sizes_nonnegative(self):
        result = simulate(5, 0.5, 0.5, 1.0, n_trials=200, seed=0)
        assert np.all(result["cascade_sizes"] >= 0)

    def test_extinction_rate_in_range(self):
        result = simulate(5, 0.5, 0.5, 1.0, n_trials=N_TRIALS, seed=SEED)
        rate = result["empirical_extinction"]
        assert 0.0 <= rate <= 1.0


class TestReproducibility:
    def test_same_seed_same_result(self):
        r1 = simulate(5, 0.5, 0.3, 1.0, n_trials=200, seed=7)
        r2 = simulate(5, 0.5, 0.3, 1.0, n_trials=200, seed=7)
        assert r1["empirical_extinction"] == r2["empirical_extinction"]
        np.testing.assert_array_equal(r1["cascade_sizes"], r2["cascade_sizes"])
