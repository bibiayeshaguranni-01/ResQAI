"""Application service for retrieving normalized disaster information."""

from __future__ import annotations

from typing import Any

from resqai.api.disaster_feeds import fetch_disaster_feed
from resqai.api.usgs_earthquakes import fetch_usgs_feed
from resqai.data.normalization import normalize_disaster_features, normalize_usgs_features


def get_current_disasters(
    *,
    url: str,
    source: str,
    disaster_type: str,
    timeout: float = 10.0,
    opener: Any = None,
) -> list[dict[str, Any]]:
    """Fetch and normalize records from any GeoJSON disaster provider."""
    fetch_kwargs: dict[str, Any] = {"timeout": timeout}
    if opener is not None:
        fetch_kwargs["opener"] = opener
    payload = fetch_disaster_feed(url, **fetch_kwargs)
    return normalize_disaster_features(payload, source=source, disaster_type=disaster_type)


def get_current_earthquakes(
    *, url: str | None = None, timeout: float | None = None, opener: Any = None
) -> list[dict[str, Any]]:
    """Fetch the USGS feed and return records ready for ResQAI consumers."""
    fetch_kwargs: dict[str, Any] = {"url": url, "timeout": timeout}
    if opener is not None:
        fetch_kwargs["opener"] = opener
    payload = fetch_usgs_feed(**fetch_kwargs)
    return normalize_usgs_features(payload)
