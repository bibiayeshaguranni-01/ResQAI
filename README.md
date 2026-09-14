# ResQAI

ResQAI is a project for collecting and organizing disaster information so that it can be easier to understand and use during emergency response. It is designed for many disaster types, not only earthquakes.

## What ResQAI Does

The current version has a common format for all disaster records and connects to the public USGS earthquake feed. It:

1. Downloads recent earthquake information.
2. Checks that the response has the expected format.
3. Converts the data into a simple, consistent ResQAI format.
4. Skips records that are missing important information instead of inventing values.
5. Reports clear errors when the data source cannot be reached or is invalid.

In simple terms, ResQAI takes information from different disaster sources and prepares it for one emergency-response dashboard.

Supported disaster categories include earthquakes, floods, wildfires, storms, hurricanes, tornadoes, landslides, tsunamis, volcanic eruptions, droughts, and extreme temperatures. The shared format is ready for these categories; live source adapters will be added as each source is verified.

## Current Status

The data collection and normalization foundation is working and tested. Earthquakes are currently connected through USGS, and the normalizer can already represent other disaster types. The historical-data pipeline prepares a genuine NOAA dataset for machine-learning experiments. Training the final model, additional live sources, risk prediction, a database, GenAI/RAG, and a finished dashboard are future additions.

ResQAI is intended to organize and prioritize information. It does not predict disasters.

## Technology Stack

Current implementation:

- Python 3.10 or newer: application language.
- `pandas`: historical dataset loading, inspection, and cleaning.
- `scikit-learn`: train/test splitting and leakage-safe preprocessing.
- Python standard library: HTTP client, JSON parsing, validation, normalization, and tests.
- `venv`: isolated project environment.
- `unittest`: basic automated testing.

No final machine-learning model is trained in the current implementation.

## How It Works

```text
External disaster sources
          |
          v
     Data collection
          |
          v
   Normalization and preprocessing
          |
          v
 Risk rules and validated ML models
          |
          v
 Emergency information services
          |
          v
      Interactive dashboard
```

At present, data collection and normalization are implemented for the USGS earthquake source, and the historical-data pipeline prepares NOAA storm-event history for ML. Risk rules, model training, emergency services, and the dashboard are planned.

## Project Structure

```text
ResQAI/
|-- .env.example
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- Drought_clean.csv
|-- Earthquake_clean.csv
|-- Eruption_clean.csv
|-- Flood_clean.csv
|-- Forest_Fires_clean.csv
|-- Tropical_Cyclone_clean.csv
|-- master_disaster_dataset.csv
|-- src/
|   `-- resqai/
|       |-- __init__.py
|       |-- main.py
|       |-- api/
|       |-- data/
|       |   `-- historical_storm_events.py
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

## Data Source

### Current source: USGS Earthquake Catalog GeoJSON feeds

- **Name:** United States Geological Survey (USGS) Earthquake Hazards Program GeoJSON feed.
- **Information:** Recent earthquake events worldwide, including magnitude, place, time, depth, status, tsunami flag, alert, and event links.
- **Important fields:** `id`; `properties.mag`; `properties.place`; `properties.time`; `properties.updated`; `properties.status`; `properties.alert`; `properties.tsunami`; `properties.felt`; `properties.url`; and `geometry.coordinates` as longitude, latitude, depth in kilometers.
- **Update frequency:** Summary feeds are near-real-time feeds intended to be checked about every minute. The selected `all_day.geojson` feed covers the previous 24 hours.
- **API requirements:** HTTPS GET with an `Accept` header. The response is GeoJSON.
- **API key:** Not required for this public feed.
- **Limitations:** It covers earthquakes, not every disaster type; records can be preliminary and later revised; optional fields can be null; the all-day feed is a rolling window rather than historical storage; and USGS availability and usage policies still apply.
- **Why suitable:** It is an official scientific source, public, structured, global, actively updated, and includes location and severity-related fields useful for ResQAI monitoring. It also keeps the implementation dependency-free and secret-free.

Source documentation: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php>

Live endpoint: <https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson>

## Setup and Installation

1. Open a terminal in the project directory.
2. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

3. Activate it on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. Install the current requirements:

   ```powershell
   python -m pip install -r requirements.txt
   ```

The requirements file contains `pandas` and `scikit-learn` for the historical-data pipeline. The live API and existing normalization code still use the Python standard library.

5. Review `.env.example`. Set the values as process environment variables when needed. The application does not automatically load `.env` files.

   ```powershell
   $env:RESQAI_USGS_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
   $env:RESQAI_API_TIMEOUT_SECONDS = "10"
   ```

   No API key or secret is required for USGS.

## Run Instructions

Run the application from the project root:

```powershell
$env:PYTHONPATH = "src"
python -m resqai.main
```

Expected output:

```text
ResQAI foundation is ready.
Data collection and historical-data preprocessing are ready. Model training, risk assessment, and dashboard features are planned for later phases.
```

Run the smoke test:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Historical Dataset and Preprocessing

### ML problem selected

The first practical ML problem is **binary classification of whether a reported storm event has any casualty**. The target is `casualty_reported`:

```text
1 if deaths_direct + deaths_indirect + injuries_direct + injuries_indirect > 0
0 otherwise
```

This is a more defensible first problem than trying to predict where or when a disaster will happen. The available event description, location, time, and magnitude fields can be used to study whether an event record is associated with reported human impact. This is an analysis target, not a claim that the system can predict disasters.

### Dataset source

- **Dataset:** NOAA Storm Events Database, 2023 detail file.
- **Publisher:** National Centers for Environmental Information (NCEI), National Oceanic and Atmospheric Administration (NOAA).
- **Official source:** <https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/StormEvents_details-ftp_v1.0_d2023_c20260323.csv.gz>
- **Purpose:** Provide historical records of severe weather and storm events in the United States, including event type, timing, location, magnitude, and reported impacts.
- **Records:** 75,593 records in the downloaded 2023 archive used for this implementation.
- **Columns:** 51 columns in the source file.

### Important columns

- `EVENT_ID`: unique event identifier.
- `EVENT_TYPE`: storm or hazard category, such as flood or thunderstorm wind.
- `STATE`, `CZ_TYPE`, and `BEGIN_LAT`/`BEGIN_LON`: geographic information.
- `YEAR`, `MONTH_NAME`, `BEGIN_DATE_TIME`, and `END_DATE_TIME`: event timing.
- `MAGNITUDE`, `MAGNITUDE_TYPE`, `BEGIN_RANGE`, and `BEGIN_AZIMUTH`: event measurements and location descriptors.
- `DEATHS_DIRECT`, `DEATHS_INDIRECT`, `INJURIES_DIRECT`, and `INJURIES_INDIRECT`: used to create the target, then excluded from the features to prevent leakage.

### Features and target

The feature matrix uses:

- Numeric features: year, event month, magnitude, beginning range, beginning latitude, beginning longitude, and engineered duration in hours.
- Categorical features: event type, state, month name, county-zone type, magnitude type, and beginning azimuth.
- Engineered features: `event_month` from the event timestamp and non-negative `duration_hours` from the start and end timestamps.

The target is `casualty_reported`. Impact columns are never passed into `X`. The preprocessing transformer is fitted only on `X_train`; the test data is transformed afterward with the already-fitted transformer.

### Inspection and cleaning results

The real 2023 archive was inspected before preprocessing:

- Duplicate complete rows: 0.
- Duplicate event IDs: 0.
- Invalid latitude values: 0.
- Invalid longitude values: 0.
- Negative death or injury counts: 0.
- Event types: 51.
- States or territories: 67.
- Target records with a reported casualty: 927.
- Target records without a reported casualty: 74,666.

Cleaning removes duplicate rows and duplicate event IDs, removes records without required identity, event type, or impact values, rejects negative impact counts, and converts invalid measurements to missing values for later imputation. The dataset is strongly imbalanced, so future model evaluation must use metrics such as precision, recall, F1, and a confusion matrix rather than accuracy alone.

### Limitations and suitability

The dataset covers NOAA-recorded storm events in the United States, not every disaster worldwide. Reporting practices changed over time and differ by event type and location. A casualty label records reported impact, not total harm, and the positive class is much smaller than the negative class. Some measurements are missing, and the 2023 file is a fixed historical snapshot that may be revised by NOAA.

It is suitable for the historical-data pipeline because it is an official, public, documented dataset with many records, multiple disaster categories, event timing and location, measurable severity fields, and explicit impact outcomes. It is also large enough to demonstrate inspection, cleaning, feature engineering, categorical encoding, scaling, and a stratified split without fabricating observations.

### Reusable pipeline functions

The implementation is in `src/resqai/data/historical_storm_events.py`:

- `load_storm_events()` loads the official CSV or a local copy.
- `inspect_storm_events()` reports shape, missing values, duplicates, types, and invalid values.
- `clean_storm_events()` removes duplicates and invalid records.
- `engineer_storm_event_features()` creates the calendar, duration, and target fields.
- `split_and_preprocess()` separates `X` and `y`, creates a stratified 80/20 split, fits imputation/encoding/scaling on training data only, and transforms the test data.
- `prepare_storm_events()` runs the complete pipeline without training a model.

### Complete pipeline

```text
DATASET
   NOAA Storm Events 2023 detail CSV, 75,593 records
          |
          v
DATA INSPECTION
   Missing values, data types, duplicates, invalid ranges, target balance
          |
          v
CLEANING
   Remove duplicate/unusable records; reject negative impacts;
   preserve valid missing measurements for imputation
          |
          v
FEATURE ENGINEERING
   Event month, event duration, and casualty_reported target
          |
          v
X / y
   X contains event metadata only; y is casualty_reported
          |
          v
TRAIN / TEST SPLIT
   Stratified 80/20 split with random_state=42
          |
          v
PREPROCESSING
   Median-impute and scale numeric columns;
   most-frequent-impute and one-hot encode categorical columns
```

No final ML model is trained yet. The pipeline stops after producing reusable, transformed training and test data.

## Data Pipeline

The public service is available through `get_current_earthquakes()`:

```python
from resqai.services.disaster_data import get_current_earthquakes

records = get_current_earthquakes()
print(records[0])
```

For another disaster type, use the provider-neutral service with a GeoJSON feed:

```python
from resqai.services.disaster_data import get_current_disasters

records = get_current_disasters(
   url="https://example.com/wildfires.geojson",
   source="Example provider",
   disaster_type="wildfire",
)
```

Each provider must supply a GeoJSON `FeatureCollection` with feature IDs, event times, and valid coordinates. A provider adapter can map a different response format into this structure before normalization.

```text
RAW DATA
{
   "id": "us-test-1",
   "properties": {"mag": 5.2, "place": "10 km north of Testville", "time": 1700000000000},
   "geometry": {"coordinates": [12.5, 45.25, 8.0]}
}
            |
            v
DATA PROCESSING
Validate FeatureCollection and feature shape; convert epoch milliseconds;
map longitude/latitude/depth; preserve missing optional fields.
            |
            v
NORMALIZED DATA
{
   "source": "USGS", "disaster_type": "earthquake", "magnitude": 5.2,
   "latitude": 45.25, "longitude": 12.5, "depth_km": 8.0
}
            |
            v
RESQAI DATA FORMAT
{
   "id": "us-test-1", "source": "USGS", "title": "...",
   "location": "10 km north of Testville", "occurred_at": "2023-11-14T22:13:20+00:00",
   "severity": "unclassified", "status": "reviewed", "tsunami": false,
   "data_quality": "complete"
}
```

The example values are a deterministic test fixture, clearly labelled as such; normal application calls use live USGS data. Optional values such as `alert`, `felt`, and `updated` remain `None` when absent. Invalid records without an ID, valid coordinates, or an event time are skipped rather than fabricated.

## Error Handling

- HTTP errors and connection failures raise `EarthquakeApiError`.
- Timeouts raise `EarthquakeApiTimeout` and use `RESQAI_API_TIMEOUT_SECONDS`.
- Invalid JSON or an invalid top-level GeoJSON response raises `EarthquakeResponseError`.
- Missing optional fields are represented explicitly as `None` or a documented fallback such as `"unclassified"`.
- Tests inject a fake opener, so tests never depend on network availability.

## Important Files and Functions

- `src/resqai/api/usgs_earthquakes.py`: `feed_settings()` reads configuration; `fetch_usgs_feed()` performs the request; `validate_feed()` checks the response envelope; custom exceptions distinguish failure categories.
- `src/resqai/api/disaster_feeds.py`: `fetch_disaster_feed()` loads and validates a GeoJSON feed from any provider.
- `src/resqai/data/normalization.py`: `normalize_usgs_features()` converts provider records into stable ResQAI dictionaries and skips unusable records.
- `src/resqai/data/historical_storm_events.py`: historical-data loading, inspection, cleaning, feature engineering, splitting, and preprocessing functions.
- `src/resqai/services/disaster_data.py`: `get_current_earthquakes()` preserves the USGS service and `get_current_disasters()` supports generic GeoJSON providers.
- `tests/test_data_pipeline.py`: tests success, missing values, malformed data, HTTP errors, timeout behavior, and configuration validation.
- `tests/test_historical_storm_events.py`: tests the historical dataset pipeline.

## What You Need to Configure

For USGS, nothing secret is required. Optionally set the feed URL and timeout shown above. Do not put real credentials in `.env.example`, source files, notebooks, or committed test data.

## What to Learn Next

Learn HTTP status handling, GeoJSON structure, UTC timestamps, schema validation, dependency injection for network tests, and the difference between preliminary observations and confirmed historical data. Next, learn how to store raw responses with provenance and define explainable risk rules without presenting them as disaster predictions.
