# ResQAI - AI-Powered Disaster Risk & Emergency Response System

## Overview

ResQAI is a multi-disaster data preparation and analysis project. It combines six cleaned disaster datasets into a common structure for data-quality checks, exploratory analysis, feature engineering, and train/test preparation.

The project covers earthquakes, floods, droughts, forest fires, volcanic eruptions, and tropical cyclones.

## Problem Statement

Disaster datasets use different column names, date formats, measurements, and missing-value conventions. This makes it difficult to compare disaster types and prepare consistent analysis data.

ResQAI standardizes shared fields while preserving disaster-specific information.

## Objectives

- Combine six disaster datasets.
- Standardize shared columns.
- Inspect missing values and duplicates.
- Check invalid coordinates, dates, scores, and durations.
- Create year, month, duration, and location features.
- Prepare data for train/test processing.

## Key Features

- Multi-disaster dataset preparation.
- Common schema for comparison.
- Date and duration feature creation.
- Country and location cleaning.
- Missing-value and duplicate analysis.
- Stratified train/test split.
- Training-only preprocessing with imputation, scaling, and encoding.

## Dataset

The six cleaned datasets contain 26,173 records:

| Disaster type | Records |
| --- | ---: |
| Earthquake | 20,290 |
| Forest fire | 3,051 |
| Flood | 2,126 |
| Tropical cyclone | 405 |
| Drought | 240 |
| Volcanic eruption | 61 |
| **Total** | **26,173** |

The data includes descriptions, alert levels, dates, countries, ISO3 codes, coordinates, severity scores, and disaster-specific measurements.

Dataset source: [Global Disaster Events (2000-2025) on Kaggle](https://www.kaggle.com/datasets/elvinrustam/global-disaster-events-20002025)

## Data Preprocessing

The notebook currently:

1. Loads the six CSV datasets with pandas.
2. Standardizes column names.
3. Removes unnecessary index columns.
4. Adds a `disaster_type` label.
5. Combines the datasets into a common analysis table.
6. Converts date columns to datetime values.
7. Creates year, month, and event-duration features.
8. Replaces invalid negative scores with missing values.
9. Cleans country values and identifies location types.
10. Checks missing values, duplicates, coordinates, dates, and durations.
11. Creates `X` and `y` for disaster-type classification.
12. Splits the data using a stratified 80/20 split.
13. Fits preprocessing only on the training data.

## Exploratory Data Analysis

The notebook checks:

- Disaster-type counts.
- Alert-level counts.
- Missing values.
- Duplicate records and descriptions.
- Country and ISO3 values.
- Geographic and multi-location records.
- Severity-score distributions.
- Event durations.
- Invalid coordinates and dates.

## Technology Stack

- Python
- pandas
- NumPy
- scikit-learn
- Jupyter Notebook
- unittest

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

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Usage

Open the notebook from the project directory:

```powershell
jupyter notebook ResQAI_Project.ipynb
```

Run the tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```
