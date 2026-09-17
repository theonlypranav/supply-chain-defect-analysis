"""Statistical tests for supplier and defect-rate comparisons."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def compare_suppliers(df: pd.DataFrame, supplier_a: int, supplier_b: int):
    """Compare defect rates between two suppliers using an independent t-test."""
    if "defect_rate" not in df.columns:
        raise ValueError("Input dataframe must contain a 'defect_rate' column.")
    a = df[df["supplier_id"] == supplier_a]["defect_rate"]
    b = df[df["supplier_id"] == supplier_b]["defect_rate"]
    if len(a) == 0 or len(b) == 0:
        raise ValueError("One or both suppliers are missing from the dataframe.")
    result = stats.ttest_ind(a, b, equal_var=False)
    return {
        "supplier_a": supplier_a,
        "supplier_b": supplier_b,
        "t_statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "interpretation": "Significant difference" if result.pvalue < 0.05 else "No significant difference",
    }


def anova_all_suppliers(df: pd.DataFrame):
    """Run ANOVA across all suppliers using batch defect rates."""
    if "defect_rate" not in df.columns:
        raise ValueError("Input dataframe must contain a 'defect_rate' column.")
    groups = [group[1]["defect_rate"].dropna().values for group in df.groupby("supplier_id")]
    if len(groups) < 2:
        raise ValueError("ANOVA requires at least two suppliers in the dataframe.")
    if any(len(group) == 0 for group in groups):
        raise ValueError("One or more supplier groups are empty.")
    f_stat, p_value = stats.f_oneway(*groups)
    return {
        "f_statistic": float(f_stat),
        "p_value": float(p_value),
        "interpretation": "Significant supplier differences" if p_value < 0.05 else "No significant supplier differences",
    }


def correlation_analysis(df: pd.DataFrame):
    """Return a numeric correlation matrix for defect-rate-related features."""
    numeric_cols = [
        "quantity_produced",
        "quality_score",
        "lead_time_days",
        "unit_price",
        "defect_rate",
        "supplier_mean_defect_rate",
        "component_defect_rate",
        "batch_age_days",
        "days_since_start",
    ]
    present = [col for col in numeric_cols if col in df.columns]
    selected = df[present].dropna()
    corr = selected.corr()
    return corr
