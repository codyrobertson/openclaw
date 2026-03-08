---
name: re-property
description: Deep property research — tax records, ownership history, permits, liens, zoning, flood zone, school district, lot details, and county assessor data. Use when asked to research a specific property address or prepare for a listing appointment.
---

# Property Deep-Dive Skill

## When to Use

Any request to research a specific property:

- "Pull everything on [address]"
- "Research [address] before my listing appointment"
- "Who owns [address]?"
- "What are the taxes on [property]?"
- "Zoning for [address]?"
- "Is [address] in a flood zone?"
- "Permit history for [property]"

## Research Checklist

For a complete property deep-dive, gather all of the following:

### 1. Ownership & Title

- Current owner name(s)
- Ownership type (individual, trust, LLC, estate)
- Purchase date and price (deed transfer)
- Deed type (warranty, quitclaim, trustee)
- Title encumbrances (liens, easements, covenants)

**Sources:** County recorder/assessor, property appraiser site

### 2. Tax Records

- Assessed value (land + improvements)
- Annual property tax amount
- Tax rate / millage
- Exemptions (homestead, senior, veteran, disability)
- Tax payment status (current, delinquent, tax lien)
- Special assessments

**Sources:** County assessor, county treasurer

### 3. Property Details

- Legal description
- Parcel number / APN
- Lot size (acres and sqft)
- Year built
- Living area (sqft)
- Bedrooms / bathrooms
- Construction type (frame, block, steel)
- Roof type and age
- Foundation type
- Garage / carport
- Pool / spa
- Number of stories

**Sources:** County assessor, Zillow, Redfin

### 4. Permits & Improvements

- Building permits (with dates and scope)
- Open/expired permits (red flag)
- Renovation history
- Additions (permitted vs unpermitted)
- Solar installations
- Pool permits

**Sources:** City/county building department, permit portal

### 5. Zoning & Land Use

- Current zoning designation (R-1, C-2, etc.)
- Allowed uses
- Setback requirements
- Height restrictions
- ADU eligibility
- Overlay districts (historic, scenic, etc.)
- Future land use designation
- Pending zoning changes

**Sources:** City/county planning department, zoning maps

### 6. Flood & Environmental

- FEMA flood zone designation (A, AE, X, etc.)
- Flood insurance requirement
- Flood history
- Environmental hazards (contamination, superfund proximity)
- Wildfire risk zone
- Earthquake fault proximity (where applicable)

**Sources:** FEMA flood map, state environmental agency

### 7. Schools

- Assigned elementary, middle, high school
- School district name
- GreatSchools ratings
- School choice / open enrollment options
- Distance to assigned schools

**Sources:** GreatSchools.org, school district boundary maps

### 8. Neighborhood Context

- HOA (name, dues, restrictions)
- Walk Score / Transit Score / Bike Score
- Nearby amenities (grocery, dining, parks)
- Crime relative to city average
- Noise (airport, highway, rail proximity)

**Sources:** WalkScore, HOA docs, crime mapping sites

### 9. Market Position

- Estimated current value (Zestimate, Redfin Estimate)
- Last sale price and date
- Price history (all transfers)
- Days since last sale
- Comparable recent sales (3-5 comps)

**Sources:** Zillow, Redfin, county recorder

## Research Protocol

### Quick Lookup (single data point)

```bash
# Use exa-search for fast answers
python3 ~/.openclaw/workspace/skills/exa-search/scripts/search.py \
  --query "property tax [address] [county] county assessor" --count 5
```

### Full Deep-Dive

1. **Start with county assessor** — most data lives here:
   - Search the county assessor/appraiser website for the parcel
   - Extract: owner, assessed value, taxes, property details, legal description

2. **Check permits** — city/county building department portal

3. **Flood zone** — FEMA flood map service

4. **Zoning** — city planning/zoning map

5. **Schools** — GreatSchools or district boundary lookup

6. **Market data** — use re-scrape or re-market skills for comps and estimates

### County Assessor Sites (Common Markets)

| County          | Assessor URL               |
| --------------- | -------------------------- |
| Maricopa, AZ    | mcassessor.maricopa.gov    |
| Clark, NV       | clarkcountynv.gov/assessor |
| Los Angeles, CA | assessor.lacounty.gov      |
| Harris, TX      | hcad.org                   |
| Cook, IL        | cookcountyassessor.com     |
| Miami-Dade, FL  | miamidade.gov/pa           |
| King, WA        | kingcounty.gov/assessor    |

For other counties, search: `[county name] county assessor property search`

## Output Format

```markdown
## Property Report: [Address]

### Ownership

- Owner: [name]
- Purchased: [date] for $[price]
- Ownership type: [individual/trust/LLC]

### Tax Summary

- Assessed Value: $[amount] (Land: $[X] + Improvements: $[Y])
- Annual Tax: $[amount]
- Exemptions: [list or none]
- Status: [current/delinquent]

### Property Details

| Detail       | Value              |
| ------------ | ------------------ |
| Parcel #     | [APN]              |
| Year Built   | [YYYY]             |
| Beds/Baths   | [X/Y]              |
| Living SF    | [N]                |
| Lot Size     | [N] sf ([X] acres) |
| Construction | [type]             |
| Roof         | [type]             |
| Pool         | [yes/no]           |

### Zoning

- Zone: [designation] — [description]
- ADU Eligible: [yes/no/check]

### Flood Zone

- FEMA Zone: [designation]
- Insurance Required: [yes/no]

### Schools

| Level      | School | Rating |
| ---------- | ------ | ------ |
| Elementary | [name] | [X/10] |
| Middle     | [name] | [X/10] |
| High       | [name] | [X/10] |

### Permits

| Date   | Type   | Description | Status        |
| ------ | ------ | ----------- | ------------- |
| [date] | [type] | [scope]     | [open/closed] |

### Market Position

- Estimated Value: $[amount]
- Last Sale: $[price] on [date]
- Comparable Sales: [count] comps, median $[amount]/sf

### Red Flags

- [Any open permits, liens, delinquent taxes, unpermitted work, flood zone issues]

_Report generated [date]. Data sources: [list sources used]_
```

## Rules

- Always note data source and date for each piece of information.
- Flag open permits — these can kill a deal or delay closing.
- Flag tax delinquencies — may indicate distressed seller.
- Note when assessed value significantly differs from market value (appeal opportunity or assessment lag).
- For county assessor sites that require JavaScript, use agent-browser.
- Privacy: don't include owner SSN, DOB, or other PII beyond name and address (public record).
