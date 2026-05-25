"""AdPages utility helpers for local landing-page marketing workflows."""

from .ads_copy import GOOGLE_ADS_LIMITS, check_google_ads_copy
from .schema import build_local_business_schema, local_business_json_ld
from .utm import build_utm_url

__all__ = [
    "GOOGLE_ADS_LIMITS",
    "build_local_business_schema",
    "build_utm_url",
    "check_google_ads_copy",
    "local_business_json_ld",
]

__version__ = "0.1.0"

