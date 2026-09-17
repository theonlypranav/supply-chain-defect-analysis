# AGENTS.md

This repository contains a supply-chain defect analysis project for CS F320, focused on supplier quality, batch defect risk, and predictive modeling.

## Project purpose

- Analyze supplier performance and defect behavior
- Explore quality trends across batches and components
- Run statistical tests to compare supplier risk
- Build classification and regression models for defect prediction
- Produce a portfolio-ready summary and dashboard

## Repository layout

- `data/`: generated CSV datasets for suppliers, batches, QC results, and defects
- `notebooks/`: Jupyter workflow from EDA to reporting
- `src/`: reusable Python modules for loading data, statistics, modeling, and plotting
- `results/`: output summaries and interactive dashboard
- `README.md`: project instructions and overview
- `REPORT.md`: narrative project report

## What this agent should answer

When asked questions about this project, answer using the generated project artifacts and repository structure. Prefer grounded facts from:

- the notebooks in `notebooks/`
- the CSV datasets in `data/`
- the summary markdown in `results/OUTPUT_SUMMARY.md`
- the project README and report

## Response style

- Be concise and practical
- Explain the project in plain English
- Point to the relevant file or notebook when helpful
- Use evidence from the generated data when available
- If the question is about running the project, give the exact command

## Commands to use for validation

- Generate data: `python generate_data.py`
- Run the dashboard: `python -m streamlit run results/interactive_summary.py`
- Open notebooks in order under `notebooks/`

## Key facts

- The repository contains 50 suppliers, 5,000 batches, 50,000 QC records, and 2,000 defect records.
- The project includes EDA, feature engineering, hypothesis testing, and predictive modeling.
- The dashboard and markdown summary live in `results/`.

## Working rules

- Prefer evidence over speculation
- If a claim depends on a notebook or result, cite the file or dataset rather than guessing
- Keep recommendations actionable for QA and supplier-risk decisions
