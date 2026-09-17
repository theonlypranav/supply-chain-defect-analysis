# Copilot Instructions for this repository

This repo is a supply-chain defect analysis project used for data science learning and portfolio presentation.

## Scope

- Focus on supplier quality, defect-risk analysis, and predictive modeling
- Use the generated synthetic dataset and project notebooks as the source of truth
- Keep answers grounded in the repository contents rather than generic assumptions

## Preferred answers

- Summarize the project clearly and practically
- Answer with concrete file references when possible
- Mention the notebook series in order: 01_eda, 02_feature_engineering, 03_statistical_analysis, 04_predictive_modeling, and 05_visualization_report
- Use the project findings in `results/OUTPUT_SUMMARY.md` when discussing outcomes

## Validation commands

- `python generate_data.py`
- `python -m streamlit run results/interactive_summary.py`

## Important facts

- Data files are under `data/`
- Reusable logic is under `src/`
- Results and summaries are under `results/`
- The project has an interactive dashboard and report output
