# Supply Chain Component Defect Analysis

Supply Chain Component Defect Analysis: Statistical Analysis and Predictive Modeling is a CS F320 data science project focused on identifying supplier risk, testing quality differences statistically, and predicting high-risk production batches before defects escalate.

## Problem Statement

Manufacturing teams often receive component batches from many suppliers with differing lead times, quality scores, and defect behavior. This project analyzes supplier quality patterns, estimates batch-level defect risk, and builds predictive models to support quality assurance decisions.

## Dataset Overview

The project uses synthetic but realistic supply chain data representing:

- 50 suppliers
- 5,000 component batches
- 50,000 unit-level QC checks
- 2,000 defect records

The datasets include supplier metadata, batch production and receipt timing, QC results, and defect classifications.

## Repository Structure

```text
supply-chain-defect-analysis/
├── README.md
├── REPORT.md
├── generate_data.py
├── data/
│   ├── suppliers.csv
│   ├── component_batches.csv
│   ├── qc_results.csv
│   └── defects.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_statistical_analysis.ipynb
│   ├── 04_predictive_modeling.ipynb
│   └── 05_visualization_report.ipynb
├── src/
│   ├── data_loader.py
│   ├── statistical_tests.py
│   ├── model_training.py
│   └── visualization.py
├── results/
│   └── (generated charts and output artifacts)
└── .gitignore
```

## Key Findings

- Supplier quality performance differs significantly across vendors.
- Defect rates are strongly affected by component type, lead time, and supplier reliability.
- A batch-level classification model can identify high-risk production before defects become expensive.
- Statistical testing reveals meaningful differences in quality outcomes across suppliers.

## How to Run

### Python Environment

This project requires Python 3.8+ with the following packages:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn jupyter notebook
```

### Generate the Data

```bash
python generate_data.py
```

### Launch the Notebooks

```bash
jupyter notebook
```

Then open the notebooks in the `notebooks/` directory in order:

1. 01_eda.ipynb
2. 02_feature_engineering.ipynb
3. 03_statistical_analysis.ipynb
4. 04_predictive_modeling.ipynb
5. 05_visualization_report.ipynb

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Scikit-learn
- Jupyter Notebook

## Project Notes

This project is intentionally synthetic but designed to reflect realistic manufacturing behavior and supply-chain variability. It serves as a portfolio-ready example of end-to-end data science work, from raw data generation through modeling and executive reporting.

## Author

CS F320 Student / Data Science Portfolio Project

## Date

September 2026
