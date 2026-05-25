"""Google Ads copy length helpers."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any
import unicodedata


GOOGLE_ADS_LIMITS = {
    "headline": 30,
    "description": 90,
    "path": 15,
}


def google_ads_character_count(text: str) -> int:
    """Count text for Google Ads style limits.

    East Asian full-width and wide characters count as 2. Other characters count
    as 1. This mirrors Google's documented double-width language note.
    """

    total = 0
    for char in str(text):
        total += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return total


def _copy_values(values: Iterable[object] | None) -> list[str]:
    if values is None:
        return []
    return [str(value).strip() for value in values if str(value).strip()]


def _field_result(field: str, text: str, limit: int, index: int | None = None) -> dict[str, Any]:
    length = google_ads_character_count(text)
    result = {
        "field": field,
        "text": text,
        "limit": limit,
        "length": length,
        "remaining": limit - length,
        "ok": length <= limit,
    }
    if index is not None:
        result["index"] = index
    return result


def check_google_ads_copy(
    *,
    headlines: Iterable[object] | None = None,
    descriptions: Iterable[object] | None = None,
    path1: object | None = None,
    path2: object | None = None,
    min_headlines: int = 3,
    min_descriptions: int = 2,
) -> dict[str, Any]:
    """Check responsive search ad copy against length and minimum-count rules."""

    headline_values = _copy_values(headlines)
    description_values = _copy_values(descriptions)
    path_values = [str(value).strip() for value in (path1, path2) if value is not None and str(value).strip()]

    checks: list[dict[str, Any]] = []
    checks.extend(
        _field_result("headline", text, GOOGLE_ADS_LIMITS["headline"], index)
        for index, text in enumerate(headline_values, start=1)
    )
    checks.extend(
        _field_result("description", text, GOOGLE_ADS_LIMITS["description"], index)
        for index, text in enumerate(description_values, start=1)
    )
    checks.extend(
        _field_result("path", text, GOOGLE_ADS_LIMITS["path"], index)
        for index, text in enumerate(path_values, start=1)
    )

    issues: list[dict[str, str]] = []
    if len(headline_values) < min_headlines:
        issues.append(
            {
                "severity": "error",
                "field": "headline",
                "message": f"Add at least {min_headlines} headlines.",
            }
        )
    if len(description_values) < min_descriptions:
        issues.append(
            {
                "severity": "error",
                "field": "description",
                "message": f"Add at least {min_descriptions} descriptions.",
            }
        )
    for check in checks:
        if not check["ok"]:
            issues.append(
                {
                    "severity": "error",
                    "field": check["field"],
                    "message": f"{check['field']} {check.get('index', '')} is {abs(check['remaining'])} characters over.",
                }
            )

    return {
        "valid": not issues,
        "limits": dict(GOOGLE_ADS_LIMITS),
        "checks": checks,
        "issues": issues,
    }

