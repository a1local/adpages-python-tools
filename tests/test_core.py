from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from adpages_tools import build_utm_url, check_google_ads_copy, local_business_json_ld  # noqa: E402


class AdPagesToolsTests(unittest.TestCase):
    def test_build_utm_url_preserves_existing_query_and_replaces_utm(self) -> None:
        url = build_utm_url(
            "https://example.com/page?ref=nav&utm_source=old#contact",
            source="google",
            medium="cpc",
            campaign="emergency-plumber",
            content="rsa-a",
        )

        self.assertEqual(
            url,
            "https://example.com/page?ref=nav&utm_source=google&utm_medium=cpc&utm_campaign=emergency-plumber&utm_content=rsa-a#contact",
        )

    def test_build_utm_url_requires_absolute_url(self) -> None:
        with self.assertRaises(ValueError):
            build_utm_url("/relative", source="google", medium="cpc", campaign="test")

    def test_local_business_json_ld_outputs_expected_schema(self) -> None:
        payload = json.loads(
            local_business_json_ld(
                name="Example Plumbing",
                url="https://example.com",
                telephone="+61 8 5550 1000",
                address={
                    "streetAddress": "10 Hay Street",
                    "addressLocality": "Perth",
                    "addressRegion": "WA",
                    "postalCode": "6000",
                    "addressCountry": "AU",
                },
                area_served=["Perth"],
                geo={"latitude": "-31.9523", "longitude": "115.8613"},
            )
        )

        self.assertEqual(payload["@context"], "https://schema.org")
        self.assertEqual(payload["@type"], "LocalBusiness")
        self.assertEqual(payload["address"]["@type"], "PostalAddress")
        self.assertEqual(payload["geo"]["@type"], "GeoCoordinates")
        self.assertEqual(payload["areaServed"], ["Perth"])

    def test_google_ads_copy_checker_flags_limits_and_counts_double_width(self) -> None:
        report = check_google_ads_copy(
            headlines=["Emergency Plumber Perth", "Same-Day Hot Water Repairs", "これは長い見出しテキストですこれは長い"],
            descriptions=[
                "Licensed Perth plumbers for urgent repairs, leaks, blocked drains and hot water.",
                "Call now for fast help from a local team with clear pricing.",
            ],
            path1="plumber",
            path2="perth",
        )

        self.assertFalse(report["valid"])
        self.assertTrue(any(issue["field"] == "headline" for issue in report["issues"]))

    def test_cli_utm_command(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "adpages_tools.cli",
                "utm",
                "--url",
                "https://example.com",
                "--source",
                "google",
                "--medium",
                "cpc",
                "--campaign",
                "test",
            ],
            cwd=ROOT,
            env={"PYTHONPATH": str(SRC)},
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertEqual(
            result.stdout.strip(),
            "https://example.com?utm_source=google&utm_medium=cpc&utm_campaign=test",
        )


if __name__ == "__main__":
    unittest.main()

