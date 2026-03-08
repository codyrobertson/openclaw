#!/usr/bin/env python3
"""
Maricopa County Assessor API client.
Wraps the public REST API at mcassessor.maricopa.gov.

Auth: Requires AUTHORIZATION header with API token.
      Set env var MC_ASSESSOR_TOKEN or pass --token.

Usage:
  # Search properties by address, owner, or APN
  python3 assessor.py search "4610 E Flower St"

  # Get full parcel details by APN
  python3 assessor.py parcel 163-32-037

  # Get property info
  python3 assessor.py propertyinfo 163-32-037

  # Get property address
  python3 assessor.py address 163-32-037

  # Get valuations (5 year history)
  python3 assessor.py valuations 163-32-037

  # Get residential details
  python3 assessor.py residential 163-32-037

  # Get owner details
  python3 assessor.py owner 163-32-037

  # Search subdivisions
  python3 assessor.py subdivisions "Arcadia"

  # Search rentals
  python3 assessor.py rentals "85018"

  # Get MCR data
  python3 assessor.py mcr 12345

  # Section/Township/Range lookup
  python3 assessor.py str 1-1N-3E

  # Get parcel maps
  python3 assessor.py maps 163-32-037

  # Full property report (all endpoints combined)
  python3 assessor.py report 163-32-037
"""

import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse

def _setup_ssl():
    """Ensure SSL cert bundle is found on macOS (Homebrew Python often missing default)."""
    try:
        import certifi
        ca = certifi.where()
    except ImportError:
        ca = "/etc/ssl/cert.pem"
    os.environ.setdefault("SSL_CERT_FILE", ca)
    import ssl
    if not os.path.exists(ssl.get_default_verify_paths().cafile or ""):
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=ca)

_setup_ssl()

BASE_URL = "https://mcassessor.maricopa.gov"

def get_token():
    token = os.environ.get("MC_ASSESSOR_TOKEN", "")
    return token

def api_get(path, token=None):
    """Make authenticated GET request to the Assessor API."""
    url = f"{BASE_URL}{path}"
    tok = token or get_token()
    headers = {"User-Agent": ""}
    if tok:
        headers["AUTHORIZATION"] = tok
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        if body:
            print(body, file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        return None

def search_property(query, page=None, token=None):
    """Search all property types. Returns JSON with Real Property, BPP, MH, Rentals, Subdivisions."""
    encoded = urllib.parse.quote(query)
    path = f"/search/property/?q={encoded}"
    if page:
        path += f"&page={page}"
    return api_get(path, token)

def search_subdivisions(query, token=None):
    """Search subdivision names."""
    encoded = urllib.parse.quote(query)
    return api_get(f"/search/sub/?q={encoded}", token)

def search_rentals(query, page=None, token=None):
    """Search rental registrations."""
    encoded = urllib.parse.quote(query)
    path = f"/search/rental/?q={encoded}"
    if page:
        path += f"&page={page}"
    return api_get(path, token)

def parcel_details(apn, token=None):
    """Get all available parcel data."""
    return api_get(f"/parcel/{apn}", token)

def property_info(apn, token=None):
    """Get property-specific information."""
    return api_get(f"/parcel/{apn}/propertyinfo", token)

def property_address(apn, token=None):
    """Get property address."""
    return api_get(f"/parcel/{apn}/address", token)

def valuation_details(apn, token=None):
    """Get 5-year valuation history."""
    return api_get(f"/parcel/{apn}/valuations", token)

def residential_details(apn, token=None):
    """Get residential parcel details."""
    return api_get(f"/parcel/{apn}/residential-details", token)

def owner_details(apn, token=None):
    """Get owner information."""
    return api_get(f"/parcel/{apn}/owner-details", token)

def mcr_data(mcr, page=None, token=None):
    """Get MCR data."""
    path = f"/parcel/mcr/{mcr}"
    if page:
        path += f"?page={page}"
    return api_get(path, token)

def str_data(str_val, page=None, token=None):
    """Get Section/Township/Range data."""
    path = f"/parcel/str/{str_val}"
    if page:
        path += f"?page={page}"
    return api_get(path, token)

def parcel_maps(apn, token=None):
    """Get parcel map file names."""
    return api_get(f"/mapid/parcel/{apn}", token)

def book_maps(book, map_num, token=None):
    """Get book/map file names."""
    return api_get(f"/mapid/bookmap/{book}/{map_num}", token)

def mcr_maps(mcr, token=None):
    """Get MCR map file names."""
    return api_get(f"/mapid/mcr/{mcr}", token)

def bpp_account(acct_type, acct, year=None, token=None):
    """Get business personal property account details. type: c/m/l"""
    path = f"/bpp/{acct_type}/{acct}"
    if year:
        path += f"/{year}"
    return api_get(path, token)

def mobile_home(acct, token=None):
    """Get mobile home account details."""
    return api_get(f"/mh/{acct}", token)

def mobile_home_vin(vin, token=None):
    """Get account number for a mobile home VIN."""
    return api_get(f"/mh/vin/{vin}", token)

def full_report(apn, token=None):
    """Combine all parcel endpoints into a single report."""
    report = {}
    for name, fn in [
        ("parcel", parcel_details),
        ("propertyinfo", property_info),
        ("address", property_address),
        ("valuations", valuation_details),
        ("residential", residential_details),
        ("owner", owner_details),
        ("maps", parcel_maps),
    ]:
        result = fn(apn, token)
        if result is not None:
            report[name] = result
    return report

def print_json(data):
    """Pretty-print JSON data."""
    if data is None:
        print("{}")
        return
    print(json.dumps(data, indent=2, default=str))

def print_search_summary(data):
    """Print a human-readable summary of property search results."""
    if not data:
        print("No results found.")
        return

    # Handle different result structures
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, list) and val:
                print(f"\n=== {key.upper()} ({len(val)} results) ===")
                for i, item in enumerate(val[:25], 1):
                    if isinstance(item, dict):
                        apn = item.get("APN", item.get("apn", item.get("ParcelNumber", "")))
                        addr = item.get("SitusAddress", item.get("Address", item.get("address", "")))
                        owner = item.get("OwnerName", item.get("Owner", ""))
                        print(f"  {i}. APN: {apn}")
                        if addr:
                            print(f"     Address: {addr}")
                        if owner:
                            print(f"     Owner: {owner}")
            elif isinstance(val, (int, float)):
                print(f"{key}: {val}")
    elif isinstance(data, list):
        for i, item in enumerate(data[:25], 1):
            if isinstance(item, dict):
                print(f"  {i}. {json.dumps(item, default=str)}")

def print_report_summary(report):
    """Print a human-readable property report."""
    if not report:
        print("No data found.")
        return

    addr = report.get("address", {})
    owner = report.get("owner", {})
    prop = report.get("propertyinfo", {})
    vals = report.get("valuations", {})
    res = report.get("residential", {})

    print("=" * 60)
    print("  PROPERTY REPORT")
    print("=" * 60)

    if isinstance(addr, dict):
        parts = [addr.get("HouseNumber", ""), addr.get("Direction", ""),
                 addr.get("StreetName", ""), addr.get("Suffix", "")]
        street = " ".join(p for p in parts if p)
        city = addr.get("CityName", "")
        zip_code = addr.get("Zip", "")
        if street:
            print(f"\n  Address: {street}")
        if city or zip_code:
            print(f"           {city}, AZ {zip_code}")

    if isinstance(owner, dict):
        name = owner.get("OwnerName", owner.get("Name", ""))
        if isinstance(owner, list) and owner:
            name = owner[0].get("OwnerName", owner[0].get("Name", ""))
        if name:
            print(f"  Owner: {name}")
    elif isinstance(owner, list) and owner:
        for o in owner:
            name = o.get("OwnerName", o.get("Name", ""))
            if name:
                print(f"  Owner: {name}")

    if isinstance(prop, dict):
        for key in ["PropertyType", "LegalClass", "YearBuilt", "LivingArea",
                     "LotSizeSqFt", "LotSizeAcres", "Bedrooms", "Bathrooms",
                     "Pool", "Garage", "Construction", "Roofing"]:
            val = prop.get(key)
            if val:
                print(f"  {key}: {val}")

    if isinstance(res, dict):
        for key in ["YearBuilt", "LivingArea", "Bedrooms", "Bathrooms",
                     "Stories", "Pool", "GarageType", "Construction", "Quality"]:
            val = res.get(key)
            if val and key not in (prop if isinstance(prop, dict) else {}):
                print(f"  {key}: {val}")

    if isinstance(vals, (dict, list)):
        val_list = vals if isinstance(vals, list) else vals.get("Valuations", vals.get("valuations", [vals]))
        if isinstance(val_list, list) and val_list:
            print(f"\n  --- Valuations (Last {len(val_list)} Years) ---")
            for v in val_list:
                if isinstance(v, dict):
                    year = v.get("TaxYear", v.get("Year", ""))
                    fcv = v.get("FullCashValue", v.get("FCV", ""))
                    lpv = v.get("LimitedValue", v.get("LPV", ""))
                    print(f"    {year}: FCV ${fcv:,}" if isinstance(fcv, (int, float)) else f"    {year}: FCV {fcv}", end="")
                    if lpv:
                        print(f"  LPV ${lpv:,}" if isinstance(lpv, (int, float)) else f"  LPV {lpv}")
                    else:
                        print()

    maps_data = report.get("maps")
    if maps_data:
        print(f"\n  Maps: {json.dumps(maps_data, default=str)}")

    print()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Maricopa County Assessor API client")
    parser.add_argument("command", choices=[
        "search", "subdivisions", "rentals",
        "parcel", "propertyinfo", "address", "valuations",
        "residential", "owner", "mcr", "str", "maps",
        "bookmaps", "mcrmaps", "bpp", "mh", "mhvin",
        "report"
    ])
    parser.add_argument("query", help="Search query, APN, MCR, STR, etc.")
    parser.add_argument("--page", type=int, help="Page number for paginated results")
    parser.add_argument("--token", help="API token (or set MC_ASSESSOR_TOKEN env var)")
    parser.add_argument("--format", choices=["json", "summary"], default="summary",
                        help="Output format (default: summary)")
    parser.add_argument("--book", help="Book number (for bookmaps)")
    parser.add_argument("--type", dest="bpp_type", choices=["c", "m", "l"],
                        help="BPP account type: c=commercial, m=multiple, l=lessor")
    parser.add_argument("--year", help="Tax year (for BPP)")

    args = parser.parse_args()
    token = args.token

    cmd = args.command
    q = args.query

    if cmd == "search":
        data = search_property(q, args.page, token)
    elif cmd == "subdivisions":
        data = search_subdivisions(q, token)
    elif cmd == "rentals":
        data = search_rentals(q, args.page, token)
    elif cmd == "parcel":
        data = parcel_details(q, token)
    elif cmd == "propertyinfo":
        data = property_info(q, token)
    elif cmd == "address":
        data = property_address(q, token)
    elif cmd == "valuations":
        data = valuation_details(q, token)
    elif cmd == "residential":
        data = residential_details(q, token)
    elif cmd == "owner":
        data = owner_details(q, token)
    elif cmd == "mcr":
        data = mcr_data(q, args.page, token)
    elif cmd == "str":
        data = str_data(q, args.page, token)
    elif cmd == "maps":
        data = parcel_maps(q, token)
    elif cmd == "bookmaps":
        if not args.book:
            print("--book required for bookmaps", file=sys.stderr)
            sys.exit(1)
        data = book_maps(args.book, q, token)
    elif cmd == "mcrmaps":
        data = mcr_maps(q, token)
    elif cmd == "bpp":
        if not args.bpp_type:
            print("--type required for bpp (c/m/l)", file=sys.stderr)
            sys.exit(1)
        data = bpp_account(args.bpp_type, q, args.year, token)
    elif cmd == "mh":
        data = mobile_home(q, token)
    elif cmd == "mhvin":
        data = mobile_home_vin(q, token)
    elif cmd == "report":
        data = full_report(q, token)
        if args.format == "summary":
            print_report_summary(data)
            return
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json" or cmd not in ("search", "report"):
        print_json(data)
    else:
        print_search_summary(data)

if __name__ == "__main__":
    main()
