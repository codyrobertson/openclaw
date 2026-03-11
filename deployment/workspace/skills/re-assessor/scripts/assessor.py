#!/usr/bin/env python3
"""
Maricopa County Assessor property lookup.
Scrapes the public website at mcassessor.maricopa.gov.

The REST API documented in their PDF is Cloudflare-protected and requires
browser-level cookies. This script scrapes the server-rendered HTML pages
which work with simple HTTP requests.

Usage:
  # Search properties by address, owner, or APN
  python3 assessor.py search "4610 E Flower St"
  python3 assessor.py search "Smith John"
  python3 assessor.py search "127-03-059"

  # Get parcel details by APN (strips dashes automatically)
  python3 assessor.py parcel 127-03-059

  # Export search results as CSV
  python3 assessor.py export "85018"
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse


def _setup_ssl():
    """Ensure SSL cert bundle is found on macOS (system certs may be outdated)."""
    import ssl
    try:
        import certifi
        ca = certifi.where()
    except ImportError:
        ca = "/etc/ssl/cert.pem"
    # Always override with certifi/fresh certs — system cert.pem may be stale
    os.environ["SSL_CERT_FILE"] = ca
    os.environ["CURL_CA_BUNDLE"] = ca
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=ca)

_setup_ssl()

BASE_URL = "https://mcassessor.maricopa.gov"


def _fetch_html(path):
    """Fetch an HTML page from the assessor website."""
    url = f"{BASE_URL}{path}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        return None


def _strip_tags(html):
    """Remove HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', html).strip()


def _clean_apn(apn):
    """Remove dashes, dots, spaces from APN."""
    return re.sub(r'[\-\.\s]', '', apn)


def search_property(query):
    """Search for properties via the CSV export endpoint (no JS needed).
    Returns list of dicts with APN, Owner, Address, City, Zip, Subdivision, MCR, STR, PropertyType."""
    import csv
    encoded = urllib.parse.quote(query)
    csv_text = _fetch_html(f"/mcs/export/property/?q={encoded}")
    if not csv_text:
        return []
    # First line is "Total Results: N", data starts at line 2 (header) + line 3+
    lines = csv_text.strip().split('\n')
    if len(lines) < 3:
        return []
    # Skip the "Total Results" line
    reader = csv.DictReader(lines[1:])
    results = []
    for row in reader:
        results.append({
            "apn": row.get("APN", ""),
            "owner": row.get("Owner", ""),
            "address": f"{row.get('Address', '')}, {row.get('City', '')} {row.get('Zip', '')}".strip(", "),
            "subdivision": row.get("Subdivison Name", row.get("Subdivision Name", "")),
            "mcr": row.get("MCR", ""),
            "str": row.get("S/T/R", ""),
            "property_type": row.get("Property Type", ""),
            "rental": row.get("Rental", ""),
        })
    return results


def parcel_details(apn):
    """Get detailed parcel information by APN."""
    clean = _clean_apn(apn)
    html = _fetch_html(f"/mcs/?q={clean}&mod=pd")
    if not html:
        return None
    return _parse_parcel_detail(html)


def _parse_parcel_detail(html):
    """Parse the parcel detail page."""
    result = {}

    # Extract APN from heading
    apn_match = re.search(r'<h3[^>]*>\s*(\d{3}-\d{2}-\d{3}[A-Z]?)\s*</h3>', html)
    if apn_match:
        result["apn"] = apn_match.group(1)

    # Extract property type
    type_match = re.search(r'<h3[^>]*>\s*(Residential|Commercial|Vacant|Agricultural|Exempt)\s+Parcel\s*</h3>', html, re.IGNORECASE)
    if type_match:
        result["property_type"] = type_match.group(1)

    # Extract from the description paragraph: "located at <a>ADDRESS</a>...owner is OWNER...subdivision"
    desc_match = re.search(r'located at.*?target="_blank">([^<]+)</a>', html, re.DOTALL)
    if desc_match:
        result["address"] = desc_match.group(1).strip()

    owner_match = re.search(r'current owner is\s+(.*?)\.', html, re.DOTALL)
    if owner_match:
        result["owner"] = _strip_tags(owner_match.group(1)).strip()

    # MCR link right after "MCR" text
    mcr_match = re.search(r'MCR\s*<a[^>]*>(\d+)</a>', html)
    if mcr_match:
        result["mcr"] = mcr_match.group(1)

    # Parse key-value pairs from the detail sections
    # The site uses pairs like: <div class="label">Key</div> <div/a/link>Value</div/a>
    # We look for short text-only divs followed by value divs
    kv_fields = {
        'MCR #': 'mcr',
        'Description': 'description',
        'Lot Size': 'lot_size',
        'Lot #': 'lot_num',
        'High School District': 'high_school_district',
        'Elementary School District': 'elementary_school_district',
        'Local Jurisdiction': 'local_jurisdiction',
        'S/T/R': 'str',
        'Market Area/Neighborhood': 'market_area',
        'Mailing Address': 'mailing_address',
        'Deed Number': 'deed_number',
        'Last Deed Date': 'last_deed_date',
        'Sale Date': 'sale_date',
        'Sale Price': 'sale_price',
    }
    for field_label, field_key in kv_fields.items():
        # Find the label, then grab the next sibling element's text content
        pattern = re.escape(field_label) + r'</(?:div|span)>\s*<(?:div|span|a)[^>]*>\s*([^<]+)'
        match = re.search(pattern, html)
        if match:
            value = match.group(1).strip()
            if value and value not in ('', 'n/a'):
                result[field_key] = value

    # Check for "Parcel not found" error
    if 'Parcel not found' in html:
        return None

    return result if result else None


def export_search(query, search_type="property"):
    """Export search results as CSV text."""
    encoded = urllib.parse.quote(query)
    html = _fetch_html(f"/mcs/export/{search_type}/?q={encoded}")
    return html


def print_json(data):
    """Pretty-print JSON data."""
    if data is None:
        print("{}")
        return
    print(json.dumps(data, indent=2, default=str))


def print_search_summary(results):
    """Print a human-readable summary of search results."""
    if not results:
        print("No results found.")
        return

    print(f"\n{'=' * 70}")
    print(f"  PROPERTY SEARCH — {len(results)} found")
    print(f"{'=' * 70}\n")

    for i, item in enumerate(results, 1):
        apn = item.get("apn", "")
        owner = item.get("owner", "")
        addr = item.get("address", "")
        ptype = item.get("property_type", "")
        print(f"  {i}. APN: {apn}")
        if addr:
            print(f"     Address: {addr}")
        if owner:
            print(f"     Owner: {owner}")
        if ptype:
            print(f"     Type: {ptype}")
        print()


def print_parcel_summary(data):
    """Print a human-readable parcel detail summary."""
    if not data:
        print("Parcel not found.")
        return

    print(f"\n{'=' * 60}")
    print(f"  PARCEL DETAIL — {data.get('apn', 'Unknown')}")
    print(f"{'=' * 60}\n")

    for key, value in data.items():
        label = key.replace('_', ' ').title()
        print(f"  {label}: {value}")
    print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Maricopa County Assessor property lookup")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search
    search_p = subparsers.add_parser("search", help="Search by address, owner, or APN")
    search_p.add_argument("query", help="Search query")
    search_p.add_argument("--format", choices=["json", "summary"], default="summary")

    # Parcel detail
    parcel_p = subparsers.add_parser("parcel", help="Get parcel details by APN")
    parcel_p.add_argument("apn", help="Assessor Parcel Number (e.g. 127-03-059)")
    parcel_p.add_argument("--format", choices=["json", "summary"], default="summary")

    # Export
    export_p = subparsers.add_parser("export", help="Export search results as CSV")
    export_p.add_argument("query", help="Search query")
    export_p.add_argument("--type", dest="search_type", default="property",
                          choices=["property", "bpp", "mh", "rental", "sub"],
                          help="Search type to export")

    args = parser.parse_args()

    if args.command == "search":
        results = search_property(args.query)
        if args.format == "json":
            print_json(results)
        else:
            print_search_summary(results)

    elif args.command == "parcel":
        data = parcel_details(args.apn)
        if args.format == "json":
            print_json(data)
        else:
            print_parcel_summary(data)

    elif args.command == "export":
        csv_data = export_search(args.query, args.search_type)
        if csv_data:
            print(csv_data)
        else:
            print("Export failed.", file=sys.stderr)


if __name__ == "__main__":
    main()
