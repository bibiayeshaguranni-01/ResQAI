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

The data collection and normalization foundation is working and tested. Earthquakes are currently connected through USGS, and the normalizer can already represent other disaster types. Additional live sources, machine learning, risk prediction, a database, GenAI/RAG, and a finished dashboard are future additions.

ResQAI is intended to organize and prioritize information. It does not predict disasters.

## Technology Stack

Current implementation:

- Python 3.10 or newer: application language.
- Python standard library: HTTP client, JSON parsing, validation, normalization, and tests.
- `venv`: isolated project environment.
- `unittest`: basic automated testing.

No machine-learning library is used in the current implementation.

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

At present, data collection and normalization are implemented for the USGS earthquake source, and the common format supports other disaster types. Risk rules, emergency services, and the dashboard are planned.

## Project Structure

```text
ResQAI/
|-- .env.example
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- src/
|   `-- resqai/
|       |-- __init__.py
|       |-- main.py
|       |-- api/
|       |-- data/
|       |-- frontend/
|       |-- ml_models/
|       |-- preprocessing/
|       |-- services/
|       `-- utils/
`-- tests/
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

The requirements file contains no third-party packages because the current implementation uses only the Python standard library.

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
Data collection, risk assessment, and dashboard features are planned for later phases.
```

Run the smoke test:

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

## Current Scope

The current implementation adds one verified real-world data source and a normalized service boundary. It does not include machine learning, risk calculations, GenAI/RAG, persistence, or a completed dashboard. Risk modeling and the dashboard remain future work.

## Data Pipeline

The public service is available through `get_current_earthquakes()`:

```python
from resqai.services.disaster_data import get_current_earthquakes

records = get_current_earthquakes()
print(records[0])
```

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
- `src/resqai/data/normalization.py`: `normalize_usgs_features()` converts provider records into stable ResQAI dictionaries and skips unusable records.
- `src/resqai/services/disaster_data.py`: `get_current_earthquakes()` is the application-facing service boundary.
- `tests/test_data_pipeline.py`: tests success, missing values, malformed data, HTTP errors, timeout behavior, and configuration validation.

## What You Need to Configure

For USGS, nothing secret is required. Optionally set the feed URL and timeout shown above. Do not put real credentials in `.env.example`, source files, notebooks, or committed test data.

## What to Learn Next

Learn HTTP status handling, GeoJSON structure, UTC timestamps, schema validation, dependency injection for network tests, and the difference between preliminary observations and confirmed historical data. Next, learn how to store raw responses with provenance and define explainable risk rules without presenting them as disaster predictions.
