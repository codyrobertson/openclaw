---
name: re-scrape
description: Scrape real estate listings from Zillow, Redfin, and Realtor.com. Use when asked to pull listings, search properties, scrape MLS data, find homes for sale/rent/sold, or get property data from listing sites.
---

# Real Estate Scraping Skill

## When to Use

Any request to pull live listing data:

- "Pull listings in [zip/city]"
- "Scrape Zillow for [area]"
- "What's for sale in [neighborhood]?"
- "Get sold comps from Redfin"
- "Find rentals in [area]"
- "Scrape listings under $500K in [zip]"

## Quick Usage (listings.py)

Run with Python (requires scrapling: `pip install scrapling`):

```bash
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  <source> "<location>" --type <type> --output <format>
```

### Examples

```bash
# Zillow — for sale in a zip
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  zillow "85251" --type for_sale --output summary

# Redfin — recently sold
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  redfin "Scottsdale, AZ" --type sold --output csv --out ~/results.csv

# Realtor.com — rentals
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  realtor "Austin, TX" --type for_rent --output json

# All three sites at once
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  all "85251" --type for_sale --output csv --out ~/all_listings.csv
```

### Parameters

| Param    | Values                                    | Default        |
| -------- | ----------------------------------------- | -------------- |
| source   | `zillow`, `redfin`, `realtor`, `all`      | required       |
| location | zip code, "City, ST", neighborhood        | required       |
| --type   | `for_sale`, `for_rent`, `sold`, `pending` | for_sale       |
| --output | `summary`, `csv`, `json`                  | summary        |
| --out    | file path for csv output                  | auto-generated |

## Manual Scraping (agent-browser)

For individual property details or when listings.py can't get what you need, use agent-browser to browse interactively:

```bash
# Navigate to search results
agent-browser open "https://www.zillow.com/scottsdale-az/"
agent-browser snapshot
# Click into a listing
agent-browser click @e<N>
agent-browser snapshot
# Get all text from the listing page
agent-browser text
```

### Site-Specific URLs

**Zillow:**

- For sale: `https://www.zillow.com/<city>-<state>/`
- Sold: `https://www.zillow.com/<city>-<state>/sold/`
- Rentals: `https://www.zillow.com/<city>-<state>/rentals/`
- By zip: `https://www.zillow.com/homes/<zip>_rb/`
- Filters: append `/<beds>-bedrooms/` or `/<min>-<max>_price/`

**Redfin:**

- For sale: `https://www.redfin.com/zipcode/<zip>` or `https://www.redfin.com/city/<city>-<state>`
- Sold: add `/filter/include=sold-3mo`
- Map: `https://www.redfin.com/zipcode/<zip>/filter/property-type=house`

**Realtor.com:**

- For sale: `https://www.realtor.com/realestateandhomes-search/<city>_<state>`
- Sold: `https://www.realtor.com/realestateandhomes-sold/<city>_<state>`
- Rent: `https://www.realtor.com/apartments/<city>_<state>`

## Custom Scrapling Scripts (for advanced scraping)

When you need to scrape something specific (county records, auction sites, etc.), write inline scrapling:

```bash
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 << 'PYEOF'
from scrapling import StealthyFetcher
import json

fetcher = StealthyFetcher()
page = fetcher.get("https://www.zillow.com/homedetails/<zpid>_zpid/")

# Property details from embedded JSON
for script in page.find_all("script"):
    if "gdpClientCache" in (script.text or ""):
        # Parse the embedded data
        print(script.text[:2000])
        break
PYEOF
```

### County Records / Auction Sites

These vary per site. General pattern:

```bash
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 << 'PYEOF'
from scrapling import StealthyFetcher

fetcher = StealthyFetcher()
page = fetcher.get("https://mcassessor.maricopa.gov/")

# Navigate search
# ... site-specific selectors
PYEOF
```

For JS-heavy sites (auction.com, some county assessors), prefer agent-browser over scrapling.

## Subagent Pattern (for large scraping jobs)

```
sessions_spawn(
  task: "TASK_ID=<id>. Scrape real estate listings.

TARGET: <site> - <area>
TYPE: <for_sale/sold/for_rent>

Use the re-scrape listings.py script:
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  <source> '<location>' --type <type> --output csv --out ~/openclaw/workspace/research_output/re_<area>_<date>.csv

For individual property details, use agent-browser to visit listing URLs.
Checkpoint with taskman after each batch.",
  label: "re-scrape-<area>",
  mode: "run",
  runTimeoutSeconds: 600
)
```

## Data Fields by Source

**Zillow:** address, price, beds, baths, sqft, zpid, status, url
**Redfin:** address, price, details (beds/baths/sqft), url
**Realtor.com:** address, city, state, zip, price, beds, baths, sqft, year_built, property_type, status, url, days_on_market

## Rules

- Always use `CURL_CA_BUNDLE=/etc/ssl/cert.pem` with scrapling.
- Always use `python3` (not system python).
- Zillow and Redfin use `Fetcher`. Realtor.com uses `StealthyFetcher` with `real_chrome=True` (Kasada anti-bot bypass). Realtor.com may 429 if rate-limited — wait a few minutes and retry.
- Rate limit: don't hammer sites. The script handles one request per search naturally.
- For bulk scraping (hundreds of listings), break into batches with delays.
- Save output to `~/openclaw/workspace/research_output/`.
- If a site blocks you, switch to agent-browser for that site.
