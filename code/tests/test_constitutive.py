"""Tests for cm.constitutive: known values, monotonicity, critical τ*."""

import numpy as np
import pytest
from cm.constitutive import r_eff, tau_star, phase_boundary


# ── Known closed-form corner values ──────────────────────────────────────

class TestReffCorners:
    def test_full_provenance_and_verification(self):
        # ρ=1, τ=1 → R_eff = β*(0)*(0)*(1+γ) = 0
        assert r_eff(10, 1.0, 1.0, 1.0) == pytest.approx(0.0)

    def test_no_provenance_no_verification(self):
        # ρ=0, τ=0 → R_eff = β*(1)*(1)*(1+0) = β
        assert r_eff(10, 0.0, 0.0, 1.0) == pytest.approx(10.0)

    def test_full_provenance_no_verification(self):
        # ρ=1, τ=0 → R_eff = β*0*1*(1+γ) = 0
        assert r_eff(10, 1.0, 0.0, 2.0) == pytest.approx(0.0)

    def test_no_provenance_full_verification(self):
        # ρ=0, τ=1 → R_eff = β*1*0*(1+0) = 0
        assert r_eff(10, 0.0, 1.0, 2.0) == pytest.approx(0.0)

    def test_no_synergy(self):
        # γ=0 → R_eff = β*(1-ρ)*(1-τ)
        assert r_eff(5, 0.4, 0.6, 0.0) == pytest.approx(5 * 0.6 * 0.4)

    def test_phase_transition_known(self):
        # β=10, ρ=0.5, τ=0.5, γ=1 → R_eff = 10*0.5*0.5*(1+0.25) = 3.125
        assert r_eff(10, 0.5, 0.5, 1.0) == pytest.approx(3.125)

    def test_vectorized_over_rho(self):
        rho = np.array([0.0, 0.5, 1.0])
        out = r_eff(10, rho, 0.0, 0.0)
        np.testing.assert_allclose(out, [10.0, 5.0, 0.0])


# ── Monotonicity ──────────────────────────────────────────────────────────

class TestMonotonicity:
    """R_eff must be non-increasing in both ρ and τ (for fixed γ ≥ 0)."""

    def test_nonincreasing_in_rho(self):
        rho_vals = np.linspace(0, 1, 50)
        r = r_eff(10, rho_vals, 0.3, 0.5)
        assert np.all(np.diff(r) <= 1e-12)

    def test_nonincreasing_in_tau(self):
        tau_vals = np.linspace(0, 1, 50)
        r = r_eff(10, 0.3, tau_vals, 0.5)
        assert np.all(np.diff(r) <= 1e-12)

    def test_nonnegative(self):
        rho = np.random.default_rng(0).uniform(0, 1, 200)
        tau = np.random.default_rng(1).uniform(0, 1, 200)
        assert np.all(r_eff(10, rho, tau, 1.0) >= 0)


# ── Critical τ* ───────────────────────────────────────────────────────────

class TestTauStar:
    def test_tau_star_known(self):
        # γ=0: R_eff = β(1-ρ)(1-τ) = 1 → τ* = 1 - 1/(β(1-ρ))
        # β=10, ρ=0: τ* = 1 - 1/10 = 0.9
        ts = tau_star(10, 0.0, 0.0)
        assert ts == pytest.approx(0.9, rel=1e-6)

    def test_tau_star_validates_reff(self):
        beta, rho, gamma = 10.0, 0.6, 1.0
        ts = tau_star(beta, rho, gamma)
        assert ts is not None
        assert r_eff(beta, rho, ts, gamma) == pytest.approx(1.0, abs=1e-8)

    def test_tau_star_none_when_impossible(self):
        # β=1, ρ=0, γ=0 → R_eff = 1*(1-τ), so τ*=0; but for β<1 it's always ≤1
        # Make R_eff(τ=1) ≥ 1: β=1, ρ=0, γ=2 → R_eff=1*(1-τ)*(1+0)=1-τ → τ*=0
        assert tau_star(1.0, 0.0, 0.0) == pytest.approx(0.0)

    def test_phase_boundary_shape(self):
        grid = np.linspace(0, 1, 30)
        tb = phase_boundary(10, 1.0, grid)
        assert tb.shape == (30,)
        # At ρ=1: R_eff=0 always, so τ*=0
        assert tb[-1] == pytest.approx(0.0, abs=1e-8)
