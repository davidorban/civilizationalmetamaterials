"""Tests for cm.plotting: style application and figure factory."""

import pytest
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from cm.plotting import (
    apply_lncs_style, new_fig,
    DARK_BLUE, SEC_BLUE, AMBER, RED, GREEN, GRAY, LIGHT_GRAY,
    LNCS_FULL_W, LNCS_HALF_W, LNCS_ASPECT,
)


class TestColorConstants:
    def test_all_hex(self):
        for c in (DARK_BLUE, SEC_BLUE, AMBER, RED, GREEN, GRAY, LIGHT_GRAY):
            assert c.startswith("#")
            assert len(c) == 7

    def test_dark_blue_value(self):
        assert DARK_BLUE == "#1B4F72"

    def test_red_value(self):
        assert RED == "#C0392B"


class TestSizing:
    def test_full_width_positive(self):
        assert LNCS_FULL_W > 0

    def test_half_width_less_than_full(self):
        assert LNCS_HALF_W < LNCS_FULL_W

    def test_aspect_in_range(self):
        assert 0.3 < LNCS_ASPECT < 2.0


class TestApplyStyle:
    def test_runs_without_error(self):
        apply_lncs_style()

    def test_sets_font_family(self):
        import matplotlib as mpl
        apply_lncs_style()
        assert mpl.rcParams["font.family"] == ["serif"]


class TestNewFig:
    def test_returns_fig_and_ax(self):
        fig, ax = new_fig()
        assert fig is not None
        assert ax is not None
        plt.close(fig)

    def test_figure_size(self):
        fig, ax = new_fig(width=4.0, aspect=0.75)
        w, h = fig.get_size_inches()
        assert w == pytest.approx(4.0, rel=1e-3)
        assert h == pytest.approx(3.0, rel=1e-3)
        plt.close(fig)
