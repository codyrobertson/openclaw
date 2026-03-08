#!/usr/bin/env python3
"""
Maricopa County Recorder document search scraper.
Searches recorded documents (deeds, liens, mortgages, etc.) from 1871-present.

Usage:
  # Search by person name
  python3 recorder.py name "Smith" "John"

  # Search by recording number
  python3 recorder.py recording "20240715342"

  # Search by business name
  python3 recorder.py business "ABC LLC"

  # Search by name with date range
  python3 recorder.py name "Smith" "John" --from 2020-01-01 --to 2026-03-08

  # Search by name with document type filter
  python3 recorder.py name "Smith" "John" --doctype "DEED"

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

# Common document type codes (display names from the site's dropdown)
DOC_TYPES = {
    "DEED": "DEED/USE WITH ANY GENERAL DEED TYPE",
    "DEED OF TRUST": "DEED OF TRUST",
    "MORTGAGE": "MORTGAGE",
    "WAR DEED": "WARRANTY DEED",
    "SPWARR": "SPECIAL WARRANTY DEED",
    "Q/CL DEED": "QUIT CLAIM DEED",
    "TRUSTEES DEED": "TRUSTEES DEED OF ANY KIND",
    "REL D/TR": "DEED OF RELEASE & FULL RECONVEYANCE OF D/TR",
    "REL MTG": "RELEASE OF MORTGAGE",
    "JUDGMENT": "JUDGMENT-GENERAL TYPES INCLUDNG CIVIL",
    "ASSIGNMNT": "ASSIGNMNT OF MTG/DEED OF TRUST OR ASSIGNMNTS",
    "AFFIDAVIT": "AFFIDAVIT/USE WITH ANY \"GENERAL\" TYPE AFFIDAVIT",
    "AGREEMENT": "AGREEMENT/USE WITH ANY GENERAL AGREEMENT",
    "EASEMENT": "EASEMENT - DEDICATION OF RIGHT OF WAY",
    "LIS PEND": "LIS PENDENS",
    "POWER ATT": "POWER OF ATTORNEY",
    "LIEN": "LIENS-GOVT/NON-GOVT & GENERAL LIENS",
    "FED TAX LN": "FEDERAL TAX LIEN",
    "STATE TAX": "STATE TAX LIEN",
    "MECH LIEN": "MATERIAL MANS MECH LN",
    "NOTICE": "NOTICE",
    "PLAT MAP": "PLAT MAP",
    "BEN DEED": "BENEFICIARY DEED",
    "PROP REST": "PROPERTY RESTRICTIONS FOR CONDO/SUBDIV",
    "SUB TRUST": "SUBSTITUTION OF TRUSTEE ON DEED OF TRUST",
    "MISC RCRD": "MISCELLANEOUS RECORDING",
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
    import ssl
    if not os.path.exists(ssl.get_default_verify_paths().cafile or ""):
        ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=ca)

_setup_ssl()


def _format_date(date_str):
    """Convert YYYY-MM-DD to M/D/YYYY as the site expects."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.month}/{dt.day}/{dt.year}"
    except ValueError:
        return date_str


def search_by_name(last_name, first_name="", middle="", date_from=None, date_to=None,
                   doc_type=""):
    """Search recorded documents by personal name."""
    params = {
        "ln1": last_name,
        "fn1": first_name,
        "mn1": middle,
        "ln2": "",
        "fn2": "",
        "mn2": "",
        "biz1": "",
        "biz2": "",
        "doc1": doc_type,
        "doc2": "",
        "doc3": "",
        "doc4": "",
        "doc5": "",
        "begdt": _format_date(date_from) or "1/1/1947",
        "enddt": _format_date(date_to) or datetime.now().strftime("%-m/%-d/%Y"),
    }
    return _fetch_results(params)


def search_by_business(name, date_from=None, date_to=None, doc_type=""):
    """Search recorded documents by business name."""
    params = {
        "biz1": name,
        "biz2": "",
        "ln1": "",
        "fn1": "",
        "mn1": "",
        "ln2": "",
        "fn2": "",
        "mn2": "",
        "doc1": doc_type,
        "doc2": "",
        "doc3": "",
        "doc4": "",
        "doc5": "",
        "begdt": _format_date(date_from) or "1/1/1947",
        "enddt": _format_date(date_to) or datetime.now().strftime("%-m/%-d/%Y"),
    }
    return _fetch_results(params)


def search_by_recording(rec_number):
    """Search by recording number. Goes to detail page directly."""
    url = f"{BASE_URL}/GetRecDataDetail.aspx?rec={rec_number}"
    html = _fetch_url(url)
    if not html:
        return []
    # Parse the detail page
    result = _parse_detail_page(html)
    return [result] if result else []


def _fetch_url(url):
    """Fetch a URL and return HTML content."""
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


def _fetch_results(params):
    """Fetch search results from the recorder website."""
    url = f"{BASE_URL}/GetRecDataPaging.aspx?{urllib.parse.urlencode(params)}"
    html = _fetch_url(url)
    if not html:
        return []
    return _parse_html_results(html)


def _parse_html_results(html):
    """Parse HTML table results with regex."""
    results = []
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    cell_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)
    tag_strip = re.compile(r'<[^>]+>')

    for row_match in row_pattern.finditer(html):
        row_html = row_match.group(1)
        cells = cell_pattern.findall(row_html)
        if len(cells) >= 4:
            clean = [tag_strip.sub("", c).strip() for c in cells]
            # Skip header rows
            if clean[0].lower() in ("name", "recording number", "rec number", ""):
                continue
            # Columns: Name, Recording Number, Recording Date, Document Code, Docket/Book, Page/Map
            result = {
                "name": clean[0] if len(clean) > 0 else "",
                "recording_number": clean[1] if len(clean) > 1 else "",
                "recording_date": clean[2] if len(clean) > 2 else "",
                "doc_type": clean[3] if len(clean) > 3 else "",
            }
            if len(clean) > 4:
                result["docket_book"] = clean[4]
            if len(clean) > 5:
                result["page_map"] = clean[5]
            if result["recording_number"] and result["recording_number"] != "&nbsp;":
                results.append(result)
    return results


def _parse_detail_page(html):
    """Parse a recording detail page."""
    tag_strip = re.compile(r'<[^>]+>')
    # Try to extract key fields from the detail page
    fields = {}
    # Look for table rows with label: value pattern
    row_pattern = re.compile(r'<tr[^>]*>(.*?)</tr>', re.DOTALL | re.IGNORECASE)
    cell_pattern = re.compile(r'<td[^>]*>(.*?)</td>', re.DOTALL | re.IGNORECASE)

    for row_match in row_pattern.finditer(html):
        row_html = row_match.group(1)
        cells = cell_pattern.findall(row_html)
        if len(cells) >= 2:
            label = tag_strip.sub("", cells[0]).strip().rstrip(":")
            value = tag_strip.sub("", cells[1]).strip()
            if label and value:
                fields[label] = value

    if not fields:
        return None

    return {
        "recording_number": fields.get("Recording Number", fields.get("Rec Number", "")),
        "recording_date": fields.get("Recording Date", fields.get("Rec Date", "")),
        "doc_type": fields.get("Document Code", fields.get("Doc Code", "")),
        "name": fields.get("Name", ""),
        "details": fields,
    }


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
        name = doc.get("name", "")
        book = doc.get("docket_book", "")
        page = doc.get("page_map", "")

        print(f"  {i}. {rec_num}  ({rec_date})")
        print(f"     Type: {doc_type}")
        if name:
            print(f"     Name: {name}")
        if book or page:
            print(f"     Book/Page: {book}/{page}")
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
    name_p.add_argument("--doctype", default="", help="Document type code")
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
    rec_p.add_argument("number", help="Full recording number (e.g. 20240715342)")
    rec_p.add_argument("--format", choices=["json", "summary"], default="summary")

    # Document types reference
    subparsers.add_parser("types", help="List common document type codes")

    args = parser.parse_args()

    if args.command == "types":
        print("\nCommon Document Type Codes:")
        print("-" * 50)
        for code, name in sorted(DOC_TYPES.items()):
            print(f"  {code:12s}  {name}")
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
        results = search_by_recording(args.number)
    else:
        parser.print_help()
        return

    print_results(results, args.format)


if __name__ == "__main__":
    main()
