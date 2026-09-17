# Supply Chain Component Defect Analysis Report

## Project Overview

This project examines defect behavior across a synthetic yet realistic electronics supply chain. The analysis covers 50 suppliers, 5,000 component batches, 50,000 QC checks, and 2,000 recorded defects. The goal is to understand which suppliers and batch characteristics contribute most to quality problems and to build predictive models that flag defect-prone batches before they reach the end customer.

## Data Description

The generated datasets contain the following major dimensions:

- Supplier records: 50 rows covering supplier name, country, lead time, unit price, and quality score.
- Batch records: 5,000 batches with component name, production timing, receipt timing, and pass/fail quantities.
- Unit QC results: 50,000 unit-level inspections across eight checkpoints.
- Defect records: 2,000 defect observations with root cause, severity, and checkpoint context.

## Key Findings From EDA

- Defect occurrences vary significantly by supplier and component type.
- Batch size correlates with quality outcomes, suggesting process and scale-related effects.
- Quality scores and lead times are useful predictors of batch-level defect risk.
- A notable minority of suppliers drive the majority of observed failures.

## Statistical Analysis

The project evaluates supplier quality differences with multiple hypothesis tests:

- Two-sample t-test comparing defect rates across high-risk suppliers
- One-way ANOVA across all suppliers
- Correlation analysis between defect rate and production features
- Normality testing using Shapiro-Wilk statistics
- Chi-square test for defect-type distribution patterns

These tests help determine whether the observed supplier-level differences are statistically significant or plausibly due to random variation.

## Predictive Modeling

Two predictive tasks were implemented:

1. Classification: predict whether a batch is high-risk using supplier and process features.
2. Regression: estimate the expected defect rate of a batch.

The recommended models include logistic regression, random forest, and ridge or linear regression as baseline estimators. Random forests generally provide stronger nonlinear performance and feature importance insights.

## Actionable Recommendations

- Prioritize supplier audits for the top-risk vendors identified by defect-rate ranking.
- Increase QC intensity for batches involving high-risk components and long lead times.
- Use the predictive model to trigger preemptive inspections before release.
- Examine recurring defect types by checkpoint and supplier to reduce systematic root causes.

## Business Impact

Reducing avoidable defect escapes can materially lower warranty costs, quality incidents, and customer dissatisfaction. Early identification of high-risk batches creates operational leverage for QA teams and improves supplier performance oversight.

## Limitations

- The data are synthetic and intended for educational and portfolio use.
- There are no external production or cost data to estimate real business impact.
- Defect rates are modeled at the batch level and may not capture every operational nuance.

## Future Work

- Add more real-world contextual features, including machine-level data and inspection timing.
- Explore time-series forecasting for monthly defect trends.
- Extend the modeling framework to multi-class defect prediction and supplier benchmarking dashboards.
- Integrate explainability tools for business stakeholders.

## Conclusion

This project demonstrates an end-to-end approach to supply chain quality analysis. It combines exploratory analysis, statistical testing, feature engineering, and predictive modeling to produce a business-oriented insight narrative that is suitable for a portfolio, coursework submission, or executive summary.
