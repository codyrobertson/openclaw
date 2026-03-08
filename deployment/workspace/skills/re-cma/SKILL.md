---
name: re-cma
description: Comparative Market Analysis (CMA) generator — pull comps, apply adjustments, calculate adjusted value range, and produce a polished report for seller listing appointments or buyer offer strategy. Use when asked to create a CMA, pull comps, or estimate property value.
---

# CMA Generator Skill

## When to Use

Any comp-based valuation request:

- "CMA for [address]"
- "What's [address] worth?"
- "Pull comps for [property]"
- "I have a listing appointment at [address]"
- "Comp analysis for [neighborhood]"
- "What should we offer on [address]?"

## CMA Process

### Step 1: Subject Property Profile

Gather subject property details (use re-property skill or listing data):

- Address
- Property type (SFR, condo, townhome, multi-family)
- Beds / baths
- Living area (sqft)
- Lot size
- Year built
- Condition (poor, fair, average, good, excellent)
- Features (pool, garage, view, upgrades)

### Step 2: Pull Comparables

**Search criteria:**

- Radius: 0.25 mile first, expand to 0.5, then 1 mile if insufficient
- Time: Sold within 90 days first, expand to 180, then 365 if insufficient
- Target: 5-7 strong comps (minimum 3)
- Match: Same property type, similar sqft (±20%), similar beds (±1), similar age (±15 years)

**Use re-scrape skill:**

```bash
CURL_CA_BUNDLE=/etc/ssl/cert.pem python3 \
  ~/.openclaw/workspace/skills/re-scrape/scripts/listings.py \
  zillow "[area]" --type sold --output json
```

**Comp quality tiers:**
| Tier | Criteria |
|------|----------|
| A (Best) | Same subdivision, <0.25mi, <90 days, ±10% sqft |
| B (Good) | Same neighborhood, <0.5mi, <180 days, ±15% sqft |
| C (Acceptable) | Similar area, <1mi, <365 days, ±20% sqft |
| D (Weak) | Use only if nothing better; note limitations |

### Step 3: Apply Adjustments

Standard adjustment grid:

| Feature                   | Adjustment Method                             |
| ------------------------- | --------------------------------------------- |
| Living area (sqft)        | $/sqft × difference (use market $/sqft)       |
| Bedrooms                  | $5K-$15K per bedroom (market-dependent)       |
| Bathrooms                 | $5K-$10K per bathroom                         |
| Garage                    | $5K-$15K per stall                            |
| Pool                      | $10K-$25K (market-dependent, can be negative) |
| Lot size                  | $/sqft for land × difference                  |
| Age/condition             | $5K-$25K per tier difference                  |
| View/location             | $10K-$50K+ (highly variable)                  |
| Upgrades (kitchen, baths) | 50-75% of renovation cost                     |
| Basement (finished)       | $20-$40/sqft                                  |

**Adjustment rules:**

- Net adjustment should not exceed 15% of comp sale price
- Gross adjustment should not exceed 25% of comp sale price
- If adjustments exceed these, the comp is too dissimilar — find a better one
- Adjust comp TO subject (if comp has pool and subject doesn't, subtract pool value from comp)

### Step 4: Calculate Value Range

```
Adjusted Comp Values → sort low to high
Weighted Average = (Tier A comps × 3 + Tier B × 2 + Tier C × 1) ÷ total weight
Suggested Range = Weighted Average ± 3-5%
```

**Price positioning strategy:**
| Strategy | Position | When to Use |
|----------|----------|-------------|
| Aggressive | Top of range | Hot market, unique features, motivated buyer pool |
| Market | Middle of range | Balanced market, standard property |
| Conservative | Bottom of range | Slow market, needs repairs, quick sale needed |
| Below market | Below range | Multiple offer strategy, estate sale, investor flip |

### Step 5: Active & Pending Context

Also pull currently active and pending listings to show:

- What the competition looks like (active)
- What buyers are currently willing to pay (pending)
- Days on market for active listings (absorption rate signal)

## Output Format

```markdown
# Comparative Market Analysis

## [Subject Address]

**Prepared for:** [Client Name]
**Prepared by:** [Agent Name]
**Date:** [Date]

---

### Subject Property

| Detail      | Value                     |
| ----------- | ------------------------- |
| Type        | [SFR/Condo/etc]           |
| Beds/Baths  | [X/Y]                     |
| Living Area | [N] sqft                  |
| Lot Size    | [N] sqft                  |
| Year Built  | [YYYY]                    |
| Condition   | [description]             |
| Features    | [pool, garage, view, etc] |

---

### Comparable Sales

#### Comp 1: [Address] ⭐ Tier [A/B/C]

|                    | Comp      | Subject | Adjustment    |
| ------------------ | --------- | ------- | ------------- |
| Sale Price         | $[amount] | —       | —             |
| Sale Date          | [date]    | —       | —             |
| Distance           | [X] mi    | —       | —             |
| Sqft               | [N]       | [N]     | $[±amount]    |
| Beds/Baths         | [X/Y]     | [X/Y]   | $[±amount]    |
| Garage             | [Y/N]     | [Y/N]   | $[±amount]    |
| Pool               | [Y/N]     | [Y/N]   | $[±amount]    |
| Condition          | [desc]    | [desc]  | $[±amount]    |
| **Adjusted Price** |           |         | **$[amount]** |
| Adjusted $/sqft    |           |         | $[amount]     |

[Repeat for each comp]

---

### Adjustment Summary

| Comp | Address | Sale Price | Net Adj | Adj Price | $/sqft | Tier    |
| ---- | ------- | ---------- | ------- | --------- | ------ | ------- |
| 1    | [addr]  | $[X]       | $[±X]   | $[X]      | $[X]   | [A/B/C] |
| 2    | [addr]  | $[X]       | $[±X]   | $[X]      | $[X]   | [A/B/C] |

[etc]

---

### Market Context

**Active Listings (Competition):**
| Address | List Price | DOM | Beds/Baths | Sqft |
|---------|-----------|-----|-----------|------|
[3-5 active listings]

**Pending Sales:**
| Address | List Price | DOM before Pending | Beds/Baths | Sqft |
|---------|-----------|-------------------|-----------|------|
[if available]

---

### Suggested Value Range

|                 | Price         | $/sqft        |
| --------------- | ------------- | ------------- |
| Low             | $[amount]     | $[amount]     |
| **Recommended** | **$[amount]** | **$[amount]** |
| High            | $[amount]     | $[amount]     |

**Positioning recommendation:** [Aggressive/Market/Conservative] — [rationale]

---

### Market Indicators

- Median DOM: [X] days
- List-to-sale ratio: [X]%
- Months of inventory: [X]
- Market type: [Seller's/Balanced/Buyer's]

---

_This CMA is for informational purposes and is not a formal appraisal. Market conditions can change rapidly. Data sourced from [sources] on [date]._
```

## Rules

- Always show your adjustment math — a CMA without visible adjustments is just guessing.
- Never present a single point value without a range.
- Note comp quality tier for each comparable.
- Flag any comps with unusual circumstances (estate sale, REO, investor flip, related party).
- Distinguish between list price and sold price throughout.
- Note when data is limited (few comps, old sales, wide search radius).
- For luxury or unique properties, note that CMA accuracy decreases with fewer comps.
- Present to client: lead with the recommended value, then support with data.
