# Supply Chain Defect Analysis Output Summary

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy
- Scikit-learn
- Jupyter Notebook
- Streamlit (for interactive dashboard viewing)

## Executive Summary

This project analyzed a realistic synthetic electronics supply chain dataset spanning 50 suppliers, 5,000 batches, 50,000 QC checks, and 2,000 recorded defects.

## Key Results

- Total suppliers: 50
- Total batches: 5,000
- Total QC units: 50,000
- Total defects: 2,000
- Overall defect rate: 4.0%
- Mean batch size: 4,996.43 units
- Average supplier quality score: 77.7
- Average supplier lead time: 39.48 days

## Data Science Methods and Tools Used

This project uses a full data science workflow spanning data generation, exploration, feature engineering, statistical inference, and predictive modeling.

### Core tools and libraries

- Python 3.8+
- Pandas for data wrangling and aggregation
- NumPy for numeric transformations and synthetic data generation
- Matplotlib and Seaborn for visual analytics and reporting
- SciPy for hypothesis testing and correlation analysis
- Scikit-learn for classification and regression modeling
- Jupyter Notebook for exploratory analysis and reproducible workflow

### Data science techniques applied

- Exploratory data analysis (EDA)
- Missing-value and duplicate checks
- Outlier detection using z-score logic
- Feature engineering for batch-level quality risk
- Supplier-level and component-level defect-rate analysis
- Statistical testing: t-test, ANOVA, correlation analysis, and normality checks
- Predictive modeling for binary classification and continuous defect-rate prediction
- Model comparison using accuracy, precision, recall, F1-score, RMSE, MAE, and R²
- Business reporting and executive summary visualization

## Top Risk Suppliers

The strongest risk signals appear in the following supplier groups:

- Supplier 3: 0.000529 defect rate
- Supplier 43: 0.000445 defect rate
- Supplier 49: 0.000344 defect rate
- Supplier 21: 0.000341 defect rate
- Supplier 7: 0.000322 defect rate

## High-Risk Components

The most defect-prone component categories are:

- Motherboard: 0.000235 defect rate
- Charger: 0.000226 defect rate
- PCB: 0.000224 defect rate
- Battery: 0.000212 defect rate
- Connector: 0.000208 defect rate

## Interpretation

- Supplier quality differs meaningfully across vendors.
- Defect risk is concentrated in a small subset of suppliers and component families.
- Batch size and process timing matter, but supplier reliability remains the most actionable signal for intervention.
- A predictive model can support proactive QA review before defective units leave the production pipeline.

## Recommended Actions

1. Audit the top-risk suppliers before the next production cycle.
2. Increase final inspection intensity for Motherboard, Charger, PCB, Battery, and Connector batches.
3. Prioritize quality review for batches with long lead times and low supplier quality scores.
4. Use the predictive model as an early-warning system for defect-prone lots.

## Dataset Source

The figures above come from the generated analytical output under the project data folder and the feature-engineered analytical dataset.
