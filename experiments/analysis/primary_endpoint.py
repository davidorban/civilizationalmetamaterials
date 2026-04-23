"""Primary endpoint analysis — H1: phase-transition crossing.

Runs against the synthetic fixture or real panel data.
Produces a summary table and a text description of the model fit.

Usage
-----
    python experiments/analysis/primary_endpoint.py
    python experiments/analysis/primary_endpoint.py --data experiments/synthetic/fixtures/panels_h1.csv
"""

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

_DEFAULT_DATA = Path(__file__).resolve().parents[1] / "synthetic" / "fixtures" / "panels_h1.csv"


def logistic(x: float | np.ndarray) -> float | np.ndarray:
    return 1 / (1 + np.exp(-x))


def analyse(df: pd.DataFrame) -> dict:
    """Simplified GEE-style analysis: logit regression with period dummies.

    Returns dict with treatment log-OR, SE, 95% CI, and p-value.
    Intended as a lightweight, no-R-required check; for formal analysis use R lme4.
    """
    from statsmodels.formula.api import glm
    from statsmodels.genmod import families

    df = df.copy()
    df["period_f"] = df["period"].astype(str)

    try:
        model = glm(
            "crossed ~ treatment + period_f",
            data=df,
            family=families.Binomial(),
        ).fit(disp=False)

        coef   = model.params["treatment"]
        se     = model.bse["treatment"]
        ci_lo  = coef - 1.96 * se
        ci_hi  = coef + 1.96 * se
        pval   = model.pvalues["treatment"]
        return {
            "log_or":  coef,
            "or":      np.exp(coef),
            "se":      se,
            "ci":      (np.exp(ci_lo), np.exp(ci_hi)),
            "p_value": pval,
            "n_obs":   int(model.nobs),
        }
    except Exception as e:
        return {"error": str(e)}


def summarize(df: pd.DataFrame) -> None:
    n_panels  = df["panel_id"].nunique()
    n_periods = df["period"].nunique()
    cross_ctrl = df.loc[df["treatment"] == 0, "crossed"].mean()
    cross_trt  = df.loc[df["treatment"] == 1, "crossed"].mean()

    print(f"Panels:  {n_panels}")
    print(f"Periods: {n_periods}")
    print(f"Crossing rate — control: {cross_ctrl:.3f}  treatment: {cross_trt:.3f}")

    result = analyse(df)
    if "error" in result:
        print(f"\nModel error (statsmodels not available?): {result['error']}")
        print("Raw OR estimate:", round(cross_trt / (1-cross_trt) / (cross_ctrl / (1-cross_ctrl)), 3) if cross_ctrl < 1 else "∞")
    else:
        print(f"\nTreatment log-OR: {result['log_or']:.3f}  (OR = {result['or']:.3f})")
        print(f"95% CI for OR:    [{result['ci'][0]:.3f}, {result['ci'][1]:.3f}]")
        print(f"p-value:          {result['p_value']:.4f}")
        if result["p_value"] < 0.05:
            print("→ H1 supported (p < 0.05)")
        else:
            print("→ H1 not supported at α = 0.05")


def main() -> None:
    p = argparse.ArgumentParser(description="Primary endpoint analysis (H1).")
    p.add_argument("--data", default=str(_DEFAULT_DATA),
                   help="CSV path (default: synthetic fixture)")
    args = p.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Data file not found: {data_path}")
        print("Run: python experiments/synthetic/generate_synthetic_panels.py")
        sys.exit(1)

    df = pd.read_csv(data_path)
    summarize(df)


if __name__ == "__main__":
    main()
