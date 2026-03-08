---
name: re-leads
description: Real estate lead research and prospecting. Use when asked to find property leads, motivated sellers, off-market deals, FSBO listings, pre-foreclosures, probate properties, vacant properties, or any real estate lead generation task.
---

# Real Estate Lead Research Skill

## When to Use

Any request involving finding real estate leads, prospecting, or sourcing deals:

- "Find motivated sellers in [area]"
- "Pull FSBO listings in [zip]"
- "Find pre-foreclosure leads"
- "Research off-market properties"
- "Find vacant lots in [city]"
- "Wholesaling leads in [market]"

## Protocol

### 1. Clarify Target Criteria

Before researching, confirm:

- **Market/Area**: City, county, zip code, or neighborhood
- **Property Type**: SFR, multi-family, commercial, land, mobile homes
- **Lead Type**: Motivated sellers, FSBO, pre-foreclosure, probate, tax lien, vacant, absentee owner, expired listing, divorce, code violation
- **Price Range**: Min/max purchase price or ARV
- **Output Format**: CSV, summary report, or both

### 2. Create Durable Task

```bash
taskman create --name "RE Leads: <area> - <type>" --description "<criteria>" --priority high
```

### 3. Spawn Research Subagent

```
sessions_spawn(
  task: "TASK_ID=<id>. Real estate lead research.

TARGET: <area/market>
PROPERTY TYPE: <type>
LEAD TYPE: <type>
PRICE RANGE: <range>

RESEARCH PLAN:
1. Search county assessor/recorder sites for target properties
2. Search Zillow, Redfin, Realtor.com for FSBO/price-reduced/expired
3. Search auction sites (auction.com, hubzu, xome) for distressed
4. Cross-reference with public records for ownership, liens, tax status
5. Score each lead by motivation signals

For each lead capture:
- Address, city, state, zip
- Owner name (if available from public records)
- Property type, beds/baths/sqft, lot size, year built
- List price or estimated value
- Days on market / listing status
- Motivation signals (price drops, vacant, tax delinquent, code violations)
- Source URL

TOOLS:
- exa-search for web search
- agent-browser for browsing property sites
- scrapling for data extraction

CHECKPOINTING:
- taskman update <id> --status running
- After each batch: taskman checkpoint <id> --data '{...}'
- Save results to ~/openclaw/workspace/research_output/re_leads_<area>_<date>.csv
- taskman complete <id> --result 'path'",
  label: "re-leads-<area>",
  mode: "run",
  runTimeoutSeconds: 600
)
```

### 4. Lead Scoring Framework

Score each lead 1-10 based on motivation signals:

| Signal                        | Points |
| ----------------------------- | ------ |
| Pre-foreclosure / NOD filed   | +3     |
| Tax delinquent (2+ years)     | +3     |
| Vacant / utilities off        | +2     |
| Absentee owner (out of state) | +2     |
| Probate / inherited           | +2     |
| Code violations               | +2     |
| FSBO / expired listing        | +1     |
| Price reduced 2+ times        | +1     |
| High DOM (90+ days)           | +1     |
| Divorce filing                | +2     |

### 5. Data Sources (by lead type)

**FSBO/Expired:**

- Zillow FSBO filter, Craigslist real estate, ForSaleByOwner.com
- Expired MLS via Vulcan7, REDX, or manual MLS search

**Pre-Foreclosure:**

- County recorder NOD/NTS filings
- PropertyShark, ATTOM, RealtyTrac

**Probate:**

- County probate court filings
- Local obituary cross-reference

**Tax Lien/Delinquent:**

- County treasurer/tax collector sites
- Tax lien auction calendars

**Vacant Properties:**

- USPS vacancy data, driving-for-dollars follow-up
- County water/utility disconnect records

**Absentee Owners:**

- County assessor (owner address vs property address mismatch)
- Skip trace for contact info

### 6. Output Format

CSV with columns:

```
address, city, state, zip, property_type, beds, baths, sqft, lot_sqft, year_built, estimated_value, list_price, owner_name, owner_address, lead_type, motivation_score, signals, source_url, notes
```

Save to `~/openclaw/workspace/research_output/re_leads_<area>_<date>.csv`

## Rules

- ALWAYS create a taskman entry before spawning.
- ALWAYS checkpoint after each batch of leads.
- Use public data sources only — no paid skip-trace services without explicit approval.
- Note data freshness — property records can be months old.
- Flag any leads that appear in multiple distress categories (highest motivation).
