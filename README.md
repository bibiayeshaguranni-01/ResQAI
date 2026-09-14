# ResQAI

## Project Overview

ResQAI is a multi-disaster information platform for collecting, validating, normalizing, and preparing emergency data. It uses one consistent format for earthquakes, floods, wildfires, storms, hurricanes, tornadoes, landslides, tsunamis, volcanic eruptions, droughts, and extreme temperatures.

The project combines live disaster-feed integration with historical-data preprocessing. USGS earthquakes are the current live-feed example, while NOAA storm-event data supports historical analysis and machine-learning preparation.

## Problem Statement

Disaster information is often distributed across different providers and formats. Emergency-response applications need data that is consistent, validated, traceable, and usable across multiple disaster categories.

ResQAI addresses the data-organization problem. It does not predict when or where disasters will occur.

## Objectives

- Collect disaster data from public and local sources.
- Validate provider responses before processing them.
- Normalize different disaster records into a common format.
- Preserve source, location, time, severity, and data-quality information.
- Prepare historical disaster data for machine-learning experiments.
- Skip incomplete or invalid records instead of inventing values.
- Report clear errors when a data source fails or returns invalid data.

## Key Features

- Provider-neutral GeoJSON feed support.
- USGS earthquake feed integration.
- Shared record format for multiple disaster types.
- Historical NOAA storm-event loading and cleaning.
- Duplicate detection and invalid-value handling.
- Feature engineering for event month, duration, and reported casualties.
- Leakage-safe train/test preprocessing.
- Automated tests for valid data, invalid data, timeouts, and HTTP failures.

## System Workflow

```text
Public or local disaster sources
              |
              v
       Data collection
              |
              v
      Response validation
              |
              v
   Cleaning and normalization
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

Data collection, validation, normalization, and historical preprocessing are implemented. Risk rules, trained models, emergency services, and the dashboard are planned extensions.

## Dataset

The repository contains cleaned datasets for several disaster categories:

- `Drought_clean.csv`
- `Earthquake_clean.csv`
- `Eruption_clean.csv`
- `Flood_clean.csv`
- `Forest_Fires_clean.csv`
- `Tropical_Cyclone_clean.csv`
- `master_disaster_dataset.csv`

The historical machine-learning pipeline uses the NOAA Storm Events Database 2023 detail file. It contains 75,593 United States storm-event records and 51 columns, including event type, location, timing, magnitude, deaths, and injuries.

The current live source is the USGS Earthquake Catalog GeoJSON feed:

- Documentation: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php>
- Live endpoint: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson>

The USGS feed is public and does not require an API key. It provides recent earthquake records, not historical records for every disaster type.

## Data Preprocessing

The historical-data pipeline:

1. Loads the NOAA CSV from a URL or local path.
2. Inspects shape, types, missing values, duplicates, and invalid ranges.
3. Removes duplicate rows and duplicate event IDs.
4. Rejects unusable identity, event type, or impact values.
5. Rejects negative death and injury counts.
6. Converts invalid measurements to missing values for later imputation.
7. Separates features from the target before preprocessing.
8. Fits preprocessing only on the training data.

## Exploratory Data Analysis (EDA)

The NOAA dataset inspection found:

- Duplicate complete rows: 0.
- Duplicate event IDs: 0.
- Invalid latitude values: 0.
- Invalid longitude values: 0.
- Negative death or injury counts: 0.
- Event types: 51.
- States or territories: 67.
- Records with a reported casualty: 927.
- Records without a reported casualty: 74,666.

The target is strongly imbalanced, so accuracy alone is not sufficient for future model evaluation. Precision, recall, F1 score, and a confusion matrix should also be used.

## Feature Engineering

The pipeline creates the target `casualty_reported`:

```text
1 if deaths_direct + deaths_indirect + injuries_direct + injuries_indirect > 0
0 otherwise
```

Numeric features include year, event month, magnitude, beginning range, beginning latitude, beginning longitude, and event duration in hours.

Categorical features include event type, state, month name, county-zone type, magnitude type, and beginning azimuth.

Death and injury columns create the target and are excluded from the feature matrix to prevent target leakage.

## Machine Learning Approach

The first machine-learning problem is binary classification of whether a reported storm event has any casualty. The pipeline uses a stratified 80/20 train/test split with `random_state=42`.

Numeric features are median-imputed and scaled. Categorical features are filled with their most frequent value and one-hot encoded. The transformer is fitted only on `X_train` and then applied to `X_test`.

## Models Used

No final classification model has been trained yet. The current implementation prepares clean, transformed training and test data for future models.

## Model Evaluation

Model evaluation is not available yet because model training has not been added. Future evaluation should use metrics suitable for the imbalanced target, including precision, recall, F1 score, and a confusion matrix.

## Results & Findings

- Disaster records can be represented with a shared normalized structure.
- The feed layer validates data before normalization.
- Invalid or incomplete records are skipped instead of fabricated.
- The NOAA dataset is large enough for meaningful preprocessing experiments.
- The casualty target is strongly imbalanced.
- The preprocessing pipeline avoids target leakage.
- A final risk model and dashboard are not part of the current implementation.

## Technology Stack

- Python 3.10 or newer.
- `pandas` for historical dataset loading and cleaning.
- `scikit-learn` for splitting and preprocessing.
- Python standard library for HTTP, JSON, validation, normalization, and tests.
- `unittest` for automated testing.
- `venv` for an isolated development environment.

## Project Structure

```text
ResQAI/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- ResQAI_Project.ipynb
|-- Drought_clean.csv
|-- Earthquake_clean.csv
|-- Eruption_clean.csv
|-- Flood_clean.csv
|-- Forest_Fires_clean.csv
|-- Tropical_Cyclone_clean.csv
|-- master_disaster_dataset.csv
|-- src/
|   `-- resqai/
|       |-- api/
|       |-- data/
|       |-- frontend/
|       |-- ml_models/
|       |-- preprocessing/
|       |-- services/
|       `-- utils/
`-- tests/
    |-- test_data_pipeline.py
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

Optional settings can be provided as environment variables. No API key is required for USGS:

```powershell
$env:RESQAI_USGS_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
$env:RESQAI_API_TIMEOUT_SECONDS = "10"
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

Fetch current earthquake records:

```python
from resqai.services.disaster_data import get_current_earthquakes

records = get_current_earthquakes()
print(records[0])
```

Fetch another disaster type through the provider-neutral service:

```python
from resqai.services.disaster_data import get_current_disasters

records = get_current_disasters(
    url="https://example.com/wildfires.geojson",
    source="Example provider",
    disaster_type="wildfire",
)
```

Each provider must supply a GeoJSON `FeatureCollection` with feature IDs, event times, and valid coordinates. A provider adapter can convert another response format into this structure.

## Screenshots / Demo

The current repository does not include a finished dashboard or screenshots. The command-line demo is the current working demonstration:

```powershell
$env:PYTHONPATH = "src"
python -m resqai.main
```

## Future Enhancements

- Add verified live providers for more disaster categories.
- Train and compare classification models.
- Add explainable risk rules and model predictions.
- Store raw responses with source and timestamp provenance.
- Add a database and scheduled data collection.
- Add GenAI/RAG support with source citations.
- Build an emergency-response dashboard.

## Limitations

- Only the USGS earthquake feed is currently connected as a live provider.
- The NOAA historical dataset covers United States storm events, not every disaster worldwide.
- The casualty label represents reported impact, not total harm.
- The dataset is imbalanced and some measurements are missing.
- No final machine-learning model or risk prediction system is available yet.
- The USGS all-day feed is a rolling 24-hour window.
- External feeds can be preliminary, revised, unavailable, or changed by their providers.

## Conclusion

ResQAI provides a tested foundation for multi-disaster data collection and analysis. It combines provider validation, common normalization, historical-data cleaning, feature engineering, and leakage-safe preprocessing. The next major step is to train and evaluate models, then connect the results to explainable risk services and an emergency-response dashboard.
