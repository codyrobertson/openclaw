---
name: re-assessor
description: Maricopa County Assessor property lookup — search properties, get parcel details, owner info, lot size, school districts, deed info. Use when asked about property details, owner lookup, APN search, or Maricopa County property data.
---

# Maricopa County Assessor

Scrapes the public website at `mcassessor.maricopa.gov`. Uses the CSV export endpoint for search and server-rendered HTML for parcel details. No API token needed.

## When to Use

- "Who owns [address]?"
- "Look up APN [number]"
- "Get property details for [address]"
- "Property info for [zip/address/APN]"
- Any Maricopa County property research

## Script

```bash
python3 skills/re-assessor/scripts/assessor.py <command> <query> [options]
```

## Commands

### Search

```bash
# Search by address, owner name, or APN
python3 skills/re-assessor/scripts/assessor.py search "4610 E Flower St"
python3 skills/re-assessor/scripts/assessor.py search "Smith John"
python3 skills/re-assessor/scripts/assessor.py search "127-03-059"

# JSON output
python3 skills/re-assessor/scripts/assessor.py search "85018" --format json
```

### Parcel Detail (by APN)

```bash
# Full parcel details (owner, address, lot size, schools, deed info)
python3 skills/re-assessor/scripts/assessor.py parcel 127-03-059

# JSON output
python3 skills/re-assessor/scripts/assessor.py parcel 127-03-059 --format json
```

### Export (CSV)

```bash
# Export search results as raw CSV
python3 skills/re-assessor/scripts/assessor.py export "85018"
python3 skills/re-assessor/scripts/assessor.py export "Smith" --type property
python3 skills/re-assessor/scripts/assessor.py export "85018" --type rental
```

## Search Result Fields

| Field           | Description                  |
| --------------- | ---------------------------- |
| `apn`           | Assessor Parcel Number       |
| `owner`         | Current owner name           |
| `address`       | Property address             |
| `subdivision`   | Subdivision name             |
| `mcr`           | Map/Census/Range number      |
| `str`           | Section/Township/Range       |
| `property_type` | RESIDENTIAL, COMMERCIAL, etc |

## Parcel Detail Fields

| Field                        | Description                   |
| ---------------------------- | ----------------------------- |
| `apn`                        | Formatted APN (127-03-059)    |
| `property_type`              | Residential, Commercial, etc  |
| `address`                    | Full street address           |
| `owner`                      | Current owner                 |
| `mcr`                        | MCR number                    |
| `description`                | Subdivision name              |
| `lot_size`                   | Lot size in sq ft             |
| `lot_num`                    | Lot number                    |
| `high_school_district`       | High school district          |
| `elementary_school_district` | Elementary school district    |
| `local_jurisdiction`         | City/jurisdiction             |
| `market_area`                | Market area/neighborhood code |
| `mailing_address`            | Owner mailing address         |
| `deed_number`                | Last recorded deed number     |
| `last_deed_date`             | Date of last deed             |
| `sale_date`                  | Last sale date                |
| `sale_price`                 | Last sale price               |

## APN Format

Dashes/dots/spaces are stripped automatically:

- `127-03-059` or `127.03.059` or `12703059`

## Workflow: Property Research

```bash
# 1. Search by address to find APN
python3 skills/re-assessor/scripts/assessor.py search "4610 E Flower St"

# 2. Get full parcel details
python3 skills/re-assessor/scripts/assessor.py parcel 127-03-059

# 3. Search recorder for ownership chain
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype DEED
```

## Data Source

Website: `https://mcassessor.maricopa.gov`
No API token required (uses public web scraping).

## Dependencies

- Python 3 with standard library only (urllib, csv, re)
- Optional: `certifi` for SSL cert resolution on Homebrew Python

## Rules

- Use `--format json` when parsing output programmatically.
- APN is the primary key — search by address first, then use APN for detail lookups.
- Combine with `re-recorder` skill for ownership chain and lien history.
