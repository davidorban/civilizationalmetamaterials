"""Secondary endpoint analysis — H2 synergy, H3 anisotropy, H4 hysteresis.

Runs against the synthetic fixture or real panel data.

Usage
-----
    python experiments/analysis/secondary_h2_h4.py
    python experiments/analysis/secondary_h2_h4.py --data experiments/synthetic/fixtures/panels_h234.csv
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

_DEFAULT_DATA = Path(__file__).resolve().parents[1] / "synthetic" / "fixtures" / "panels_h234.csv"


def analyse_h2(df: pd.DataFrame) -> None:
    """H2: synergy — joint ρ×τ reduction exceeds additive prediction."""
    print("── H2: Synergy ─────────────────────────────────────────────────")
    trt = df[df["treatment"] == 1].copy()
    ctrl = df[df["treatment"] == 0].copy()

    # Compare within-panel R_eff reduction between treatment and control
    r_within_trt  = trt["r_eff_within"].mean()
    r_within_ctrl = ctrl["r_eff_within"].mean()
    r_cross_trt   = trt["r_eff_cross"].mean()
    r_cross_ctrl  = ctrl["r_eff_cross"].mean()

    print(f"  R_eff_within:  control={r_within_ctrl:.3f}  treatment={r_within_trt:.3f}")
    print(f"  R_eff_cross:   control={r_cross_ctrl:.3f}  treatment={r_cross_trt:.3f}")

    # Simple t-test on within-panel R_eff between treated and control periods
    t, p = stats.ttest_ind(trt["r_eff_within"], ctrl["r_eff_within"])
    print(f"  t-test R_eff_within (trt vs ctrl): t={t:.3f}, p={p:.4f}")
    if p < 0.05:
        print("  → H2 supported: treatment significantly reduces within-panel R_eff")
    else:
        print("  → H2 not supported at α = 0.05")


def analyse_h3(df: pd.DataFrame) -> None:
    """H3: anisotropy — within-panel improvement ≠ cross-panel improvement."""
    print("\n── H3: Anisotropy ───────────────────────────────────────────────")
    trt = df[df["treatment"] == 1].copy()

    diff = trt["r_eff_cross"] - trt["r_eff_within"]
    mean_diff = diff.mean()
    se_diff   = diff.std() / np.sqrt(len(diff))
    t_stat    = mean_diff / se_diff if se_diff > 0 else np.nan
    p_val     = 2 * stats.t.sf(abs(t_stat), df=len(diff) - 1) if not np.isnan(t_stat) else np.nan

    print(f"  Mean(R_cross − R_within) in treated periods: {mean_diff:.3f}")
    print(f"  SE: {se_diff:.3f}   t={t_stat:.3f}   p={p_val:.4f}")
    if not np.isnan(p_val) and p_val < 0.05 and mean_diff > 0:
        print("  → H3 supported: cross-boundary R_eff > within-panel R_eff")
    else:
        print("  → H3 not supported at α = 0.05")


def analyse_h4(df: pd.DataFrame) -> None:
    """H4: hysteresis — recovery longer than improvement (exploratory).

    Requires panels with both a treatment and a post-treatment period.
    Not testable in the standard stepped-wedge without an extension; this is
    flagged as exploratory and NA when not feasible.
    """
    print("\n── H4: Hysteresis (exploratory) ─────────────────────────────────")
    print("  H4 requires a post-withdrawal observation period.")
    print("  Not present in standard stepped-wedge design without extension.")
    print("  → H4: exploratory, cannot be assessed in this dataset.")


def main() -> None:
    p = argparse.ArgumentParser(description="Secondary endpoint analyses (H2–H4).")
    p.add_argument("--data", default=str(_DEFAULT_DATA))
    args = p.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        print("Run: python experiments/synthetic/generate_synthetic_panels.py")
        sys.exit(1)

    df = pd.read_csv(data_path)
    analyse_h2(df)
    analyse_h3(df)
    analyse_h4(df)


if __name__ == "__main__":
    main()
