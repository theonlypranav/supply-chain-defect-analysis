"""Generate realistic supply-chain quality datasets for the CS F320 project."""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"


# Constants
SUPPLIER_NAMES = [
    "Samsung", "TSMC", "Corning", "Intel", "Apple", "NVIDIA", "Foxconn", "LG Chem",
    "Sony", "Panasonic", "Murata", "Amphenol", "Onsemi", "STMicroelectronics", "SK Hynix",
    "Hitachi", "Mitsubishi", "Bosch", "Sumitomo", "Delta Electronics", "Jabil", "Flex", "ASE",
    "Qualcomm", "Broadcom", "Texas Instruments", "Infineon", "Kioxia", "Seagate", "Western Digital",
    "Kyocera", "Canon", "Denso", "Renesas", "Nokia", "Ericsson", "Huawei", "Xiaomi", "Lenovo",
    "Dell", "HP", "Acer", "ASUSTeK", "Wistron", "Pegatron", "Liteon", "Molex", "TE Connectivity",
    "Coherent", "APC", "TDK", "Schneider", "Siemens"
]
COUNTRIES = ["USA", "South Korea", "Taiwan", "China", "Japan", "Germany"]
COMPONENT_NAMES = [
    "Processor", "Display", "Battery", "Camera", "Charger", "Connector",
    "Sensor", "Memory", "Power IC", "Speaker", "Motherboard", "PCB", "Fan", "Microcontroller"
]
CHECKPOINTS = {
    1: "Electrical",
    2: "Camera",
    3: "Speaker",
    4: "Battery",
    5: "Screen",
    6: "Connectivity",
    7: "Thermal",
    8: "Final",
}
DEFECT_TYPE_MAP = {
    1: ["Power fluctuation", "Short circuit", "Connector misalignment"],
    2: ["Camera focus failed", "Lens scratch", "Sensor calibration drift"],
    3: ["Speaker distortion", "Audio clipping", "Low volume output"],
    4: ["Battery not detected", "Charging instability", "Cell imbalance"],
    5: ["Screen artifact", "Dead pixel", "Color calibration issue"],
    6: ["Connectivity drop", "Signal interference", "Port instability"],
    7: ["Thermal runaway risk", "Overheating", "Fan failure"],
    8: ["Final assembly defect", "Ingress issue", "Packaging damage"],
}
ROOT_CAUSES = [
    "Material defect",
    "Process variation",
    "Supplier quality issue",
    "Equipment calibration drift",
    "Handling damage",
    "Investigation pending",
    "Environmental exposure",
    "Packaging error",
]


rng = np.random.default_rng(42)


def generate_suppliers() -> pd.DataFrame:
    rows = []
    for supplier_id in range(1, 51):
        name = SUPPLIER_NAMES[supplier_id - 1]
        country = COUNTRIES[(supplier_id - 1) % len(COUNTRIES)]
        lead_time = int(rng.integers(15, 61))
        unit_price = round(float(rng.uniform(2, 500)), 2)
        quality_score = int(rng.integers(60, 98))
        rows.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": name,
                "country": country,
                "lead_time_days": lead_time,
                "unit_price": unit_price,
                "quality_score": quality_score,
            }
        )
    return pd.DataFrame(rows)


def generate_batches(suppliers: pd.DataFrame, n_batches: int = 5000) -> pd.DataFrame:
    today = pd.Timestamp.today().normalize()
    start_date = today - pd.DateOffset(months=24)
    rows = []
    for idx in range(1, n_batches + 1):
        supplier_id = int(rng.integers(1, 51))
        supplier = suppliers.loc[suppliers["supplier_id"] == supplier_id].iloc[0]
        component_name = COMPONENT_NAMES[int(rng.integers(0, len(COMPONENT_NAMES)))]
        quantity_produced = int(rng.integers(100, 10001))
        production_offset_days = int(rng.integers(0, 730))
        production_date = start_date + pd.Timedelta(days=production_offset_days)
        received_date = production_date + pd.Timedelta(days=int(rng.integers(5, 21)))
        quality_multiplier = supplier["quality_score"] / 100
        base_pass_rate = 0.90 + 0.09 * quality_multiplier
        pass_rate = min(0.99, max(0.85, base_pass_rate + rng.normal(0, 0.025)))
        quantity_passed_qc = int(round(quantity_produced * pass_rate))
        rows.append(
            {
                "batch_id": f"BATCH-{production_date.year}-{idx:05d}",
                "supplier_id": supplier_id,
                "component_name": component_name,
                "quantity_produced": quantity_produced,
                "production_date": production_date.strftime("%Y-%m-%d"),
                "received_date": received_date.strftime("%Y-%m-%d"),
                "quantity_passed_qc": quantity_passed_qc,
            }
        )
    return pd.DataFrame(rows)


def generate_qc_results(batches: pd.DataFrame, n_units_target: int = 50000) -> pd.DataFrame:
    rows = []
    total_units = 0
    for _, batch in batches.iterrows():
        supplier = pd.read_csv(DATA_DIR / "suppliers.csv").loc[
            pd.read_csv(DATA_DIR / "suppliers.csv")["supplier_id"] == batch["supplier_id"]
        ].iloc[0]
        quality_score = supplier["quality_score"]
        target_units = max(5, min(18, int(round(10 + (100 - quality_score) / 5 + rng.normal(0, 2)))))
        target_units = int(np.clip(target_units, 5, 18))
        if total_units + target_units > n_units_target:
            target_units = max(1, n_units_target - total_units)
        received_date = pd.Timestamp(batch["received_date"])
        for unit_idx in range(target_units):
            checkpoint_id = int(rng.integers(1, 9))
            checkpoint_name = CHECKPOINTS[checkpoint_id]
            pass_prob = 0.965 - (100 - quality_score) / 1000
            pass_prob = float(np.clip(pass_prob, 0.88, 0.99))
            result = "Pass" if rng.random() < pass_prob else "Fail"
            tested_offset = int(rng.integers(0, 8))
            tested_date = (received_date + pd.Timedelta(days=tested_offset)).strftime("%Y-%m-%d")
            tester_id = f"TEST{int(rng.integers(1, 51)):03d}"
            unit_id = f"UNIT-{total_units + unit_idx + 1:05d}"
            rows.append(
                {
                    "unit_id": unit_id,
                    "batch_id": batch["batch_id"],
                    "checkpoint_id": checkpoint_id,
                    "checkpoint_name": checkpoint_name,
                    "result": result,
                    "tested_date": tested_date,
                    "tester_id": tester_id,
                }
            )
        total_units += target_units
        if total_units >= n_units_target:
            break

    # Ensure exact row count ~50k by padding or trimming if needed
    qc_df = pd.DataFrame(rows)
    if len(qc_df) < n_units_target:
        while len(qc_df) < n_units_target:
            idx = int(rng.integers(0, len(batches)))
            batch = batches.iloc[idx]
            received_date = pd.Timestamp(batch["received_date"])
            checkpoint_id = int(rng.integers(1, 9))
            checkpoint_name = CHECKPOINTS[checkpoint_id]
            quality_score = pd.read_csv(DATA_DIR / "suppliers.csv").loc[
                pd.read_csv(DATA_DIR / "suppliers.csv")["supplier_id"] == batch["supplier_id"]
            ].iloc[0]["quality_score"]
            pass_prob = 0.965 - (100 - quality_score) / 1000
            pass_prob = float(np.clip(pass_prob, 0.88, 0.99))
            result = "Pass" if rng.random() < pass_prob else "Fail"
            tested_offset = int(rng.integers(0, 8))
            tested_date = (received_date + pd.Timedelta(days=tested_offset)).strftime("%Y-%m-%d")
            tester_id = f"TEST{int(rng.integers(1, 51)):03d}"
            qc_df.loc[len(qc_df)] = {
                "unit_id": f"UNIT-{len(qc_df) + 1:05d}",
                "batch_id": batch["batch_id"],
                "checkpoint_id": checkpoint_id,
                "checkpoint_name": checkpoint_name,
                "result": result,
                "tested_date": tested_date,
                "tester_id": tester_id,
            }
    qc_df = qc_df.iloc[:n_units_target].reset_index(drop=True)
    qc_df["unit_id"] = [f"UNIT-{idx + 1:05d}" for idx in range(len(qc_df))]
    return qc_df


def generate_defects(qc_results: pd.DataFrame) -> pd.DataFrame:
    failed_rows = qc_results[qc_results["result"] == "Fail"].copy()
    if len(failed_rows) < 2000:
        raise ValueError("Not enough failed units to generate the defect dataset.")
    failed_rows = failed_rows.sample(n=2000, random_state=42).reset_index(drop=True)
    rows = []
    for idx, row in failed_rows.iterrows():
        checkpoint_id = int(row["checkpoint_id"])
        defect_type = rng.choice(DEFECT_TYPE_MAP.get(checkpoint_id, ["General defect"]))
        severity = rng.choice(["Critical", "High", "Medium", "Low"], p=[0.1, 0.25, 0.35, 0.30])
        root_cause = rng.choice(ROOT_CAUSES)
        reported_date = pd.Timestamp(row["tested_date"]) + pd.Timedelta(days=int(rng.integers(0, 4)))
        rows.append(
            {
                "defect_id": f"DEF-{idx + 1:05d}",
                "unit_id": row["unit_id"],
                "batch_id": row["batch_id"],
                "checkpoint_id": checkpoint_id,
                "defect_type": defect_type,
                "severity": severity,
                "root_cause": root_cause,
                "reported_date": reported_date.strftime("%Y-%m-%d"),
            }
        )
    return pd.DataFrame(rows)


def build_analytical_dataset() -> pd.DataFrame:
    """Build the merged analytical dataset used by notebooks and models."""
    suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
    batches = pd.read_csv(DATA_DIR / "component_batches.csv")
    qc_results = pd.read_csv(DATA_DIR / "qc_results.csv")
    defects = pd.read_csv(DATA_DIR / "defects.csv")

    df = batches.merge(suppliers, on="supplier_id", how="left")
    failed_units = qc_results[qc_results["result"] == "Fail"].groupby("batch_id").size().reset_index(name="failed_units")
    defect_counts = defects.groupby("batch_id").size().reset_index(name="defect_count")
    df = df.merge(failed_units, on="batch_id", how="left")
    df = df.merge(defect_counts, on="batch_id", how="left")

    df["failed_units"] = df["failed_units"].fillna(0).astype(int)
    df["defect_count"] = df["defect_count"].fillna(0).astype(int)
    df["defect_rate"] = df["defect_count"] / df["quantity_produced"]
    df["binary_target"] = (df["defect_rate"] > df["defect_rate"].quantile(0.75)).astype(int)
    df["production_date"] = pd.to_datetime(df["production_date"])
    df["received_date"] = pd.to_datetime(df["received_date"])
    df["days_since_start"] = (df["production_date"] - df["production_date"].min()).dt.days
    df["month_of_year"] = df["production_date"].dt.month
    df["quarter"] = df["production_date"].dt.quarter
    df["batch_age_days"] = (pd.Timestamp.today().normalize() - df["production_date"]).dt.days

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

    component_rate = (
        df.groupby("component_name")
        .agg(component_defect_rate=("defect_rate", "mean"))
        .reset_index()
    )
    df = df.merge(component_rate, on="component_name", how="left")

    df["supplier_mean_defect_rate"] = df["supplier_mean_defect_rate"].fillna(0)
    df["supplier_std_defect_rate"] = df["supplier_std_defect_rate"].fillna(0)
    df["component_defect_rate"] = df["component_defect_rate"].fillna(0)
    return df


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    suppliers = generate_suppliers()
    batches = generate_batches(suppliers, n_batches=5000)
    suppliers.to_csv(DATA_DIR / "suppliers.csv", index=False)
    batches.to_csv(DATA_DIR / "component_batches.csv", index=False)

    qc_results = generate_qc_results(batches)
    qc_results.to_csv(DATA_DIR / "qc_results.csv", index=False)

    defects = generate_defects(qc_results)
    defects.to_csv(DATA_DIR / "defects.csv", index=False)

    analytical_df = build_analytical_dataset()
    analytical_df.to_csv(DATA_DIR / "analytical_dataset.csv", index=False)

    print(f"Generated supplier data: {len(suppliers)} rows")
    print(f"Generated batch data: {len(batches)} rows")
    print(f"Generated QC results: {len(qc_results)} rows")
    print(f"Generated defects: {len(defects)} rows")
    print(f"Generated analytical dataset: {len(analytical_df)} rows")


if __name__ == "__main__":
    main()
