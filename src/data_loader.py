"""Utilities for loading and preparing the supply-chain defect datasets."""

from __future__ import annotations

from typing import Dict

import pandas as pd


def load_data(data_dir: str = "data/") -> Dict[str, pd.DataFrame]:
    """Load all datasets and return them as a dictionary."""
    suppliers = pd.read_csv(f"{data_dir}/suppliers.csv")
    batches = pd.read_csv(f"{data_dir}/component_batches.csv")
    qc_results = pd.read_csv(f"{data_dir}/qc_results.csv")
    defects = pd.read_csv(f"{data_dir}/defects.csv")
    return {
        "suppliers": suppliers,
        "batches": batches,
        "qc_results": qc_results,
        "defects": defects,
    }


def merge_datasets(suppliers: pd.DataFrame, batches: pd.DataFrame, qc_results: pd.DataFrame, defects: pd.DataFrame) -> pd.DataFrame:
    """Merge supplier, batch, QC, and defect information into a single analytical table."""
    batch_with_supplier = batches.merge(suppliers, on="supplier_id", how="left")

    failed_units = qc_results[qc_results["result"] == "Fail"].copy()
    failed_unit_counts = failed_units.groupby("batch_id").size().reset_index(name="failed_units")

    defect_counts = defects.groupby("batch_id").size().reset_index(name="defect_count")
    defect_severity = defects.groupby("batch_id").apply(
        lambda x: x["severity"].value_counts().to_dict()
    ).reset_index(name="severity_breakdown")

    merged = batch_with_supplier.merge(failed_unit_counts, on="batch_id", how="left")
    merged = merged.merge(defect_counts, on="batch_id", how="left")
    merged = merged.merge(defect_severity, on="batch_id", how="left")

    merged["failed_units"] = merged["failed_units"].fillna(0).astype(int)
    merged["defect_count"] = merged["defect_count"].fillna(0).astype(int)
    merged["production_date"] = pd.to_datetime(merged["production_date"])
    merged["received_date"] = pd.to_datetime(merged["received_date"])
    merged["batch_size"] = merged["quantity_produced"]
    merged["quality_pass_rate"] = merged["quantity_passed_qc"] / merged["quantity_produced"]
    return merged


def create_features(merged_df: pd.DataFrame) -> pd.DataFrame:
    """Engineer features used for modeling and statistical analysis."""
    df = merged_df.copy()
    df["defect_count"] = df["defect_count"].fillna(0)
    df["defect_rate"] = df["defect_count"] / df["quantity_produced"]

    q75 = df["defect_rate"].quantile(0.75)
    df["high_defect"] = (df["defect_rate"] > q75).astype(int)

    supplier_stats = (
        df.groupby("supplier_id")
        .agg(
            supplier_mean_defect_rate=("defect_rate", "mean"),
            supplier_std_defect_rate=("defect_rate", "std"),
            supplier_num_batches=("batch_id", "count"),
            supplier_total_units=("quantity_produced", "sum"),
        )
        .reset_index()
    )
    df = df.merge(supplier_stats, on="supplier_id", how="left")

    component_stats = (
        df.groupby("component_name")
        .agg(component_defect_rate=("defect_rate", "mean"))
        .reset_index()
    )
    df = df.merge(component_stats, on="component_name", how="left")

    df["days_since_start"] = (df["production_date"] - df["production_date"].min()).dt.days
    df["month_of_year"] = df["production_date"].dt.month
    df["quarter"] = df["production_date"].dt.quarter
    df["batch_age_days"] = (pd.Timestamp.today().normalize() - df["production_date"]).dt.days

    df["defect_count"] = df["defect_count"].fillna(0)
    df["supplier_mean_defect_rate"] = df["supplier_mean_defect_rate"].fillna(0)
    df["supplier_std_defect_rate"] = df["supplier_std_defect_rate"].fillna(0)
    df["component_defect_rate"] = df["component_defect_rate"].fillna(0)
    return df
