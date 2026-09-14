"""Tests for the Phase 3 historical dataset pipeline."""

from __future__ import annotations

from io import StringIO
import unittest

import pandas as pd

from resqai.data.historical_storm_events import (
    IMPACT_COLUMNS,
    TARGET_COLUMN,
    clean_storm_events,
    inspect_storm_events,
    load_storm_events,
    prepare_storm_events,
)


def sample_storm_events() -> pd.DataFrame:
    rows = []
    for event_id in range(12):
        rows.append(
            {
                "EVENT_ID": event_id,
                "EVENT_TYPE": "Thunderstorm Wind" if event_id % 2 else "Flood",
                "STATE": "TEST",
                "YEAR": 2023,
                "MONTH_NAME": "January",
                "CZ_TYPE": "C",
                "MAGNITUDE": float(event_id),
                "MAGNITUDE_TYPE": "MG",
                "BEGIN_RANGE": 1.0,
                "BEGIN_AZIMUTH": "N",
                "BEGIN_LAT": 35.0,
                "BEGIN_LON": -90.0,
                "BEGIN_DATE_TIME": "01-JAN-23 01:00:00",
                "END_DATE_TIME": "01-JAN-23 03:00:00",
                "BEGIN_YEARMONTH": 202301,
                "DEATHS_DIRECT": 1 if event_id < 4 else 0,
                "DEATHS_INDIRECT": 0,
                "INJURIES_DIRECT": 0,
                "INJURIES_INDIRECT": 0,
            }
        )
    return pd.DataFrame(rows)


class HistoricalStormEventsTests(unittest.TestCase):
    def test_load_storm_events_reads_csv_text(self) -> None:
        data = load_storm_events(StringIO("EVENT_ID,EVENT_TYPE\n1,Flood\n"))

        self.assertEqual(list(data["EVENT_TYPE"]), ["Flood"])

    def test_inspection_reports_missing_values_duplicates_and_invalid_values(self) -> None:
        data = sample_storm_events()
        data.loc[0, "BEGIN_LAT"] = 100
        data.loc[1, "MAGNITUDE"] = None
        data = pd.concat([data, data.iloc[[2]]], ignore_index=True)

        report = inspect_storm_events(data)

        self.assertEqual(report.row_count, 13)
        self.assertEqual(report.duplicate_rows, 1)
        self.assertEqual(report.duplicate_event_ids, 1)
        self.assertEqual(report.missing_values["MAGNITUDE"], 1)
        self.assertEqual(report.invalid_values["BEGIN_LAT"], 1)

    def test_cleaning_removes_duplicate_ids_and_negative_impact_values(self) -> None:
        data = sample_storm_events()
        data.loc[0, "DEATHS_DIRECT"] = -1
        data = pd.concat([data, data.iloc[[1]]], ignore_index=True)

        cleaned = clean_storm_events(data)

        self.assertEqual(len(cleaned), 11)
        self.assertTrue((cleaned[list(IMPACT_COLUMNS)] >= 0).all().all())

    def test_preparation_splits_and_preprocesses_without_target_columns(self) -> None:
        prepared = prepare_storm_events(sample_storm_events(), test_size=0.25)

        self.assertEqual(prepared.X_train.shape[0], 9)
        self.assertEqual(prepared.X_test.shape[0], 3)
        self.assertEqual(prepared.y_train.name, TARGET_COLUMN)
        self.assertNotIn(TARGET_COLUMN, prepared.feature_columns)
        self.assertFalse(set(IMPACT_COLUMNS).intersection(prepared.feature_columns))
        self.assertEqual(prepared.X_train.shape[1], prepared.X_test.shape[1])