---
name: re-recorder
description: Maricopa County Recorder document search — find deeds, liens, mortgages, judgments, and other recorded documents from 1871-present. Use when asked about ownership history, title search, liens, recorded documents, deed lookup, or Maricopa County recording records.
---

# Maricopa County Recorder

Search recorded documents (deeds, mortgages, liens, etc.) from the Maricopa County Recorder's Office. Coverage: 1871-present.

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

# With date range
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --from 2020-01-01 --to 2026-03-08

# Filter by document type
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --doctype DEED
```

### Search by Business Name

```bash
python3 skills/re-recorder/scripts/recorder.py business "ABC Holdings LLC"
python3 skills/re-recorder/scripts/recorder.py business "First American Title" --doctype DEEDTR
```

### Search by Recording Number

```bash
# Year + sequence number
python3 skills/re-recorder/scripts/recorder.py recording "2024" "0715342"
```

### List Document Type Codes

```bash
python3 skills/re-recorder/scripts/recorder.py types
```

### JSON Output

```bash
python3 skills/re-recorder/scripts/recorder.py name "Smith" "John" --format json
```

## Common Document Type Codes

| Code      | Description              |
| --------- | ------------------------ |
| `DEED`    | Deed                     |
| `DEEDTR`  | Deed of Trust            |
| `RELDTR`  | Release of Deed of Trust |
| `MTG`     | Mortgage                 |
| `RELMTG`  | Release of Mortgage      |
| `LIEN`    | Lien                     |
| `RELLIEN` | Release of Lien          |
| `MECHLN`  | Mechanic's Lien          |
| `JUDGMT`  | Judgment                 |
| `AFFDT`   | Affidavit                |
| `QUIT`    | Quit Claim Deed          |
| `WARR`    | Warranty Deed            |
| `SPWARR`  | Special Warranty Deed    |
| `TRUSTEE` | Trustee's Deed           |
| `CCREST`  | CC&Rs                    |
| `EASMNT`  | Easement                 |
| `POA`     | Power of Attorney        |

## Workflow: Title Chain

```bash
# 1. Find the APN via assessor
python3 skills/re-assessor/scripts/assessor.py search "4610 E Flower St"

# 2. Get current owner
python3 skills/re-assessor/scripts/assessor.py owner 163-32-037

# 3. Search recorder for all deeds on that owner
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype DEED

# 4. Check for liens
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype LIEN

# 5. Check for deeds of trust (mortgages)
python3 skills/re-recorder/scripts/recorder.py name "OwnerLastName" "OwnerFirstName" --doctype DEEDTR
```

## Data Source

Website: `https://legacy.recorder.maricopa.gov/recdocdata/`
Coverage: June 1, 1871 through present
Max results: 500 per search

## Dependencies

- Works with or without scrapling (falls back to urllib)
- No API token required (public website)

## Rules

- Use `--format json` when parsing output programmatically.
- Max 500 results per search. Use date ranges to narrow.
- Combine with `re-assessor` skill for full property research.
- For title searches: search by both owner names AND property-related parties.
- Document types can be combined with name/date filters.
