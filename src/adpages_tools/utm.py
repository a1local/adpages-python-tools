"""UTM URL helpers."""

from __future__ import annotations

from collections.abc import Mapping
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


UTM_FIELDS = ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content")


def _clean(value: object, field_name: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} must not be empty")
    return text


def build_utm_url(
    base_url: str,
    *,
    source: str,
    medium: str,
    campaign: str,
    term: str | None = None,
    content: str | None = None,
    extra_params: Mapping[str, object] | None = None,
    preserve_existing: bool = True,
) -> str:
    """Return a URL with UTM parameters added.

    Existing query parameters are preserved by default. Existing UTM parameters
    are replaced by the provided values so campaign links stay explicit.
    """

    url = _clean(base_url, "base_url")
    parts = urlsplit(url)
    if not parts.scheme or not parts.netloc:
        raise ValueError("base_url must be an absolute URL with scheme and host")

    query_items: list[tuple[str, str]] = []
    if preserve_existing:
        query_items.extend(
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if key not in UTM_FIELDS
        )

    query_items.extend(
        [
            ("utm_source", _clean(source, "source")),
            ("utm_medium", _clean(medium, "medium")),
            ("utm_campaign", _clean(campaign, "campaign")),
        ]
    )

    if term is not None:
        query_items.append(("utm_term", _clean(term, "term")))
    if content is not None:
        query_items.append(("utm_content", _clean(content, "content")))

    if extra_params:
        for key, value in extra_params.items():
            clean_key = _clean(key, "extra parameter key")
            if clean_key in UTM_FIELDS:
                raise ValueError(f"extra_params must not override {clean_key}")
            query_items.append((clean_key, _clean(value, clean_key)))

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            urlencode(query_items),
            parts.fragment,
        )
    )

