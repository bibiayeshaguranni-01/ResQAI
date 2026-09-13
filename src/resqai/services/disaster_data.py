"""Application service for retrieving normalized disaster information."""

from __future__ import annotations

from typing import Any

from resqai.api.usgs_earthquakes import fetch_usgs_feed
from resqai.data.normalization import normalize_usgs_features


def get_current_earthquakes(
    *, url: str | None = None, timeout: float | None = None, opener: Any = None
) -> list[dict[str, Any]]:
    """Fetch the USGS feed and return records ready for ResQAI consumers."""
    fetch_kwargs: dict[str, Any] = {"url": url, "timeout": timeout}
    if opener is not None:
        fetch_kwargs["opener"] = opener
    payload = fetch_usgs_feed(**fetch_kwargs)
    return normalize_usgs_features(payload)
