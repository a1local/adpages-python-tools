# AdPages Tools for Python

Dependency-free Python utilities for small landing-page and local-service marketing workflows.

This package is designed as a practical PyPI/GitHub/tutorial surface for AdPages: useful enough on its own, close to local-service landing page work, and simple to maintain.

## What it includes

- UTM URL builder for campaign links.
- LocalBusiness JSON-LD builder for local landing pages.
- Google Ads responsive search ad copy length checker.
- Small CLI for quick terminal use.

The Google Ads copy checker uses the current common responsive search ad limits: headlines up to 30 characters, descriptions up to 90 characters, and display URL paths up to 15 characters each. Recheck the official Google Ads docs before publishing a public release.

## Install

From this folder during development:

```bash
python3 -m pip install -e .
```

After a future PyPI release:

```bash
python3 -m pip install adpages-tools
```

## Python Usage

Build a tagged campaign URL:

```python
from adpages_tools import build_utm_url

url = build_utm_url(
    "https://example.com/plumber-perth",
    source="google",
    medium="cpc",
    campaign="emergency-plumber",
    content="rsa-a",
)
print(url)
```

Create LocalBusiness JSON-LD:

```python
from adpages_tools import local_business_json_ld

json_ld = local_business_json_ld(
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
    area_served=["Perth", "Fremantle"],
)
print(json_ld)
```

Check ad copy:

```python
from adpages_tools import check_google_ads_copy

report = check_google_ads_copy(
    headlines=["Emergency Plumber Perth", "Same-Day Hot Water Repairs", "Book a Local Plumber"],
    descriptions=[
        "Licensed Perth plumbers for urgent repairs, leaks, blocked drains and hot water.",
        "Call now for fast help from a local team with clear pricing.",
    ],
    path1="plumber",
    path2="perth",
)
print(report["valid"])
```

## CLI Examples

```bash
adpages-tools utm \
  --url https://example.com/plumber-perth \
  --source google \
  --medium cpc \
  --campaign emergency-plumber \
  --content rsa-a
```

```bash
adpages-tools schema \
  --name "Example Plumbing" \
  --url https://example.com \
  --phone "+61 8 5550 1000" \
  --locality Perth \
  --region WA \
  --country AU \
  --area-served Perth \
  --area-served Fremantle
```

```bash
adpages-tools ads-copy \
  --headline "Emergency Plumber Perth" \
  --headline "Same-Day Hot Water Repairs" \
  --headline "Book a Local Plumber" \
  --description "Licensed Perth plumbers for urgent repairs, leaks, blocked drains and hot water." \
  --description "Call now for fast help from a local team with clear pricing." \
  --path1 plumber \
  --path2 perth \
  --json
```

## Local Checks

Run the package-local check:

```bash
npm run check
```

Or run the underlying Python commands directly:

```bash
python3 scripts/check.py
python3 -m unittest discover -s tests
python3 -m compileall -q src tests scripts
```

The checker verifies that:

- `pyproject.toml` parses.
- Python modules compile.
- Unit tests pass.
- Source files do not contain network-call patterns or secret placeholders.
- README and privacy notes state that there are no external API calls, hidden tracking, or hosted backend.

## Publishing Position

This should be published as a small utility package for:

- PyPI discovery via campaign URL and LocalBusiness schema workflows.
- GitHub examples and tutorials.
- Developer docs that point back to AdPages landing-page QA tools.

It makes no external API calls, has no hidden tracking, does not collect data, and has no hosted backend.

## Publish Blockers

- Confirm PyPI package ownership for `adpages-tools`.
- Finalize license text and support URLs.
- Add repository, changelog, and issue tracker URLs.
- Build and inspect wheel and sdist artifacts with `python3 -m build` and `twine check`.
- Validate the CLI after installing from a built wheel in a clean virtual environment.
- Recheck Google Ads copy limits against official docs before release.
