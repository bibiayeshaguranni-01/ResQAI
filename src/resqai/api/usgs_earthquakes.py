"""HTTP client and validation for the USGS earthquake GeoJSON feed."""

from __future__ import annotations

from collections.abc import Callable
import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
DEFAULT_TIMEOUT_SECONDS = 10.0


class EarthquakeApiError(RuntimeError):
    """Base error for failures while reading the USGS feed."""


class EarthquakeApiTimeout(EarthquakeApiError):
    """The feed did not respond before the configured timeout."""


class EarthquakeResponseError(EarthquakeApiError):
    """The feed response was not valid USGS GeoJSON."""


def feed_settings() -> tuple[str, float]:
    """Read the feed URL and timeout from environment variables."""
    url = os.getenv("RESQAI_USGS_FEED_URL", DEFAULT_USGS_URL).strip()
    timeout_text = os.getenv("RESQAI_API_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS))
    try:
        timeout = float(timeout_text)
    except ValueError as exc:
        raise ValueError("RESQAI_API_TIMEOUT_SECONDS must be a positive number") from exc
    if not url:
        raise ValueError("RESQAI_USGS_FEED_URL must not be empty")
    if timeout <= 0:
        raise ValueError("RESQAI_API_TIMEOUT_SECONDS must be greater than zero")
    return url, timeout


def fetch_usgs_feed(
    url: str | None = None,
    timeout: float | None = None,
    opener: Callable[..., Any] = urlopen,
) -> dict[str, Any]:
    """Fetch and validate one USGS GeoJSON response."""
    configured_url, configured_timeout = feed_settings()
    request_url = url or configured_url
    request_timeout = timeout or configured_timeout
    request = Request(request_url, headers={"Accept": "application/geo+json, application/json"})
    try:
        with opener(request, timeout=request_timeout) as response:
            if getattr(response, "status", 200) != 200:
                raise EarthquakeApiError(f"USGS feed returned HTTP {response.status}")
            payload = json.loads(response.read().decode("utf-8"))
    except TimeoutError as exc:
        raise EarthquakeApiTimeout(f"USGS feed timed out after {request_timeout:g} seconds") from exc
    except HTTPError as exc:
        raise EarthquakeApiError(f"USGS feed returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise EarthquakeApiError(f"Could not reach USGS feed: {exc.reason}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EarthquakeResponseError("USGS feed was not valid UTF-8 JSON") from exc

    validate_feed(payload)
    return payload


def validate_feed(payload: Any) -> None:
    """Validate the required top-level GeoJSON structure."""
    if not isinstance(payload, dict) or payload.get("type") != "FeatureCollection":
        raise EarthquakeResponseError("USGS response must be a GeoJSON FeatureCollection")
    features = payload.get("features")
    if not isinstance(features, list):
        raise EarthquakeResponseError("USGS response must contain a features list")
