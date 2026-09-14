# ResQAI - AI-Powered Disaster Risk & Emergency Response System

## Overview

ResQAI is a multi-disaster data analysis project. It combines cleaned disaster records into a common dataset for data quality checks, exploratory analysis, feature engineering, and future machine-learning experiments.

The project covers droughts, earthquakes, volcanic eruptions, floods, forest fires, and tropical cyclones. It organizes disaster information; it does not currently predict disasters.

## Problem Statement

Disaster datasets often come from different sources and use different column names, date formats, measurements, and missing-value conventions. This makes it difficult to compare disaster types or prepare them for analysis.

ResQAI addresses this problem by standardizing shared fields while preserving measurements that are specific to each disaster type.

## Objectives

- Combine six disaster datasets into one analysis-ready dataset.
- Standardize shared columns such as dates, coordinates, country, and disaster type.
- Inspect missing values, duplicates, invalid values, and inconsistent categories.
- Create useful date, duration, and location features.
- Prepare reliable inputs for future machine-learning models.
- Keep the workflow reproducible through a Jupyter Notebook.

## Key Features

- Multi-disaster dataset preparation.
- Common schema for cross-disaster comparison.
- Disaster-specific feature preservation.
- Date parsing and duration calculation.
- Country and location-category cleaning.
- Missing-value and duplicate analysis.
- Class-distribution analysis for machine learning.
- Reproducible CSV export.

## Dataset

The project uses six cleaned disaster datasets with 26,173 records in total:

| Disaster type | Records |
| --- | ---: |
| Drought | 240 |
| Earthquake | 20,290 |
| Volcanic eruption | 61 |
| Flood | 2,126 |
| Forest fire | 3,051 |
| Tropical cyclone | 405 |
| **Total** | **26,173** |

The data includes descriptions, alert levels, dates, countries, ISO3 codes, coordinates, severity scores, and disaster-specific impact measurements.

The cleaned master output contains common fields such as `description`, `alertlevel`, `alertscore`, `country`, `fromdate`, `todate`, `iso3`, `longitude`, `latitude`, and `disaster_type`.

## Data Preprocessing

The notebook performs the following preparation steps:

1. Loads the six CSV datasets with pandas.
2. Standardizes column names and removes unnecessary index columns.
3. Adds a `disaster_type` label.
4. Aligns shared columns across all datasets.
5. Combines the records into a master dataset.
6. Converts date columns to datetime values.
7. Creates year, month, and event-duration features.
8. Replaces invalid negative scores with missing values.
9. Cleans country names and identifies multi-location records.
10. Checks duplicates, missing values, coordinate ranges, and invalid dates.

## Exploratory Data Analysis

The analysis examines:

- Record counts by disaster type.
- Alert-level distributions.
- Missing values by column and disaster type.
- Duplicate records and repeated descriptions.
- Country and ISO3 distributions.
- Geographic and multi-location records.
- Severity-score distributions.
- Event duration and date ranges.
- Invalid latitude, longitude, year, month, and duration values.

Earthquakes represent the largest class, while eruptions represent the smallest. This imbalance must be considered before training a classification model.

## Machine Learning

The current notebook prepares a classification dataset where `disaster_type` is the target. Candidate features include alert level, alert scores, longitude, latitude, year, month, and calculated duration.

The workflow separates the target from the input features, performs a stratified 80/20 train/test split, and uses a preprocessing pipeline:

- Numeric values are median-imputed and scaled.
- The categorical alert level is filled using the most frequent value and one-hot encoded.
- The preprocessor is fitted only on the training data.

No final model has been trained yet.

## Model Evaluation

Model evaluation is not yet available because model training is still pending. Future experiments should use metrics appropriate for the selected task, including accuracy, balanced accuracy, precision, recall, F1 score, a confusion matrix, and per-class results.

Because the classes are imbalanced, accuracy alone should not be used to judge performance.

## System Architecture

```text
Six cleaned disaster datasets
              |
              v
       Data loading
              |
              v
   Column standardization
              |
              v
    Dataset combination
              |
              v
 Cleaning and feature engineering
              |
              v
       Exploratory analysis
              |
              v
 Train/test preprocessing
              |
              v
 Future ML models and risk services
```

## Technology Stack

- Python 3.10 or newer.
- pandas for loading, cleaning, and combining datasets.
- NumPy for numerical operations.
- scikit-learn for splitting and preprocessing.
- Jupyter Notebook for the analysis workflow.
- unittest for project tests.

## Project Structure

```text
ResQAI/
|-- README.md
|-- requirements.txt
|-- ResQAI_Project.ipynb
|-- src/resqai/
|   |-- data/
|   |-- frontend/
|   |-- ml_models/
|   |-- preprocessing/
|   `-- utils/
`-- tests/
```

## Installation

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Usage

Open the notebook from the project directory to run the complete data workflow:

```powershell
jupyter notebook ResQAI_Project.ipynb
```

Run the application status command:

```powershell
$env:PYTHONPATH = "src"
python -m resqai.main
```

Run the tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Results

- Six disaster datasets were combined into a common analysis workflow.
- The combined dataset contains 26,173 records.
- Shared dates, coordinates, countries, alert fields, and disaster labels are available for comparison.
- Date and duration features were created.
- Missing values, duplicate records, invalid coordinates, and unusual durations were investigated.
- Training and test data can now be prepared without fitting preprocessing on the test set.
- No final model performance results are available yet.

## Future Scope

- Train and compare classification models.
- Improve class balancing and validation strategies.
- Add visual dashboards for disaster trends and locations.
- Add explainable risk scoring.
- Preserve more disaster-specific features in model experiments.
- Add automated data-quality reports.
- Develop emergency-response services.

## Limitations

- The six datasets use different disaster-specific columns.
- The target classes are highly imbalanced.
- Some values, coordinates, and dates may be missing.
- A final machine-learning model has not been trained.
- Model evaluation results are not available yet.
- The project does not currently provide real-time data or a completed dashboard.
