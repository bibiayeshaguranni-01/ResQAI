# ResQAI - AI-Powered Disaster Risk & Emergency Response System

## Overview

ResQAI is a multi-disaster data project. It combines six cleaned CSV datasets into one master dataset for analysis and future machine-learning work.

The project covers:

- Droughts
- Earthquakes
- Volcanic eruptions
- Floods
- Forest fires
- Tropical cyclones

ResQAI organizes disaster information. It does not predict disasters yet.

## Objectives

- Load and clean disaster datasets.
- Use one common structure for different disaster types.
- Combine the datasets into one master CSV file.
- Explore severity, location, dates, and impact data.
- Prepare the data for future machine-learning models.

## Datasets

The six source files are:

| File | Records |
| --- | ---: |
| `Drought_clean.csv` | 240 |
| `Earthquake_clean.csv` | 20,290 |
| `Eruption_clean.csv` | 61 |
| `Flood_clean.csv` | 2,126 |
| `Forest_Fires_clean.csv` | 3,051 |
| `Tropical_Cyclone_clean.csv` | 405 |
| **Total** | **26,173** |

The datasets contain information such as descriptions, dates, countries, coordinates, severity, and disaster-specific impact measurements.

## Master Dataset

`master_disaster_dataset_cleaned.csv` is the committed output created from the six source files in `ResQAI_Project.ipynb`. The notebook may create `master_disaster_dataset.csv` temporarily before cleaning, but that intermediate file is not committed.

The notebook:

1. Loads the six CSV files with pandas.
2. Adds a `disaster_type` column.
3. Standardizes column names.
4. Selects common columns:
   - `description`
   - `alertlevel`
   - `alertscore`
   - `episodealertlevel`
   - `episodealertscore`
   - `country`
   - `fromdate`
   - `todate`
   - `iso3`
   - `gdacs_id`
   - `longitude`
   - `latitude`
   - `disaster_type`
5. Adds missing columns with `NaN` values when needed.
6. Combines all records with `pandas.concat()`.
7. Saves the cleaned result as `master_disaster_dataset_cleaned.csv`.

The final cleaned master dataset contains 26,173 rows and 13 columns.

## Data Processing

The project checks and prepares the data by:

- Inspecting columns and data types.
- Checking missing values.
- Standardizing dates and coordinates.
- Preserving disaster-specific fields.
- Creating common fields for comparison.
- Avoiding invented values.

## Machine Learning Status

No final machine-learning model has been trained yet. The data is being prepared for future classification, regression, clustering, and risk-analysis experiments.

Future model work should define a clear target, remove data leakage, split the data correctly, and use suitable evaluation metrics.

## Project Structure

```text
ResQAI/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- ResQAI_Project.ipynb
|-- Drought_clean.csv
|-- Earthquake_clean.csv
|-- Eruption_clean.csv
|-- Flood_clean.csv
|-- Forest_Fires_clean.csv
|-- Tropical_Cyclone_clean.csv
|-- master_disaster_dataset_cleaned.csv
|-- src/resqai/
`-- tests/
```

## Installation

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

## How to Run

Run the application:

```powershell
$env:PYTHONPATH = "src"
python -m resqai.main
```

Run the tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Open the notebook to recreate the master dataset:

```powershell
jupyter notebook ResQAI_Project.ipynb
```

## Technology

- Python
- pandas
- scikit-learn
- Jupyter Notebook
- unittest

## Current Limitations

- No final machine-learning model is available.
- No dashboard is available yet.
- The six source files use different columns for disaster-specific measurements.
- Some values may be missing.
- Risk prediction is planned for a future version.

## Future Work

- Complete exploratory data analysis.
- Train and compare machine-learning models.
- Add explainable risk analysis.
- Build an emergency-response dashboard.
- Add more validated disaster datasets.
