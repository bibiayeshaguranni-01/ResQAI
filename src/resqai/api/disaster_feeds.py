"""HTTP client for disaster feeds that use GeoJSON FeatureCollections."""

from __future__ import annotations

from collections.abc import Callable
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class DisasterFeedError(RuntimeError):
    """Base error for failures while reading a disaster feed."""


class DisasterFeedTimeout(DisasterFeedError):
    """The feed did not respond before the configured timeout."""


class DisasterFeedResponseError(DisasterFeedError):
    """The feed response was not a valid GeoJSON FeatureCollection."""


def fetch_disaster_feed(
    url: str,
    *,
    timeout: float = 10.0,
    opener: Callable[..., Any] = urlopen,
) -> dict[str, Any]:
    """Fetch and validate a GeoJSON disaster feed from any provider."""
    if not url.strip():
        raise ValueError("url must not be empty")
    if timeout <= 0:
        raise ValueError("timeout must be greater than zero")

    request = Request(url, headers={"Accept": "application/geo+json, application/json"})
    try:
        with opener(request, timeout=timeout) as response:
            if getattr(response, "status", 200) != 200:
                raise DisasterFeedError(f"Disaster feed returned HTTP {response.status}")
            payload = json.loads(response.read().decode("utf-8"))
    except TimeoutError as exc:
        raise DisasterFeedTimeout(f"Disaster feed timed out after {timeout:g} seconds") from exc
    except HTTPError as exc:
        raise DisasterFeedError(f"Disaster feed returned HTTP {exc.code}") from exc
    except URLError as exc:
        raise DisasterFeedError(f"Could not reach disaster feed: {exc.reason}") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DisasterFeedResponseError("Disaster feed was not valid UTF-8 JSON") from exc

    if not isinstance(payload, dict) or payload.get("type") != "FeatureCollection":
        raise DisasterFeedResponseError("Disaster feed must be a GeoJSON FeatureCollection")
    if not isinstance(payload.get("features"), list):
        raise DisasterFeedResponseError("Disaster feed must contain a features list")
    return payload