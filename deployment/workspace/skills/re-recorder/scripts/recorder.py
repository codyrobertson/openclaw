#!/usr/bin/env python3
"""
Maricopa County Recorder document search scraper.
Searches recorded documents (deeds, liens, mortgages, etc.) from 1871-present.

Usage:
  # Search by person name
  python3 recorder.py name "Smith" "John"

  # Search by recording number (year + sequence)
  python3 recorder.py recording "2024" "0715342"

  # Search by business name
  python3 recorder.py business "ABC LLC"

  # Search by name with date range
  python3 recorder.py name "Robertson" "Cody" --from 2020-01-01 --to 2026-03-08

  # Search by name with document type filter
  python3 recorder.py name "Smith" "John" --doctype DEED

  # Output as JSON
  python3 recorder.py name "Smith" "John" --format json
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

BASE_URL = "https://legacy.recorder.maricopa.gov/recdocdata"

# Common document type codes
DOC_TYPES = {
    "DEED": "Deed",
    "DEEDTR": "Deed of Trust",
    "RELDTR": "Release of Deed of Trust",
    "SUBDTR": "Substitution of Trustee - Deed of Trust",
    "MTG": "Mortgage",
    "RELMTG": "Release of Mortgage",
    "ASSIGN": "Assignment",
    "LIEN": "Lien",
    "RELLIEN": "Release of Lien",
    "MECHLN": "Mechanic's Lien",
    "JUDGMT": "Judgment",
    "AFFDT": "Affidavit",
    "AGREE": "Agreement",
    "EASMNT": "Easement",
    "DECREE": "Decree",
    "NOTICE": "Notice",
    "POA": "Power of Attorney",
    "QUIT": "Quit Claim Deed",
    "WARR": "Warranty Deed",
    "SPWARR": "Special Warranty Deed",
    "TRUSTEE": "Trustee's Deed",
    "WILL": "Will",
    "CCREST": "Covenants, Conditions & Restrictions",
    "PLAT": "Plat",
    "MAP": "Map",
}

def _setup_ssl():
    """Ensure SSL cert bundle is found on macOS (Homebrew Python often missing default)."""
    try:
        import certifi
        ca = certifi.where()
    except ImportError:
        ca = "/etc/ssl/cert.pem"
    os.environ.setdefault("SSL_CERT_FILE", ca)
    os.environ.setdefault("CURL_CA_BUNDLE", ca)
    # Also patch urllib default context for this process
    import ssl
    if not os.path.exists(ssl.get_default_verify_paths().cafile or ""):
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=ca)

_setup_ssl()

try:
    from scrapling import Fetcher
    HAS_SCRAPLING = True
except ImportError:
    HAS_SCRAPLING = False


def search_by_name(last_name, first_name="", middle="", date_from=None, date_to=None,
                   doc_type="", max_results=500):
    """Search recorded documents by personal name."""
    params = {
        "lname": last_name,
        "fname": first_name,
        "mname": middle,
        "doctypegroup": doc_type,
        "begdate": date_from or "",
        "enddate": date_to or "",
        "maxresults": str(max_results),
    }
    return _fetch_results(params)


def search_by_business(name, date_from=None, date_to=None, doc_type="", max_results=500):
    """Search recorded documents by business name."""
    params = {
        "busname": name,
        "doctypegroup": doc_type,
        "begdate": date_from or "",
        "enddate": date_to or "",
        "maxresults": str(max_results),
    }
    return _fetch_results(params)


def search_by_recording(year, number, suffix=""):
    """Search by recording number."""
    params = {
        "recyear": year,
        "recnumber": number,
        "recsuffix": suffix,
    }
    return _fetch_results(params)


def _fetch_results(params):
    """Fetch search results from the recorder website."""
    if HAS_SCRAPLING:
        return _fetch_with_scrapling(params)
    return _fetch_with_urllib(params)


def _fetch_with_urllib(params):
    """Fallback: fetch with urllib and parse HTML manually."""
    url = f"{BASE_URL}/GetRecDataRslts.aspx?{urllib.parse.urlencode(params)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.reason}", file=sys.stderr)
        return []
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        return []

    return _parse_html_results(html)


def _fetch_with_scrapling(params):
    """Fetch with scrapling for better anti-bot handling."""
    url = f"{BASE_URL}/GetRecDataRslts.aspx?{urllib.parse.urlencode(params)}"
    fetcher = Fetcher()
    try:
        page = fetcher.get(url)
    except Exception as e:
        print(f"Scrapling error: {e}", file=sys.stderr)
        return _fetch_with_urllib(params)

    if page.status != 200:
        print(f"HTTP {page.status}", file=sys.stderr)
        return []

    results = []
    rows = page.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 5:
            result = _extract_row_data(cells)
            if result:
                results.append(result)
    return results


def _parse_html_results(html):
    """Parse HTML table results with regex (no BeautifulSoup needed)."""
    results = []
    # Find table rows
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    cell_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)
    tag_strip = re.compile(r'<[^>]+>')

    for row_match in row_pattern.finditer(html):
        row_html = row_match.group(1)
        cells = cell_pattern.findall(row_html)
        if len(cells) >= 5:
            clean_cells = [tag_strip.sub("", c).strip() for c in cells]
            # Skip header rows
            if clean_cells[0].lower() in ("recording number", "rec number", ""):
                continue
            result = {
                "recording_number": clean_cells[0] if len(clean_cells) > 0 else "",
                "recording_date": clean_cells[1] if len(clean_cells) > 1 else "",
                "doc_type": clean_cells[2] if len(clean_cells) > 2 else "",
                "parties": clean_cells[3] if len(clean_cells) > 3 else "",
            }
            # Only include non-empty results
            if result["recording_number"] and result["recording_number"] != "&nbsp;":
                results.append(result)
    return results


def _extract_row_data(cells):
    """Extract document data from a table row's cells."""
    try:
        texts = [c.text.strip() if hasattr(c, 'text') else str(c).strip() for c in cells]
        if not texts[0] or texts[0].lower() in ("recording number", "rec number"):
            return None
        result = {
            "recording_number": texts[0],
            "recording_date": texts[1] if len(texts) > 1 else "",
            "doc_type": texts[2] if len(texts) > 2 else "",
            "parties": texts[3] if len(texts) > 3 else "",
        }
        if len(texts) > 4:
            result["additional"] = texts[4]
        return result
    except (IndexError, AttributeError):
        return None


def print_results(results, fmt="summary"):
    """Print search results."""
    if not results:
        print("No documents found.")
        return

    if fmt == "json":
        print(json.dumps(results, indent=2, default=str))
        return

    print(f"\n{'=' * 70}")
    print(f"  RECORDED DOCUMENTS — {len(results)} found")
    print(f"{'=' * 70}\n")

    for i, doc in enumerate(results, 1):
        rec_num = doc.get("recording_number", "")
        rec_date = doc.get("recording_date", "")
        doc_type = doc.get("doc_type", "")
        parties = doc.get("parties", "")
        type_name = DOC_TYPES.get(doc_type, doc_type)

        print(f"  {i}. {rec_num}  ({rec_date})")
        print(f"     Type: {type_name}")
        if parties:
            print(f"     Parties: {parties}")
        print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Maricopa County Recorder document search")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Name search
    name_p = subparsers.add_parser("name", help="Search by personal name")
    name_p.add_argument("last_name")
    name_p.add_argument("first_name", nargs="?", default="")
    name_p.add_argument("--middle", default="")
    name_p.add_argument("--from", dest="date_from", help="Start date (YYYY-MM-DD)")
    name_p.add_argument("--to", dest="date_to", help="End date (YYYY-MM-DD)")
    name_p.add_argument("--doctype", default="", help="Document type code (DEED, MTG, LIEN, etc.)")
    name_p.add_argument("--format", choices=["json", "summary"], default="summary")

    # Business search
    biz_p = subparsers.add_parser("business", help="Search by business name")
    biz_p.add_argument("name")
    biz_p.add_argument("--from", dest="date_from")
    biz_p.add_argument("--to", dest="date_to")
    biz_p.add_argument("--doctype", default="")
    biz_p.add_argument("--format", choices=["json", "summary"], default="summary")

    # Recording number search
    rec_p = subparsers.add_parser("recording", help="Search by recording number")
    rec_p.add_argument("year", help="Recording year (e.g. 2024)")
    rec_p.add_argument("number", help="Recording sequence number")
    rec_p.add_argument("--suffix", default="")
    rec_p.add_argument("--format", choices=["json", "summary"], default="summary")

    # Document types reference
    types_p = subparsers.add_parser("types", help="List common document type codes")

    args = parser.parse_args()

    if args.command == "types":
        print("\nCommon Document Type Codes:")
        print("-" * 50)
        for code, name in sorted(DOC_TYPES.items()):
            print(f"  {code:10s}  {name}")
        return

    if args.command == "name":
        results = search_by_name(
            args.last_name, args.first_name, args.middle,
            args.date_from, args.date_to, args.doctype
        )
    elif args.command == "business":
        results = search_by_business(
            args.name, args.date_from, args.date_to, args.doctype
        )
    elif args.command == "recording":
        results = search_by_recording(args.year, args.number, args.suffix)
    else:
        parser.print_help()
        return

    print_results(results, args.format)


if __name__ == "__main__":
    main()
