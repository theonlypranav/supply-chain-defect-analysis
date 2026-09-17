"""Visualization functions for defect analysis and executive reporting."""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_defect_by_supplier(df: pd.DataFrame):
    """Plot supplier defect rate ranking."""
    supplier_summary = (
        df.groupby("supplier_name")
        .agg(defect_rate=("defect_rate", "mean"), batches=("batch_id", "count"))
        .reset_index()
        .sort_values("defect_rate", ascending=False)
    )
    plt.figure(figsize=(10, 6))
    sns.barplot(data=supplier_summary.head(10), x="defect_rate", y="supplier_name", palette="viridis")
    plt.title("Top 10 Suppliers by Defect Rate")
    plt.xlabel("Defect Rate")
    plt.ylabel("Supplier")
    plt.tight_layout()
    return plt.gcf()


def plot_defect_trend(df: pd.DataFrame):
    """Plot monthly defect-rate trend over time."""
    df = df.copy()
    df["month"] = df["production_date"].dt.to_period("M").astype(str)
    trend = df.groupby("month")["defect_rate"].mean().reset_index()
    plt.figure(figsize=(12, 5))
    sns.lineplot(data=trend, x="month", y="defect_rate", marker="o")
    plt.title("Defect Rate Trend Over Time")
    plt.xlabel("Month")
    plt.ylabel("Mean Defect Rate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()


def create_dashboard(df: pd.DataFrame, models: dict):
    """Create a simple executive summary dashboard."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    supplier_summary = df.groupby("supplier_name")["defect_rate"].mean().sort_values(ascending=False).head(8)
    supplier_summary.plot(kind="bar", ax=axes[0, 0], color="salmon")
    axes[0, 0].set_title("Average Defect Rate by Supplier")
    axes[0, 0].set_ylabel("Defect Rate")
    axes[0, 0].tick_params(axis="x", rotation=45)

    component_summary = df.groupby("component_name")["defect_rate"].mean().sort_values(ascending=False)
    component_summary.plot(kind="bar", ax=axes[0, 1], color="steelblue")
    axes[0, 1].set_title("Defect Rate by Component")
    axes[0, 1].set_ylabel("Defect Rate")
    axes[0, 1].tick_params(axis="x", rotation=45)

    if "Random Forest" in models:
        model_values = [models["Random Forest"]["accuracy"], models["Logistic Regression"]["accuracy"]]
        model_names = ["Random Forest", "Logistic Regression"]
        axes[1, 0].bar(model_names, model_values, color=["#4C72B0", "#55A868"])
        axes[1, 0].set_title("Classification Accuracy Comparison")
        axes[1, 0].set_ylabel("Accuracy")

    if "Random Forest Regressor" in models:
        reg_metrics = [models["Random Forest Regressor"]["r2"], models["Linear Regression"]["r2"]]
        reg_labels = ["RF Regressor", "Linear Regression"]
        axes[1, 1].bar(reg_labels, reg_metrics, color=["#C44E52", "#8172B3"])
        axes[1, 1].set_title("Regression R^2 Comparison")
        axes[1, 1].set_ylabel("R^2")

    plt.tight_layout()
    return fig
