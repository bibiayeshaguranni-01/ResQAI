# ResQAI

## Project Overview

ResQAI is a multi-disaster information platform for collecting, validating, normalizing, and preparing emergency data. It uses one consistent format for earthquakes, floods, wildfires, storms, hurricanes, tornadoes, landslides, tsunamis, volcanic eruptions, droughts, and extreme temperatures.

The project uses six cleaned disaster CSV files for analysis. Each file keeps disaster-specific measurements while sharing useful fields such as description, dates, location, severity, and impact.

## Problem Statement

Disaster information is often distributed across different providers and formats. Emergency-response applications need data that is consistent, validated, traceable, and usable across multiple disaster categories.

ResQAI addresses the data-organization problem. It does not predict when or where disasters will occur.

## Objectives

- Load and combine six disaster datasets.
- Validate and clean dataset values before analysis.
- Standardize shared fields across disaster records.
- Preserve source, location, time, severity, and data-quality information.
- Prepare historical disaster data for machine-learning experiments.
- Skip incomplete or invalid records instead of inventing values.
- Produce a reusable master dataset for analysis.

## Key Features

- Shared analysis format for multiple disaster types.
- Loading and cleaning six disaster CSV files.
- Duplicate detection and invalid-value handling.
- Feature engineering for dates, duration, location, and severity.
- Exploratory analysis of disaster counts and impact fields.
- Automated tests for the historical-data pipeline.

## System Workflow

```text
Six cleaned disaster CSV files
              |
              v
    Data loading
              |
              v
    Data validation
              |
              v
    Standardization
              |
              v
 Historical data preprocessing
              |
              v
   Risk rules and ML models
              |
              v
 Emergency information services
              |
              v
       Dashboard interface
```

Data loading, validation, standardization, master-dataset creation, and exploratory preprocessing are implemented. Risk rules, trained models, emergency services, and the dashboard are planned extensions.

## Dataset

The project dataset contains six cleaned CSV files:

- `Drought_clean.csv`: 240 records, including drought severity, affected area, duration, and location.
- `Earthquake_clean.csv`: 20,290 records, including magnitude, depth, exposed population, and location.
- `Eruption_clean.csv`: 61 records, including volcanic explosivity, population exposure, severity, and location.
- `Flood_clean.csv`: 2,126 records, including severity, deaths, displaced people, and location.
- `Forest_Fires_clean.csv`: 3,051 records, including burned area, affected people, duration, and location.
- `Tropical_Cyclone_clean.csv`: 405 records, including wind speed, storm surge, vulnerability, category, and location.

Together, the six files contain 26,173 records. The files use different column names for disaster-specific measurements, but they share common concepts such as description, start date, end date, country, coordinates, severity, and impact.

### How the Master Dataset Was Created

The notebook creates `master_disaster_dataset.csv` from the six cleaned CSV files. The master file is a standardized analysis output, not a seventh source dataset.

1. Load the six cleaned CSV files with pandas.
2. Add a `disaster_type` label to each file.
3. Standardize column names, including dates, coordinates, and GDACS IDs.
4. Use one common schema:

   `description`, `alertlevel`, `alertscore`, `episodealertlevel`, `episodealertscore`, `country`, `fromdate`, `todate`, `iso3`, `gdacs_id`, `longitude`, `latitude`, and `disaster_type`.

5. Add missing schema columns to each dataset with `NaN` values.
6. Select the common columns in the same order for every dataset.
7. Combine the six tables with `pd.concat(..., ignore_index=True)`.
8. Save the result as `master_disaster_dataset.csv`.

The notebook uses this process:

```python
import numpy as np
import pandas as pd

datasets = {
    "Drought": pd.read_csv("Drought_clean.csv"),
    "Earthquake": pd.read_csv("Earthquake_clean.csv"),
    "Eruption": pd.read_csv("Eruption_clean.csv"),
    "Flood": pd.read_csv("Flood_clean.csv"),
    "Forest Fire": pd.read_csv("Forest_Fires_clean.csv"),
    "Tropical Cyclone": pd.read_csv("Tropical_Cyclone_clean.csv"),
}

master_columns = [
    "description", "alertlevel", "alertscore",
    "episodealertlevel", "episodealertscore", "country",
    "fromdate", "todate", "iso3", "gdacs_id",
    "longitude", "latitude", "disaster_type",
]

prepared = []
for disaster_type, dataframe in datasets.items():
    dataframe = dataframe.copy()
    dataframe["disaster_type"] = disaster_type

    for column in master_columns:
        if column not in dataframe.columns:
            dataframe[column] = np.nan

    prepared.append(dataframe[master_columns])

master_disaster_dataset = pd.concat(prepared, ignore_index=True)
master_disaster_dataset.to_csv("master_disaster_dataset.csv", index=False)
```

This produces a 26,173-row, 13-column master dataset while retaining the original six cleaned files as the source datasets.

## Data Preprocessing

The CSV preprocessing workflow:

1. Loads each of the six disaster CSV files from the project directory.
2. Inspects columns, row counts, missing values, and data types.
3. Standardizes date and coordinate fields where possible.
4. Preserves disaster-specific severity and impact measurements.
5. Checks numeric fields for invalid values.
6. Adds a disaster category to each record.
7. Creates a consistent analysis-ready representation without inventing values.

## Exploratory Data Analysis (EDA)

The current dataset inventory is:

| Disaster type | Records |
| --- | ---: |
| Drought | 240 |
| Earthquake | 20,290 |
| Eruption | 61 |
| Flood | 2,126 |
| Forest fire | 3,051 |
| Tropical cyclone | 405 |
| **Total** | **26,173** |

Exploration should compare event counts, severity, duration, geographic coverage, exposed populations, deaths, displacement, and other impact fields by disaster type. Because the six files do not use one identical schema, analysis should identify shared fields first and then use disaster-specific fields where available.

## Feature Engineering

Potential shared features include disaster type, country, start date, end date, longitude, latitude, severity, and impact. Useful derived features include event duration, event year, event month, and normalized severity values.

Disaster-specific features include earthquake magnitude and depth, flood deaths and displacement, forest-fire area and affected people, cyclone wind speed and storm surge, drought affected area, and eruption explosivity and population exposure. Any future prediction target must be defined carefully so that target-related impact columns are not included as input features.

## Machine Learning Approach

The six CSV files can support classification, regression, clustering, and descriptive analysis. A final target has not been selected yet because the disaster files contain different outcome fields. A future model should use a documented target, a stratified or appropriate split, and preprocessing fitted only on the training data.

Numeric features can be imputed and scaled. Categorical features can be filled and one-hot encoded. The same preprocessing decisions should be applied consistently within each model experiment.

## Models Used

No final machine-learning model has been trained yet. The current work focuses on preparing and understanding the six disaster datasets.

## Model Evaluation

Model evaluation is not available yet because a final target and model have not been selected. Future evaluation should use metrics appropriate for the selected task, such as precision, recall, F1 score, a confusion matrix, mean absolute error, or R-squared.

## Results & Findings

- Disaster records can be represented with a shared normalized structure.
- The dataset workflow validates and standardizes data before analysis.
- Invalid or incomplete records are skipped instead of fabricated.
- The six files contain 26,173 records across six disaster categories.
- Earthquakes make up the largest part of the available records.
- Each disaster type provides different severity and impact measurements.
- Shared date and location fields can support cross-disaster comparisons.
- Disaster-specific fields are needed for detailed analysis.
- A final target, model, and evaluation result have not been selected.
- A final risk model and dashboard are not part of the current implementation.

## Technology Stack

- Python 3.10 or newer.
- `pandas` for historical dataset loading and cleaning.
- `scikit-learn` for splitting and preprocessing.
- Python standard library for file handling, validation, and tests.
- `unittest` for automated testing.
- `venv` for an isolated development environment.

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
|-- src/
|   `-- resqai/
|       |-- data/
|       |-- frontend/
|       |-- ml_models/
|       |-- preprocessing/
|       `-- utils/
`-- tests/
    |-- test_historical_storm_events.py
    `-- test_main.py
```

## Installation & Setup

Open a terminal in the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## How to Run

Run the application from the project root:

```powershell
$env:PYTHONPATH = "src"
python -m resqai.main
```

Run all tests:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Usage / Example

The notebook loads the six source files and creates the master dataset:

```powershell
jupyter notebook ResQAI_Project.ipynb
```

## Screenshots / Demo

The current repository does not include a finished dashboard or screenshots. The command-line demo is the current working demonstration:

```powershell
$env:PYTHONPATH = "src"
python -m resqai.main
```

## Future Enhancements

- Train and compare classification models.
- Add explainable risk rules and model predictions.
- Store processed datasets with source and timestamp provenance.
- Add a database and scheduled data collection.
- Add GenAI/RAG support with source citations.
- Build an emergency-response dashboard.

## Limitations

- The six CSV files use different schemas and have different available impact fields.
- Some measurements and coordinates may be missing.
- No final machine-learning model or risk prediction system is available yet.

## Conclusion

ResQAI provides a tested foundation for multi-disaster dataset analysis. It combines CSV loading, cleaning, standardization, master-dataset creation, exploratory analysis, and feature engineering. The next major step is to train and evaluate models, then connect the results to explainable risk services and an emergency-response dashboard.
