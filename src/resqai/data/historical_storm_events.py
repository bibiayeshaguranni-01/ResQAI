"""Phase 3 pipeline for the NOAA Storm Events historical dataset."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import IO, Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


NOAA_STORM_EVENTS_2023_URL = (
    "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
    "StormEvents_details-ftp_v1.0_d2023_c20260323.csv.gz"
)
TARGET_COLUMN = "casualty_reported"
IMPACT_COLUMNS = (
    "DEATHS_DIRECT",
    "DEATHS_INDIRECT",
    "INJURIES_DIRECT",
    "INJURIES_INDIRECT",
)
NUMERIC_FEATURES = (
    "YEAR",
    "event_month",
    "MAGNITUDE",
    "BEGIN_RANGE",
    "BEGIN_LAT",
    "BEGIN_LON",
    "duration_hours",
)
CATEGORICAL_FEATURES = (
    "EVENT_TYPE",
    "STATE",
    "MONTH_NAME",
    "CZ_TYPE",
    "MAGNITUDE_TYPE",
    "BEGIN_AZIMUTH",
)
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES


@dataclass(frozen=True)
class DatasetInspection:
    """Quality measurements captured before cleaning."""

    row_count: int
    column_count: int
    missing_values: dict[str, int]
    duplicate_rows: int
    duplicate_event_ids: int
    data_types: dict[str, str]
    invalid_values: dict[str, int]


@dataclass
class PreparedDataset:
    """Leakage-safe train/test arrays and the fitted preprocessing transformer."""

    X_train: Any
    X_test: Any
    y_train: pd.Series
    y_test: pd.Series
    preprocessor: ColumnTransformer
    feature_columns: tuple[str, ...]
    inspection: DatasetInspection
    cleaned_rows: int


def load_storm_events(
    source: pd.DataFrame | str | Path | IO[bytes] = NOAA_STORM_EVENTS_2023_URL,
) -> pd.DataFrame:
    """Load a genuine NOAA Storm Events CSV or gzip-compressed CSV source."""
    if isinstance(source, pd.DataFrame):
        return source.copy()
    return pd.read_csv(source, compression="infer", low_memory=False)


def inspect_storm_events(data: pd.DataFrame) -> DatasetInspection:
    """Inspect shape, missing values, duplicates, types, and invalid values."""
    required_numeric = [*IMPACT_COLUMNS, "BEGIN_LAT", "BEGIN_LON", "MAGNITUDE"]
    invalid_values = {
        column: int((pd.to_numeric(data[column], errors="coerce") < 0).sum())
        for column in IMPACT_COLUMNS
        if column in data.columns
    }
    for column, lower, upper in (("BEGIN_LAT", -90, 90), ("BEGIN_LON", -180, 180)):
        if column in data.columns:
            values = pd.to_numeric(data[column], errors="coerce")
            invalid_values[column] = int((values.notna() & ~values.between(lower, upper)).sum())
    if "MAGNITUDE" in data.columns:
        magnitude = pd.to_numeric(data["MAGNITUDE"], errors="coerce")
        invalid_values["MAGNITUDE"] = int((magnitude.notna() & (magnitude < 0)).sum())
    for column in required_numeric:
        invalid_values.setdefault(column, 0)

    return DatasetInspection(
        row_count=len(data),
        column_count=len(data.columns),
        missing_values={column: int(count) for column, count in data.isna().sum().items()},
        duplicate_rows=int(data.duplicated().sum()),
        duplicate_event_ids=(
            int(data["EVENT_ID"].duplicated().sum()) if "EVENT_ID" in data else 0
        ),
        data_types={column: str(dtype) for column, dtype in data.dtypes.items()},
        invalid_values=invalid_values,
    )


def clean_storm_events(data: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate or unusable events and mark invalid measurements as missing."""
    cleaned = data.copy()
    cleaned = cleaned.drop_duplicates()
    if "EVENT_ID" in cleaned:
        cleaned = cleaned.drop_duplicates(subset=["EVENT_ID"])

    required = ["EVENT_ID", "EVENT_TYPE", *IMPACT_COLUMNS]
    cleaned = cleaned.dropna(subset=[column for column in required if column in cleaned.columns])
    for column in [*IMPACT_COLUMNS, "BEGIN_LAT", "BEGIN_LON", "MAGNITUDE"]:
        if column in cleaned:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    invalid_impact = (cleaned[list(IMPACT_COLUMNS)] < 0).any(axis=1)
    cleaned = cleaned.loc[~invalid_impact].copy()
    if "BEGIN_LAT" in cleaned:
        cleaned.loc[~cleaned["BEGIN_LAT"].between(-90, 90), "BEGIN_LAT"] = pd.NA
    if "BEGIN_LON" in cleaned:
        cleaned.loc[~cleaned["BEGIN_LON"].between(-180, 180), "BEGIN_LON"] = pd.NA
    if "MAGNITUDE" in cleaned:
        cleaned.loc[cleaned["MAGNITUDE"] < 0, "MAGNITUDE"] = pd.NA
    return cleaned.reset_index(drop=True)


def engineer_storm_event_features(data: pd.DataFrame) -> pd.DataFrame:
    """Create calendar and duration features without using casualty outcomes."""
    featured = data.copy()
    begin = pd.to_datetime(
        featured.get("BEGIN_DATE_TIME"), format="%d-%b-%y %H:%M:%S", errors="coerce"
    )
    end = pd.to_datetime(
        featured.get("END_DATE_TIME"), format="%d-%b-%y %H:%M:%S", errors="coerce"
    )
    featured["event_month"] = begin.dt.month.fillna(
        pd.to_numeric(featured.get("BEGIN_YEARMONTH"), errors="coerce") % 100
    )
    featured["duration_hours"] = (end - begin).dt.total_seconds().div(3600).clip(lower=0)
    featured[TARGET_COLUMN] = featured[list(IMPACT_COLUMNS)].sum(axis=1) > 0
    return featured


def split_and_preprocess(
    data: pd.DataFrame, *, test_size: float = 0.2, random_state: int = 42
) -> PreparedDataset:
    """Create X/y, split first, then fit preprocessing only on the training data."""
    inspection = inspect_storm_events(data)
    cleaned = clean_storm_events(data)
    featured = engineer_storm_event_features(cleaned)
    X = featured[list(FEATURE_COLUMNS)]
    y = featured[TARGET_COLUMN].astype("int8")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    numeric_pipeline = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, list(NUMERIC_FEATURES)),
            ("categorical", categorical_pipeline, list(CATEGORICAL_FEATURES)),
        ]
    )
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    return PreparedDataset(
        X_train=X_train_processed,
        X_test=X_test_processed,
        y_train=y_train,
        y_test=y_test,
        preprocessor=preprocessor,
        feature_columns=FEATURE_COLUMNS,
        inspection=inspection,
        cleaned_rows=len(featured),
    )


def prepare_storm_events(
    source: pd.DataFrame | str | Path | IO[bytes] = NOAA_STORM_EVENTS_2023_URL,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> PreparedDataset:
    """Run the complete Phase 3 dataset preparation pipeline."""
    return split_and_preprocess(
        load_storm_events(source), test_size=test_size, random_state=random_state
    )