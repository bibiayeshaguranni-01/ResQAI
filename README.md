# ResQAI

## Project Overview

ResQAI is a multi-disaster information platform for collecting, validating, normalizing, and preparing emergency data. It uses one consistent format for earthquakes, floods, wildfires, storms, hurricanes, tornadoes, landslides, tsunamis, volcanic eruptions, droughts, and extreme temperatures.

The project uses six cleaned disaster CSV files for analysis and provides live-feed integration for future provider updates. Each file keeps disaster-specific measurements while sharing useful fields such as description, dates, location, severity, and impact.

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
- Loading and cleaning six disaster CSV files.
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

The project dataset contains six cleaned CSV files:

- `Drought_clean.csv`: 240 records, including drought severity, affected area, duration, and location.
- `Earthquake_clean.csv`: 20,290 records, including magnitude, depth, exposed population, and location.
- `Eruption_clean.csv`: 61 records, including volcanic explosivity, population exposure, severity, and location.
- `Flood_clean.csv`: 2,126 records, including severity, deaths, displaced people, and location.
- `Forest_Fires_clean.csv`: 3,051 records, including burned area, affected people, duration, and location.
- `Tropical_Cyclone_clean.csv`: 405 records, including wind speed, storm surge, vulnerability, category, and location.

Together, the six files contain 26,173 records. The files use different column names for disaster-specific measurements, but they share common concepts such as description, start date, end date, country, coordinates, severity, and impact.

The current live source is the USGS Earthquake Catalog GeoJSON feed:

- Documentation: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php>
- Live endpoint: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson>

The USGS feed is public and does not require an API key. It provides recent earthquake records, not historical records for every disaster type.

## Data Preprocessing

The CSV preprocessing workflow:

1. Loads each disaster CSV from the project directory.
2. Inspects columns, row counts, missing values, and data types.
3. Standardizes date and coordinate fields where possible.
4. Preserves disaster-specific severity and impact measurements.
5. Checks numeric fields for invalid values.
6. Keeps the disaster category and source fields for analysis.
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
- The feed layer validates data before normalization.
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
- The six CSV files use different schemas and have different available impact fields.
- Some measurements and coordinates may be missing.
- No final machine-learning model or risk prediction system is available yet.
- The USGS all-day feed is a rolling 24-hour window.
- External feeds can be preliminary, revised, unavailable, or changed by their providers.

## Conclusion

ResQAI provides a tested foundation for multi-disaster data collection and analysis. It combines provider validation, common normalization, historical-data cleaning, feature engineering, and leakage-safe preprocessing. The next major step is to train and evaluate models, then connect the results to explainable risk services and an emergency-response dashboard.
