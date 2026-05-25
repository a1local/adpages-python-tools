"""LocalBusiness JSON-LD helpers."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any


def _clean(value: object, field_name: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} must not be empty")
    return text


def _list_or_none(values: Iterable[object] | None) -> list[str] | None:
    if values is None:
        return None
    result = [_clean(value, "list item") for value in values]
    return result or None


def _postal_address(address: Mapping[str, object] | str | None) -> dict[str, Any] | str | None:
    if address is None:
        return None
    if isinstance(address, str):
        return _clean(address, "address")

    allowed = {
        "streetAddress",
        "addressLocality",
        "addressRegion",
        "postalCode",
        "addressCountry",
    }
    payload = {
        key: _clean(value, key)
        for key, value in address.items()
        if key in allowed and value is not None and str(value).strip()
    }
    if not payload:
        return None
    payload["@type"] = "PostalAddress"
    return payload


def build_local_business_schema(
    *,
    name: str,
    url: str,
    business_type: str = "LocalBusiness",
    telephone: str | None = None,
    address: Mapping[str, object] | str | None = None,
    description: str | None = None,
    image: str | None = None,
    price_range: str | None = None,
    same_as: Iterable[str] | None = None,
    area_served: Iterable[str] | None = None,
    opening_hours: Iterable[str] | None = None,
    geo: Mapping[str, object] | None = None,
) -> dict[str, Any]:
    """Build a Schema.org LocalBusiness-compatible JSON-LD dictionary."""

    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": _clean(business_type, "business_type"),
        "name": _clean(name, "name"),
        "url": _clean(url, "url"),
    }

    optional_values: dict[str, Any] = {
        "telephone": telephone,
        "address": _postal_address(address),
        "description": description,
        "image": image,
        "priceRange": price_range,
        "sameAs": _list_or_none(same_as),
        "areaServed": _list_or_none(area_served),
        "openingHours": _list_or_none(opening_hours),
    }

    if geo:
        lat = geo.get("latitude")
        lon = geo.get("longitude")
        if lat is not None and lon is not None:
            optional_values["geo"] = {
                "@type": "GeoCoordinates",
                "latitude": _clean(lat, "latitude"),
                "longitude": _clean(lon, "longitude"),
            }

    for key, value in optional_values.items():
        if value is None:
            continue
        if isinstance(value, str) and not value.strip():
            continue
        schema[key] = value

    return schema


def local_business_json_ld(**kwargs: Any) -> str:
    """Build pretty JSON-LD for a LocalBusiness schema."""

    return json.dumps(build_local_business_schema(**kwargs), indent=2, sort_keys=False)

