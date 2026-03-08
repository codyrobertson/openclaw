---
name: re-market
description: Real estate market analysis and reports. Use when asked about market conditions, neighborhood analysis, comp analysis, pricing trends, rent vs buy analysis, market reports, or any real estate market research.
---

# Real Estate Market Analysis Skill

## When to Use

Any request involving market research or analysis:

- "What's the market like in [area]?"
- "Pull comps for [address]"
- "Neighborhood analysis for [area]"
- "Is [area] a buyer's or seller's market?"
- "Rent vs buy in [city]"
- "Market report for [zip code]"

## Analysis Types

### 1. Comparable Sales Analysis (Comps)

Pull 5-10 comparable recent sales:

- Within 0.5-1 mile radius
- Sold within last 6 months (extend to 12 if insufficient)
- Similar: sqft (±20%), beds/baths (±1), year built (±15 years), condition
- Same property type and zoning

**Output table:**

```
| Address | Sold Date | Sold Price | $/SF | Beds | Baths | SF | Year | DOM | Adjustments |
```

**Adjustments to note:**

- Pool (+/- based on market)
- Garage (per stall value)
- Lot size premium/discount
- Condition (updated vs original)
- View premium

**Sources:** Zillow sold listings, Redfin sold, Realtor.com, county recorder

### 2. Market Snapshot Report

For a given area (zip, city, or neighborhood):

**Metrics to pull:**

- Median sale price (current + YoY change)
- Median price per sqft
- Average days on market (DOM)
- Months of inventory (active listings ÷ monthly sales)
- List-to-sale price ratio
- New listings (30-day count)
- Pending sales (30-day count)
- Price reductions (% of active listings reduced)
- Absorption rate

**Market classification:**
| Months of Inventory | Market Type |
|---------------------|-------------|
| < 3 months | Strong seller's market |
| 3-4 months | Seller's market |
| 4-6 months | Balanced |
| 6-8 months | Buyer's market |
| > 8 months | Strong buyer's market |

**Sources:** Redfin Data Center, Zillow Research, Realtor.com data, Altos Research, local MLS stats

### 3. Neighborhood Analysis

Comprehensive neighborhood profile:

- **Demographics**: Population, median income, median age, growth rate
- **Schools**: Ratings (GreatSchools), school district, proximity
- **Safety**: Crime stats relative to city average
- **Commute**: Drive time to major employment centers
- **Amenities**: Walk Score, Transit Score, Bike Score, nearby retail/dining
- **Development**: Planned developments, zoning changes, infrastructure projects
- **Market trends**: 1/3/5 year price trends, rental trends
- **Investment signals**: Rent-to-price ratio, cap rate range, vacancy rate

**Sources:** Census data, GreatSchools, WalkScore, CrimeMapping, city planning dept, Zillow/Redfin neighborhood pages

### 4. Rent vs Buy Analysis

Compare renting vs buying for a specific price point and area:

**Inputs needed:**

- Purchase price
- Down payment %
- Interest rate (use current 30yr fixed)
- Property tax rate
- Insurance estimate
- HOA (if applicable)
- Comparable rent for similar property
- Expected appreciation rate
- Investment return on down payment (opportunity cost)

**Output:**

- Monthly cost of owning (PITI + maintenance + opportunity cost)
- Monthly cost of renting
- Breakeven timeline
- 5-year and 10-year wealth comparison
- Price-to-rent ratio (>20 = rent favored, <15 = buy favored)

### 5. Investment Analysis

For rental/investment properties:

**Metrics:**

- **Cap Rate**: NOI ÷ Purchase Price
- **Cash-on-Cash Return**: Annual Cash Flow ÷ Total Cash Invested
- **Gross Rent Multiplier**: Purchase Price ÷ Annual Gross Rent
- **1% Rule**: Monthly Rent ≥ 1% of Purchase Price
- **DSCR**: NOI ÷ Annual Debt Service
- **50% Rule estimate**: Operating expenses ≈ 50% of gross rent
- **Pro forma cash flow**: Gross rent - vacancy - expenses - debt service

## Research Protocol

### 1. Create Task

```bash
taskman create --name "RE Market: <type> - <area>" --description "<what to analyze>" --priority high
```

### 2. Spawn Subagent (for comprehensive reports)

```
sessions_spawn(
  task: "TASK_ID=<id>. Real estate market analysis.

ANALYSIS TYPE: <type>
AREA: <area/address>
<additional criteria>

Use exa-search and agent-browser to pull data from:
- Zillow, Redfin, Realtor.com for listings/sales/market stats
- Census.gov for demographics
- GreatSchools for school ratings
- WalkScore for walkability
- County assessor for tax records and property details

Save report to ~/openclaw/workspace/research_output/re_market_<area>_<date>.md
Checkpoint progress with taskman.",
  label: "re-market-<area>",
  mode: "run",
  runTimeoutSeconds: 600
)
```

### 3. Quick Lookups (no subagent needed)

For simple questions ("what's median price in 85251?"), search directly:

```bash
python3 ~/.openclaw/workspace/skills/exa-search/scripts/search.py --query "median home price 85251 2024" --count 5
```

## Output Format

**Reports:** Save as Markdown to `~/openclaw/workspace/research_output/re_market_<area>_<date>.md`

**Quick answers:** Provide inline with source attribution.

**Tables:** Use clean markdown tables. On Discord/WhatsApp, use bullet lists instead.

## Rules

- Always cite data sources and note data freshness (date pulled).
- Distinguish between list price and sold price — never conflate them.
- Note sample size when presenting averages (median of 3 sales ≠ median of 300).
- For comps, always note if adjusted or unadjusted.
- Don't make appreciation predictions — present historical trends and let the user decide.
- Flag any data that seems anomalous (outlier sales, atypical properties in comp set).
