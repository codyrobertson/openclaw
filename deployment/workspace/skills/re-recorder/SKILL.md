---
name: re-recorder
description: Maricopa County Recorder document search — find deeds, liens, mortgages, judgments, and other recorded documents from 1871-present. Use when asked about ownership history, title search, liens, recorded documents, deed lookup, or Maricopa County recording records.
---

# Maricopa County Recorder

Search recorded documents (deeds, mortgages, liens, etc.) from the Maricopa County Recorder's Office. Coverage: 1947-present (1871-1946 via separate tab on site).

## When to Use

- "Who has owned this property?"
- "Any liens on [address]?"
- "Pull the deed for [property]"
- "Title search for [name/property]"
- "Find mortgage documents for [name]"
- "What's recorded under [name]?"
- "Ownership chain for [property]"
- Any Maricopa County recorded document search

## Script

```bash
python3 skills/re-recorder/scripts/recorder.py <command> [args] [options]
```

## Commands

### Search by Person Name

```bash
# Last name only
python3 skills/re-recorder/scripts/recorder.py name "Smith"

# Last and first name
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John"

# With middle initial
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --middle "A"

# With date range (YYYY-MM-DD format)
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --from 2020-01-01 --to 2026-03-08

# Filter by document type (use full name from site dropdown)
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --doctype "DEED/USE WITH ANY GENERAL DEED TYPE"
```

### Search by Business Name

```bash
python3 skills/re-recorder/scripts/recorder.py business "ABC Holdings LLC"
python3 skills/re-recorder/scripts/recorder.py business "First American Title"
```

### Search by Recording Number

```bash
# Full recording number (e.g. 20240715342)
python3 skills/re-recorder/scripts/recorder.py recording "20240715342"
```

### List Document Type Codes

```bash
python3 skills/re-recorder/scripts/recorder.py types
```

### JSON Output

```bash
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --format json
```

## Result Fields

| Field              | Description                 |
| ------------------ | --------------------------- |
| `name`             | Party name on the document  |
| `recording_number` | Full recording number       |
| `recording_date`   | Date recorded (MM/DD/YYYY)  |
| `doc_type`         | Document type code          |
| `docket_book`      | Docket/book number (if any) |
| `page_map`         | Page/map number (if any)    |

## Common Document Types (as shown in results)

| Code         | Description              |
| ------------ | ------------------------ |
| `DEED`       | General Deed             |
| `DEED TRST`  | Deed of Trust            |
| `REL D/T`    | Release of Deed of Trust |
| `WAR DEED`   | Warranty Deed            |
| `SPEC/W D`   | Special Warranty Deed    |
| `Q/CL DEED`  | Quit Claim Deed          |
| `MORTGAGE`   | Mortgage                 |
| `REL MTG`    | Release of Mortgage      |
| `JUDGMENT`   | Judgment                 |
| `ASSIGNMNT`  | Assignment               |
| `AFFIDAVIT`  | Affidavit                |
| `LIS PEND`   | Lis Pendens              |
| `BENE DEED`  | Beneficiary Deed         |
| `SUB TRSTE`  | Substitution of Trustee  |
| `FIN STATE`  | Financing Statement      |
| `LIEN`       | Lien                     |
| `FED TAX LN` | Federal Tax Lien         |
| `MECH LIEN`  | Mechanic's Lien          |
| `NOTICE`     | Notice                   |

## Workflow: Title Chain

```bash
# 1. Find the APN via assessor
python3 skills/re-assessor/scripts/assessor.py search "4610 E Flower St"

# 2. Get current owner
python3 skills/re-assessor/scripts/assessor.py parcel 127-03-059

# 3. Search recorder for all deeds on that owner
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype DEED

# 4. Check for liens
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype LIEN

# 5. Check for deeds of trust (mortgages)
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype "DEED OF TRUST"
```

## Data Source

Website: `https://legacy.recorder.maricopa.gov/recdocdata/`
Coverage: 1947-present (default), 1871-1946 (separate tab on site)
Results: 20 per page (paginated via "Page Down" on site)

## Dependencies

- Python 3 with standard library only (urllib, re)
- Optional: `certifi` for SSL cert resolution on Homebrew Python
- No API token required (public website)

## Rules

- Use `--format json` when parsing output programmatically.
- Use date ranges to narrow results for common names.
- Combine with `re-assessor` skill for full property research.
- For title searches: search by both owner names AND property-related parties.
- Document types can be combined with name/date filters.
