"""Tests for cm.anisotropy: coordination tensor and anisotropy index."""

import numpy as np
import pytest
from cm.anisotropy import coordination_tensor, anisotropy_index, sweep_cross_boundary
from cm.constitutive import r_eff


class TestCoordinationTensor:
    def test_isotropic_case(self):
        # If rho_w == rho_c and tau_w == tau_c, tensor is symmetric
        T = coordination_tensor(10, 0.5, 0.5, 0.5, 0.5, 1.0)
        assert T[0, 0] == pytest.approx(T[0, 1])
        assert T[1, 0] == pytest.approx(T[1, 1])

    def test_diagonal_matches_constitutive(self):
        beta, gamma = 10.0, 1.0
        rho_w, tau_w = 0.7, 0.6
        T = coordination_tensor(beta, rho_w, tau_w, 0.1, 0.1, gamma)
        expected = r_eff(beta, rho_w, tau_w, gamma)
        assert T[0, 0] == pytest.approx(expected)

    def test_offdiag_matches_constitutive(self):
        beta, gamma = 5.0, 0.5
        rho_c, tau_c = 0.2, 0.3
        T = coordination_tensor(beta, 0.8, 0.8, rho_c, tau_c, gamma)
        expected_cross = r_eff(beta, rho_c, tau_c, gamma)
        assert T[0, 1] == pytest.approx(expected_cross)

    def test_shape(self):
        T = coordination_tensor(10, 0.5, 0.5, 0.3, 0.3, 1.0)
        assert T.shape == (2, 2)


class TestAnisotropyIndex:
    def test_isotropic_zero(self):
        T = coordination_tensor(10, 0.5, 0.5, 0.5, 0.5, 1.0)
        assert anisotropy_index(T) == pytest.approx(0.0, abs=1e-12)

    def test_range_zero_to_one(self):
        T = coordination_tensor(10, 0.9, 0.9, 0.0, 0.0, 0.0)
        ai = anisotropy_index(T)
        assert 0.0 <= ai <= 1.0

    def test_all_zero_tensor(self):
        T = np.zeros((2, 2))
        assert anisotropy_index(T) == pytest.approx(0.0)


class TestSweepCrossBoundary:
    def test_output_shapes(self):
        rg, tg, ai = sweep_cross_boundary(10, 1.0, n_points=20)
        assert rg.shape == (20, 20)
        assert tg.shape == (20, 20)
        assert ai.shape == (20, 20)

    def test_ai_bounded(self):
        _, _, ai = sweep_cross_boundary(10, 1.0, n_points=15)
        assert np.all(ai >= 0.0)
        assert np.all(ai <= 1.0)
