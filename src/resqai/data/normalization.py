"""Convert provider-specific earthquake records into the ResQAI format."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def normalize_usgs_features(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize valid USGS features, skipping records with unusable identity/location data."""
    normalized: list[dict[str, Any]] = []
    for feature in payload.get("features", []):
        record = _normalize_feature(feature)
        if record is not None:
            normalized.append(record)
    return normalized


def _normalize_feature(feature: Any) -> dict[str, Any] | None:
    if not isinstance(feature, dict):
        return None
    properties = feature.get("properties")
    geometry = feature.get("geometry")
    if not isinstance(properties, dict) or not isinstance(geometry, dict):
        return None
    coordinates = geometry.get("coordinates")
    event_id = feature.get("id")
    if not isinstance(event_id, str) or not event_id or not _valid_coordinates(coordinates):
        return None
    longitude, latitude, depth = coordinates[:3]
    occurred_at = _iso_timestamp(properties.get("time"))
    if occurred_at is None:
        return None
    return {
        "id": event_id,
        "source": "USGS",
        "source_url": _optional_string(properties.get("url")),
        "disaster_type": "earthquake",
        "title": _optional_string(properties.get("title")) or "Earthquake",
        "location": _optional_string(properties.get("place")) or "Unknown location",
        "latitude": float(latitude),
        "longitude": float(longitude),
        "depth_km": float(depth) if depth is not None else None,
        "magnitude": _optional_float(properties.get("mag")),
        "severity": _optional_string(properties.get("alert")) or "unclassified",
        "occurred_at": occurred_at,
        "updated_at": _iso_timestamp(properties.get("updated")),
        "status": _optional_string(properties.get("status")) or "unknown",
        "tsunami": bool(properties.get("tsunami", False)),
        "felt_reports": _optional_int(properties.get("felt")),
        "data_quality": "partial" if properties.get("mag") is None else "complete",
    }


def _valid_coordinates(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) >= 2
        and all(isinstance(item, (int, float)) for item in value[:2])
        and -180 <= value[0] <= 180
        and -90 <= value[1] <= 90
    )


def _iso_timestamp(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()


def _optional_string(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _optional_float(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def _optional_int(value: Any) -> int | None:
    return int(value) if isinstance(value, int) else None
