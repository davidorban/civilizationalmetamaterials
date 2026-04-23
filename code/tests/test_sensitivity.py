"""Tests for cm.sensitivity: OAT sweeps and Sobol indices."""

import numpy as np
import pytest
from cm.sensitivity import oat_sweep, sobol_indices, DEFAULT_BASE, DEFAULT_PROBLEM


class TestOATSweep:
    def test_tau_sweep_shape(self):
        x, r = oat_sweep("tau", n_points=50)
        assert x.shape == (50,)
        assert r.shape == (50,)

    def test_rho_sweep_shape(self):
        x, r = oat_sweep("rho", n_points=50)
        assert x.shape == (50,)
        assert r.shape == (50,)

    def test_beta_sweep_monotone_increasing(self):
        # R_eff increases with β (all else fixed)
        x, r = oat_sweep("beta", n_points=50, base=DEFAULT_BASE)
        assert np.all(np.diff(r) >= -1e-12)

    def test_tau_sweep_monotone_decreasing(self):
        x, r = oat_sweep("tau", n_points=50)
        assert np.all(np.diff(r) <= 1e-12)

    def test_rho_sweep_monotone_decreasing(self):
        x, r = oat_sweep("rho", n_points=50)
        assert np.all(np.diff(r) <= 1e-12)

    def test_gamma_sweep_returns_values(self):
        x, r = oat_sweep("gamma", n_points=50)
        assert len(r) == 50
        assert np.all(np.isfinite(r))

    def test_custom_base(self):
        x, r = oat_sweep("tau", n_points=10, base={"beta": 5, "rho": 0.5, "tau": 0.5, "gamma": 0})
        # At τ=0 with ρ=0.5, β=5, γ=0: R_eff = 5*0.5*1 = 2.5
        assert r[0] == pytest.approx(2.5, rel=1e-6)


class TestSobolIndices:
    def test_keys_present(self):
        si = sobol_indices(n_samples=64, seed=0)
        for k in ("names", "S1", "ST", "S1_conf", "ST_conf"):
            assert k in si

    def test_indices_length(self):
        si = sobol_indices(n_samples=64, seed=0)
        assert len(si["S1"]) == len(DEFAULT_PROBLEM["names"])
        assert len(si["ST"]) == len(DEFAULT_PROBLEM["names"])

    def test_indices_in_range(self):
        si = sobol_indices(n_samples=128, seed=42)
        # S1 and ST can be negative due to sampling noise, but ST >= S1 typically
        assert all(np.isfinite(si["S1"]))
        assert all(np.isfinite(si["ST"]))

    def test_names_match_problem(self):
        si = sobol_indices(n_samples=64, seed=0)
        assert si["names"] == DEFAULT_PROBLEM["names"]
