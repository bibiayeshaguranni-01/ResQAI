# ResQAI

ResQAI is an AI-powered disaster risk and emergency response system. It is being developed as an Information Science and Engineering project to monitor real-world emergency information, assess risk, prioritize incidents, and present useful response information.

## Problem Statement

Emergency information can be distributed across different sources and may be difficult to compare quickly. ResQAI will provide a structured way to collect, normalize, assess, and display disaster-related information. The system will support monitoring and prioritization; it will not claim to predict future disasters unless a later, validated model supports that claim.

## Objectives

- Collect reliable real-world disaster and emergency information.
- Normalize incoming information into a consistent application format.
- Prepare data for analysis and, where justified, machine learning.
- Assess incident severity or priority using explainable logic and validated models.
- Provide useful emergency-response information.
- Present results through an interactive dashboard.
- Keep the implementation understandable, testable, and suitable for academic demonstration.

## Planned Features

- Real-world disaster data integration.
- Data cleaning and preprocessing.
- Historical dataset analysis.
- Risk assessment and incident prioritization.
- Emergency-response information services.
- Interactive dashboard.
- Optional GenAI or RAG support only if it provides clear value and uses reliable sources.

## Technology Stack

Current implementation:

- Python 3.10 or newer: application language.
- Python standard library: HTTP client, JSON parsing, validation, normalization, and tests.
- `venv`: isolated project environment.
- `unittest`: basic automated testing.

No machine-learning library is used in the current implementation.

## Architecture Overview

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

The current foundation contains the package boundaries for these components, but later-stage behavior has not been implemented yet.

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

## Setup Instructions

## Data Source Investigation

### Selected source: USGS Earthquake Catalog GeoJSON feeds

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
