"""Command-line interface for AdPages tools."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from .ads_copy import check_google_ads_copy
from .schema import local_business_json_ld
from .utm import build_utm_url


def _key_value_pairs(values: Sequence[str] | None) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for value in values or []:
        if "=" not in value:
            raise argparse.ArgumentTypeError(f"Expected KEY=VALUE, got {value!r}")
        key, item_value = value.split("=", 1)
        key = key.strip()
        item_value = item_value.strip()
        if not key or not item_value:
            raise argparse.ArgumentTypeError(f"Expected non-empty KEY=VALUE, got {value!r}")
        pairs[key] = item_value
    return pairs


def _add_utm_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("utm", help="Build a UTM-tagged URL")
    parser.add_argument("--url", required=True, help="Absolute landing page URL")
    parser.add_argument("--source", required=True, help="UTM source")
    parser.add_argument("--medium", required=True, help="UTM medium")
    parser.add_argument("--campaign", required=True, help="UTM campaign")
    parser.add_argument("--term", help="UTM term")
    parser.add_argument("--content", help="UTM content")
    parser.add_argument("--param", action="append", help="Extra query parameter as KEY=VALUE")


def _add_schema_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("schema", help="Build LocalBusiness JSON-LD")
    parser.add_argument("--name", required=True, help="Business name")
    parser.add_argument("--url", required=True, help="Business website URL")
    parser.add_argument("--type", default="LocalBusiness", dest="business_type", help="Schema.org business type")
    parser.add_argument("--phone", dest="telephone", help="Telephone number")
    parser.add_argument("--street", dest="streetAddress", help="Street address")
    parser.add_argument("--locality", dest="addressLocality", help="City or locality")
    parser.add_argument("--region", dest="addressRegion", help="State or region")
    parser.add_argument("--postal-code", dest="postalCode", help="Postal code")
    parser.add_argument("--country", dest="addressCountry", help="Country code or name")
    parser.add_argument("--description", help="Short business description")
    parser.add_argument("--image", help="Image URL")
    parser.add_argument("--price-range", dest="price_range", help="Price range text")
    parser.add_argument("--same-as", action="append", help="Social/profile URL")
    parser.add_argument("--area-served", action="append", help="Service area")
    parser.add_argument("--opening-hours", action="append", help="Opening hours text")
    parser.add_argument("--latitude", help="Latitude")
    parser.add_argument("--longitude", help="Longitude")


def _add_ads_copy_parser(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    parser = subparsers.add_parser("ads-copy", help="Check Google Ads copy lengths")
    parser.add_argument("--headline", action="append", dest="headlines", help="Responsive search ad headline")
    parser.add_argument("--description", action="append", dest="descriptions", help="Responsive search ad description")
    parser.add_argument("--path1", help="Display URL path 1")
    parser.add_argument("--path2", help="Display URL path 2")
    parser.add_argument("--json", action="store_true", help="Print the full JSON report")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="adpages-tools", description="AdPages marketing utility tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    _add_utm_parser(subparsers)
    _add_schema_parser(subparsers)
    _add_ads_copy_parser(subparsers)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "utm":
        print(
            build_utm_url(
                args.url,
                source=args.source,
                medium=args.medium,
                campaign=args.campaign,
                term=args.term,
                content=args.content,
                extra_params=_key_value_pairs(args.param),
            )
        )
        return 0

    if args.command == "schema":
        address = {
            key: getattr(args, key)
            for key in ("streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry")
            if getattr(args, key)
        }
        geo = None
        if args.latitude and args.longitude:
            geo = {"latitude": args.latitude, "longitude": args.longitude}
        print(
            local_business_json_ld(
                name=args.name,
                url=args.url,
                business_type=args.business_type,
                telephone=args.telephone,
                address=address or None,
                description=args.description,
                image=args.image,
                price_range=args.price_range,
                same_as=args.same_as,
                area_served=args.area_served,
                opening_hours=args.opening_hours,
                geo=geo,
            )
        )
        return 0

    if args.command == "ads-copy":
        report = check_google_ads_copy(
            headlines=args.headlines,
            descriptions=args.descriptions,
            path1=args.path1,
            path2=args.path2,
        )
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            status = "valid" if report["valid"] else "invalid"
            print(f"Google Ads copy is {status}.")
            for issue in report["issues"]:
                print(f"- {issue['field']}: {issue['message']}")
        return 0 if report["valid"] else 1

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

