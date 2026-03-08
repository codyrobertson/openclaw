---
name: re-assessor
description: Maricopa County Assessor property lookup via REST API — search properties, get parcel details, valuations, owner info, residential details, maps. Use when asked about property taxes, assessed values, property details, owner lookup, APN search, or Maricopa County property data.
---

# Maricopa County Assessor

Public REST API at `mcassessor.maricopa.gov`. Returns JSON. Requires API token for authenticated access.

## When to Use

- "What's this property worth?" / assessed value questions
- "Who owns [address]?"
- "Look up APN [number]"
- "Get property details for [address]"
- "What are the taxes on [property]?"
- "5-year valuation history"
- "Property info for [zip/address/APN]"
- Any Maricopa County property research

## Setup

Set `MC_ASSESSOR_TOKEN` env var. To get a token, use the contact form at mcassessor.maricopa.gov (select "API Question/Token").

The API works without a token for basic searches but may rate-limit.

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
python3 skills/re-assessor/scripts/assessor.py search "163-32-037"

# Paginate (25 results per page)
python3 skills/re-assessor/scripts/assessor.py search "85018" --page 2

# Subdivision search
python3 skills/re-assessor/scripts/assessor.py subdivisions "Arcadia"

# Rental registration search
python3 skills/re-assessor/scripts/assessor.py rentals "85018"
```

### Parcel Lookup (by APN)

```bash
# Full parcel details
python3 skills/re-assessor/scripts/assessor.py parcel 163-32-037

# Specific data
python3 skills/re-assessor/scripts/assessor.py propertyinfo 163-32-037
python3 skills/re-assessor/scripts/assessor.py address 163-32-037
python3 skills/re-assessor/scripts/assessor.py valuations 163-32-037
python3 skills/re-assessor/scripts/assessor.py residential 163-32-037
python3 skills/re-assessor/scripts/assessor.py owner 163-32-037

# MCR and Section/Township/Range
python3 skills/re-assessor/scripts/assessor.py mcr 12345
python3 skills/re-assessor/scripts/assessor.py str 1-1N-3E

# Parcel maps
python3 skills/re-assessor/scripts/assessor.py maps 163-32-037
```

### Full Report (all endpoints combined)

```bash
python3 skills/re-assessor/scripts/assessor.py report 163-32-037
```

## API Endpoints Reference

| Endpoint            | Path                                | Description                             |
| ------------------- | ----------------------------------- | --------------------------------------- |
| Search Property     | `/search/property/?q={query}`       | All property types, paginated (25/page) |
| Search Subdivisions | `/search/sub/?q={query}`            | Subdivision names and parcel counts     |
| Search Rentals      | `/search/rental/?q={query}`         | Rental registrations, paginated         |
| Parcel Details      | `/parcel/{apn}`                     | All parcel data                         |
| Property Info       | `/parcel/{apn}/propertyinfo`        | Property-specific info                  |
| Address             | `/parcel/{apn}/address`             | Property address                        |
| Valuations          | `/parcel/{apn}/valuations`          | 5-year FCV/LPV history                  |
| Residential         | `/parcel/{apn}/residential-details` | Residential details                     |
| Owner               | `/parcel/{apn}/owner-details`       | Owner information                       |
| MCR                 | `/parcel/mcr/{mcr}`                 | MCR data, paginated                     |
| STR                 | `/parcel/str/{str}`                 | Section/Township/Range, paginated       |
| Parcel Maps         | `/mapid/parcel/{apn}`               | Map file names                          |
| Book/Map            | `/mapid/bookmap/{book}/{map}`       | Book/map file names                     |
| MCR Maps            | `/mapid/mcr/{mcr}`                  | MCR map file names                      |
| BPP Account         | `/bpp/{type}/{acct}[/{year}]`       | Business personal property              |
| Mobile Home         | `/mh/{acct}`                        | Mobile home account                     |
| MH VIN              | `/mh/vin/{vin}`                     | Mobile home by VIN                      |

## Auth

Header: `AUTHORIZATION: <token>` (custom header, not Bearer).
User-Agent must be set to empty string or null.

## APN Format

Assessor Parcel Number can include spaces, dashes, or dots:

- `163-32-037`
- `163.32.037`
- `16332037`

## Rules

- Always use `--format json` when piping output to other tools.
- APN is the primary key — search by address first, then use APN for detail lookups.
- Valuations show FCV (Full Cash Value) and LPV (Limited Property Value).
- Results paginate at 25 per page. Use `--page N` for more.
- Combine with `re-recorder` skill for ownership chain and lien history.
