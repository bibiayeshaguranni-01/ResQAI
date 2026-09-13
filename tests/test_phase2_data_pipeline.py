"""Focused tests for the Phase 2 USGS data pipeline."""

from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from resqai.api.usgs_earthquakes import (
    EarthquakeApiError,
    EarthquakeApiTimeout,
    EarthquakeResponseError,
    fetch_usgs_feed,
)
from resqai.data.normalization import normalize_usgs_features
from resqai.services.disaster_data import get_current_earthquakes


def sample_payload() -> dict:
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "us-test-1",
                "properties": {
                    "mag": 5.2,
                    "place": "10 km north of Testville",
                    "time": 1700000000000,
                    "updated": 1700000005000,
                    "url": "https://example.test/event/us-test-1",
                    "alert": None,
                    "status": "reviewed",
                    "tsunami": 0,
                    "felt": 12,
                    "title": "M 5.2 - 10 km north of Testville",
                },
                "geometry": {"type": "Point", "coordinates": [12.5, 45.25, 8.0]},
            }
        ],
    }


class FakeResponse:
    status = 200

    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class Phase2PipelineTests(unittest.TestCase):
    def test_normalizes_usgs_feature_into_resqai_format(self) -> None:
        records = normalize_usgs_features(sample_payload())

        self.assertEqual(records[0]["id"], "us-test-1")
        self.assertEqual(records[0]["disaster_type"], "earthquake")
        self.assertEqual(records[0]["latitude"], 45.25)
        self.assertEqual(records[0]["longitude"], 12.5)
        self.assertEqual(records[0]["severity"], "unclassified")
        self.assertEqual(records[0]["felt_reports"], 12)

    def test_service_fetches_and_normalizes_data(self) -> None:
        records = get_current_earthquakes(opener=lambda *args, **kwargs: FakeResponse(sample_payload()))

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["source"], "USGS")

    def test_malformed_top_level_response_is_rejected(self) -> None:
        with self.assertRaises(EarthquakeResponseError):
            fetch_usgs_feed(opener=lambda *args, **kwargs: FakeResponse({"type": "Feature"}))

    def test_http_failure_is_reported(self) -> None:
        response = FakeResponse(sample_payload())
        response.status = 503

        with self.assertRaises(EarthquakeApiError):
            fetch_usgs_feed(opener=lambda *args, **kwargs: response)

    def test_timeout_is_reported(self) -> None:
        def timeout_opener(*args: object, **kwargs: object) -> None:
            raise TimeoutError

        with self.assertRaises(EarthquakeApiTimeout):
            fetch_usgs_feed(opener=timeout_opener)

    def test_invalid_timeout_configuration_is_rejected(self) -> None:
        with patch.dict("os.environ", {"RESQAI_API_TIMEOUT_SECONDS": "not-a-number"}):
            with self.assertRaises(ValueError):
                fetch_usgs_feed(opener=lambda *args, **kwargs: FakeResponse(sample_payload()))

    def test_feature_with_missing_identity_or_coordinates_is_skipped(self) -> None:
        payload = sample_payload()
        payload["features"].append({"properties": {}, "geometry": {"coordinates": [0, 0]}})

        self.assertEqual(len(normalize_usgs_features(payload)), 1)


if __name__ == "__main__":
    unittest.main()