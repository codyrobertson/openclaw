#!/usr/bin/env python3
"""
Real estate listing scraper using scrapling (browser-level scraping).
Bypasses API blocks by scraping actual search result pages.

Usage:
  # Zillow — for sale in a zip code
  python3 listings.py zillow "85251" --type for_sale --output summary

  # Zillow — sold recently
  python3 listings.py zillow "Scottsdale, AZ" --type sold --output csv --out ~/results.csv

  # Redfin — for sale
  python3 listings.py redfin "85251" --type for_sale

  # Realtor.com — for rent
  python3 listings.py realtor "Austin, TX" --type for_rent

  # All sources at once
  python3 listings.py all "85251" --type for_sale
"""

import csv
import os
import re
import sys
import json as json_mod
import time
from datetime import datetime
from urllib.parse import quote_plus

os.environ.setdefault("CURL_CA_BUNDLE", "/etc/ssl/cert.pem")

try:
    from scrapling import Fetcher, StealthyFetcher
except ImportError:
    print("ERROR: scrapling not available. Install: pip install scrapling", file=sys.stderr)
    sys.exit(1)


def scrape_zillow(location, listing_type="for_sale"):
    """Scrape Zillow search results from embedded JSON."""
    loc_slug = location.replace(" ", "-").replace(",", "").lower()

    if listing_type == "sold":
        url = f"https://www.zillow.com/{loc_slug}/sold/"
    elif listing_type == "for_rent":
        url = f"https://www.zillow.com/{loc_slug}/rentals/"
    else:
        url = f"https://www.zillow.com/{loc_slug}/"

    print(f"Scraping Zillow: {url}", file=sys.stderr)
    fetcher = Fetcher()
    page = fetcher.get(url)

    listings = []

    # Find the big JSON blob with listResults
    for script in page.find_all("script"):
        text = script.text or ""
        if '"listResults"' not in text:
            continue
        # Extract the listResults array from the JSON
        try:
            match = re.search(r'"listResults"\s*:\s*\[', text)
            if not match:
                continue
            # Find the start of the array and parse from there
            # Try to parse from a known structure
            # The data is inside: {"cat1":{"searchResults":{"listResults":[...]}}}
            cat1_match = re.search(r'"cat1"\s*:\s*\{', text)
            if cat1_match:
                # Parse from cat1 onwards
                depth = 0
                cat1_start = cat1_match.start()
                cat1_end = cat1_start
                for i in range(cat1_match.end() - 1, len(text)):
                    if text[i] == '{':
                        depth += 1
                    elif text[i] == '}':
                        depth -= 1
                        if depth == 0:
                            cat1_end = i + 1
                            break
                chunk = '{' + text[cat1_start:cat1_end] + '}'
                try:
                    data = json_mod.loads(chunk)
                    results = data.get("cat1", {}).get("searchResults", {}).get("listResults", [])
                    for item in results:
                        listing = extract_zillow_listing(item)
                        if listing:
                            listings.append(listing)
                except json_mod.JSONDecodeError:
                    pass

            if listings:
                break

            # Fallback: extract individual zpid objects
            for m in re.finditer(r'\{"zpid"\s*:\s*"?\d+"?[^}]*"address"[^}]*\}', text):
                try:
                    obj = json_mod.loads(m.group())
                    listing = extract_zillow_listing(obj)
                    if listing:
                        listings.append(listing)
                except json_mod.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"Parse error: {e}", file=sys.stderr)
            continue

    return listings


def extract_zillow_listing(item):
    """Extract a single listing from Zillow's JSON data."""
    listing = {"source": "zillow"}
    listing["address"] = item.get("address", item.get("streetAddress", ""))
    listing["price"] = item.get("unformattedPrice", item.get("price", ""))
    if isinstance(listing["price"], str) and listing["price"].startswith("$"):
        cleaned = listing["price"].replace("$", "").replace(",", "").strip()
        if cleaned.replace(".", "").isdigit():
            listing["price"] = cleaned

    listing["beds"] = item.get("beds", "")
    listing["baths"] = item.get("baths", "")
    listing["sqft"] = item.get("area", item.get("livingArea", ""))
    listing["lot_sqft"] = item.get("lotAreaValue", "")
    listing["zpid"] = item.get("zpid", "")
    listing["status"] = item.get("statusText", item.get("homeStatus", ""))
    listing["latitude"] = item.get("latLong", {}).get("latitude", "") if isinstance(item.get("latLong"), dict) else ""
    listing["longitude"] = item.get("latLong", {}).get("longitude", "") if isinstance(item.get("latLong"), dict) else ""
    listing["broker"] = item.get("brokerName", "")

    detail_url = item.get("detailUrl", "")
    if detail_url and not detail_url.startswith("http"):
        detail_url = f"https://www.zillow.com{detail_url}"
    listing["url"] = detail_url

    if listing["address"]:
        return listing
    return None


def scrape_redfin(location, listing_type="for_sale"):
    """Scrape Redfin search results."""
    if listing_type == "sold":
        url = f"https://www.redfin.com/city/{quote_plus(location)}/filter/include=sold-3mo"
    elif listing_type == "for_rent":
        url = f"https://www.redfin.com/city/{quote_plus(location)}/apartments-for-rent"
    else:
        url = f"https://www.redfin.com/zipcode/{location}" if location.isdigit() \
              else f"https://www.redfin.com/city/{quote_plus(location)}"

    print(f"Scraping Redfin: {url}", file=sys.stderr)
    fetcher = Fetcher()
    page = fetcher.get(url)

    listings = []

    # Parse bp-Homecard elements
    cards = page.find_all(".bp-Homecard")

    for card in cards:
        listing = {"source": "redfin"}

        # Address from bp-Homecard__Address link
        addr_el = card.find(".bp-Homecard__Address")
        if addr_el:
            listing["address"] = addr_el.text.strip()
            href = addr_el.attrib.get("href", "")
            if href.startswith("/"):
                href = f"https://www.redfin.com{href}"
            if href:
                listing["url"] = href

        # Price
        price_el = card.find(".bp-Homecard__Price--value")
        if price_el:
            listing["price"] = price_el.text.strip()

        # Stats
        beds_el = card.find(".bp-Homecard__Stats--beds")
        baths_el = card.find(".bp-Homecard__Stats--baths")
        sqft_el = card.find(".bp-Homecard__LockedStat--value")
        if beds_el:
            listing["beds"] = beds_el.text.strip().replace(" beds", "").replace(" bed", "")
        if baths_el:
            listing["baths"] = baths_el.text.strip().replace(" baths", "").replace(" bath", "")
        if sqft_el:
            listing["sqft"] = sqft_el.text.strip().replace(",", "").replace(" ", "")

        if listing.get("address") or listing.get("price"):
            listings.append(listing)

    return listings


def scrape_realtor(location, listing_type="for_sale"):
    """Scrape Realtor.com search results."""
    loc_slug = location.replace(" ", "-").replace(",", "").replace(".", "").lower()

    type_map = {
        "for_sale": "realestateandhomes-search",
        "sold": "realestateandhomes-sold",
        "for_rent": "apartments",
        "pending": "realestateandhomes-search",
    }
    section = type_map.get(listing_type, "realestateandhomes-search")

    url = f"https://www.realtor.com/{section}/{loc_slug}"

    print(f"Scraping Realtor.com: {url}", file=sys.stderr)

    def _wait_for_kasada(_page):
        """Realtor.com uses Kasada anti-bot — need to wait for JS challenge."""
        time.sleep(10)

    try:
        fetcher = StealthyFetcher()
        page = fetcher.fetch(
            url,
            real_chrome=True,
            headless=True,
            page_action=_wait_for_kasada,
            network_idle=True,
            timeout=60000,
        )
    except Exception as e:
        print(f"Realtor.com browser error: {e}", file=sys.stderr)
        return []

    if page.status == 429 or page.status == 403:
        print(f"Realtor.com blocked ({page.status}) — IP may be rate-limited, try again later.", file=sys.stderr)
        return []

    listings = []

    # Try __NEXT_DATA__ JSON first
    next_data = page.find("script#__NEXT_DATA__")
    if next_data and next_data.text:
        try:
            data = json_mod.loads(next_data.text)
            props = data.get("props", {}).get("pageProps", {})
            results = props.get("properties", []) or \
                      props.get("searchResults", {}).get("home_search", {}).get("results", [])
            for item in results:
                listing = {"source": "realtor"}
                loc = item.get("location", {})
                addr = loc.get("address", {})
                listing["address"] = addr.get("line", "")
                listing["city"] = addr.get("city", "")
                listing["state"] = addr.get("state_code", "")
                listing["zip"] = addr.get("postal_code", "")
                listing["price"] = item.get("list_price", item.get("price", ""))
                desc = item.get("description", {})
                listing["beds"] = desc.get("beds", "")
                listing["baths"] = desc.get("baths", "")
                listing["sqft"] = desc.get("sqft", desc.get("lot_sqft", ""))
                listing["year_built"] = desc.get("year_built", "")
                listing["property_type"] = desc.get("type", "")
                listing["status"] = item.get("status", "")
                listing["url"] = f"https://www.realtor.com{item.get('permalink', '')}" \
                    if item.get("permalink") else ""
                listing["days_on_market"] = item.get("list_date_min", "")
                if listing["address"]:
                    listings.append(listing)
        except (json_mod.JSONDecodeError, KeyError, TypeError) as e:
            print(f"JSON parse error: {e}", file=sys.stderr)

    # Fallback: parse HTML cards
    if not listings:
        cards = page.find_all("[data-testid='property-card']") or \
                page.find_all("[class*='PropertyCard']") or \
                page.find_all("[class*='property-card']")

        for card in cards:
            listing = {"source": "realtor"}

            addr_el = card.find("[data-testid='card-address']") or card.find("[class*='address']")
            if addr_el:
                listing["address"] = addr_el.text.strip()

            price_el = card.find("[data-testid='card-price']") or card.find("[class*='price']")
            if price_el:
                listing["price"] = price_el.text.strip()

            link_el = card.find("a[href*='/realestateandhomes-detail/']") or card.find("a[href]")
            if link_el:
                href = link_el.attrib.get("href", "")
                if href.startswith("/"):
                    href = f"https://www.realtor.com{href}"
                listing["url"] = href

            meta_el = card.find("[data-testid='card-meta']") or card.find("[class*='meta']")
            if meta_el:
                listing["details"] = meta_el.text.strip()

            if listing.get("address") or listing.get("price"):
                listings.append(listing)

    return listings


def format_output(listings, args):
    """Format and output results."""
    if not listings:
        print("No listings found.", file=sys.stderr)
        return

    if args.output == "json":
        print(json_mod.dumps(listings, indent=2, default=str))
        return

    if args.output == "csv":
        out_path = args.out or os.path.expanduser(
            f"~/openclaw/workspace/research_output/re_{args.source}_{args.type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        all_keys = set()
        for l in listings:
            all_keys.update(l.keys())
        all_keys = sorted(all_keys)
        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(listings)
        print(f"Saved {len(listings)} listings to: {out_path}")
        return

    # Summary output
    print(f"\n{'='*60}")
    print(f"  {args.source.upper()} — {args.location} — {args.type}")
    print(f"  {len(listings)} listings found")
    print(f"{'='*60}\n")

    # Parse prices for stats
    prices = []
    for l in listings:
        p = l.get("price", "")
        if isinstance(p, (int, float)):
            prices.append(p)
        elif isinstance(p, str):
            cleaned = re.sub(r'[^\d.]', '', p.replace(",", ""))
            if cleaned:
                try:
                    prices.append(float(cleaned))
                except ValueError:
                    pass

    if prices:
        print(f"  Price Range: ${min(prices):,.0f} — ${max(prices):,.0f}")
        prices_sorted = sorted(prices)
        median = prices_sorted[len(prices_sorted) // 2]
        print(f"  Median: ${median:,.0f}")
        print(f"  Average: ${sum(prices) / len(prices):,.0f}")
        print()

    # Print listings
    for i, l in enumerate(listings[:20], 1):
        addr = l.get("address", "N/A")
        price = l.get("price", "N/A")
        details = l.get("details", "")
        beds = l.get("beds", "")
        baths = l.get("baths", "")
        sqft = l.get("sqft", "")
        if beds or baths or sqft:
            detail_parts = []
            if beds:
                detail_parts.append(f"{beds}bd")
            if baths:
                detail_parts.append(f"{baths}ba")
            if sqft:
                detail_parts.append(f"{sqft}sf")
            details = " / ".join(detail_parts)
        url = l.get("url", "")
        print(f"  {i:2d}. {addr}")
        price_str = str(price)
        if not price_str.startswith("$"):
            price_str = f"${price_str}"
        print(f"      {price_str}  {details}")
        if url:
            print(f"      {url}")
        print()

    if len(listings) > 20:
        print(f"  ... and {len(listings) - 20} more. Use --output csv to save all.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scrape real estate listings")
    parser.add_argument("source", choices=["zillow", "redfin", "realtor", "all"],
                        help="Site to scrape")
    parser.add_argument("location", help="Location: zip code, city/state, or neighborhood")
    parser.add_argument("--type", default="for_sale",
                        choices=["for_sale", "for_rent", "sold", "pending"],
                        help="Listing type (default: for_sale)")
    parser.add_argument("--output", choices=["csv", "json", "summary"], default="summary",
                        help="Output format (default: summary)")
    parser.add_argument("--out", help="Output file path (for csv)")
    args = parser.parse_args()

    all_listings = []

    if args.source in ("zillow", "all"):
        try:
            results = scrape_zillow(args.location, args.type)
            all_listings.extend(results)
            print(f"Zillow: {len(results)} listings", file=sys.stderr)
        except Exception as e:
            print(f"Zillow error: {e}", file=sys.stderr)

    if args.source in ("redfin", "all"):
        try:
            results = scrape_redfin(args.location, args.type)
            all_listings.extend(results)
            print(f"Redfin: {len(results)} listings", file=sys.stderr)
        except Exception as e:
            print(f"Redfin error: {e}", file=sys.stderr)

    if args.source in ("realtor", "all"):
        try:
            results = scrape_realtor(args.location, args.type)
            all_listings.extend(results)
            print(f"Realtor.com: {len(results)} listings", file=sys.stderr)
        except Exception as e:
            print(f"Realtor.com error: {e}", file=sys.stderr)

    format_output(all_listings, args)


if __name__ == "__main__":
    main()
