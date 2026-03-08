---
name: re-deals
description: Real estate deal analysis — ROI calculations, cap rate, cash flow projections, rehab estimates, ARV analysis, wholesale deal analysis, BRRRR analysis, and rental yield calculations. Use when asked to analyze a real estate deal or investment property.
---

# Real Estate Deal Analysis Skill

## When to Use

Any investment/deal analysis request:

- "Analyze this deal at [address]"
- "Run the numbers on [property]"
- "What's the cap rate on this?"
- "Is this a good flip?"
- "BRRRR analysis for [property]"
- "Wholesale deal — what's my MAO?"
- "Cash flow projection for [rental]"

## Input Requirements

Minimum needed:

- **Purchase price** (or asking price)
- **Property type** (SFR, duplex, triplex, quad, commercial)
- **Rent estimates** (actual or market rate)
- **Property condition** (turnkey, light rehab, heavy rehab, gut)

Nice to have:

- Address (to pull tax records, comps, rent comps)
- Actual expenses (taxes, insurance, HOA, utilities)
- Rehab scope/estimate
- Financing terms (down payment, rate, term)

If details are missing, use exa-search and agent-browser to pull from Zillow/Redfin/county records.

## Analysis Frameworks

### 1. Buy & Hold (Rental) Analysis

**Income:**

- Gross Scheduled Rent (monthly × 12)
- Other income (laundry, parking, storage, pet fees)
- Less: Vacancy (market-dependent, typically 5-8%)
- = Effective Gross Income (EGI)

**Expenses (use actuals when available, otherwise estimate):**
| Expense | Rule of Thumb |
|---------|--------------|
| Property taxes | Pull from county assessor |
| Insurance | 0.5-1% of property value annually |
| Maintenance/repairs | 5-10% of gross rent |
| Capital expenditure reserves | 5-10% of gross rent |
| Property management | 8-10% of collected rent (even if self-managing) |
| HOA | Actual or $0 |
| Utilities (owner-paid) | Actual or estimate |
| Lawn/snow | Actual or estimate |

**Total Operating Expenses**
**Net Operating Income (NOI)** = EGI - Operating Expenses

**Debt Service:**

- Monthly mortgage payment (P&I)
- Annual debt service = monthly × 12

**Cash Flow** = NOI - Annual Debt Service
**Monthly Cash Flow** = Cash Flow ÷ 12

**Key Metrics:**

```
Cap Rate = NOI ÷ Purchase Price
Cash-on-Cash Return = Annual Cash Flow ÷ Total Cash Invested
Gross Rent Multiplier = Purchase Price ÷ Annual Gross Rent
DSCR = NOI ÷ Annual Debt Service
1% Rule = Monthly Rent ÷ Purchase Price (target ≥ 1%)
50% Rule Check = Operating Expenses ÷ Gross Rent (should be ~50%)
Price Per Unit = Purchase Price ÷ Number of Units
Price Per SF = Purchase Price ÷ Square Footage
```

**Deal Quality Benchmarks:**
| Metric | Good | Great | Walk Away |
|--------|------|-------|-----------|
| Cap Rate | 6-8% | 8%+ | <5% |
| Cash-on-Cash | 8-10% | 12%+ | <6% |
| DSCR | 1.2+ | 1.4+ | <1.0 |
| 1% Rule | ≥0.8% | ≥1.0% | <0.6% |
| Monthly Cash Flow/Unit | $150+ | $250+ | <$100 |

_Note: Benchmarks vary significantly by market. A 5% cap in a Class A market may be excellent._

### 2. Fix & Flip Analysis

**Acquisition:**

- Purchase price
- Closing costs (typically 2-3% of purchase price)
- Total acquisition = purchase + closing

**Rehab Budget:**
| Category | Light Rehab | Medium Rehab | Heavy Rehab |
|----------|------------|-------------|-------------|
| Cosmetic (paint, flooring, fixtures) | $5-15K | $15-30K | $30-50K |
| Kitchen | $5-10K | $15-30K | $30-60K |
| Bathrooms (per) | $3-8K | $8-15K | $15-30K |
| Roof | — | $5-12K | $8-20K |
| HVAC | — | $4-8K | $6-15K |
| Foundation | — | — | $10-30K |
| Electrical/Plumbing | — | $3-8K | $8-25K |
| Contingency | 10% | 15% | 20% |

_These are rough national averages — adjust for local market._

**Holding Costs (per month):**

- Mortgage/hard money payments
- Property taxes (monthly proration)
- Insurance
- Utilities
- Holding time estimate: Light 2-3mo, Medium 3-5mo, Heavy 5-8mo

**Sale:**

- After Repair Value (ARV) — based on comps of similar renovated properties
- Agent commission (5-6% of sale price)
- Seller closing costs (1-2%)
- Transfer taxes (varies by state)

**Profit Calculation:**

```
Total Investment = Acquisition + Rehab + Holding Costs
Net Sale Proceeds = ARV - Commission - Closing Costs - Transfer Tax
Profit = Net Sale Proceeds - Total Investment
ROI = Profit ÷ Total Investment
Annualized ROI = ROI × (12 ÷ Holding Months)
```

**70% Rule (max purchase price):**

```
MAO = (ARV × 0.70) - Rehab Cost
```

### 3. BRRRR Analysis

Buy, Rehab, Rent, Refinance, Repeat:

**Phase 1 — Buy + Rehab:** Same as flip analysis for acquisition + rehab costs.

**Phase 2 — Rent:** Same as buy & hold analysis for income/expenses.

**Phase 3 — Refinance:**

- Appraised value after rehab (= ARV)
- New loan amount = ARV × LTV (typically 70-75%)
- Cash out = New loan - Original loan payoff
- Cash left in deal = Total invested - Cash out

**BRRRR Success Metrics:**

```
Cash Left in Deal — target: $0 or negative (money back + equity)
Cash-on-Cash Return on Cash Left — if $0 left = infinite
Equity Created = ARV - New Loan Balance
Monthly Cash Flow (post-refi)
```

### 4. Wholesale Analysis

**Maximum Allowable Offer (MAO):**

```
MAO = (ARV × 0.70) - Rehab Cost - Wholesale Fee
```

**Wholesale Fee:** Typically $5K-$15K for SFR, more for larger deals.

**Assignment vs Double Close:**

- Assignment: Lower cost, fee visible to all parties
- Double close: Higher cost (two sets of closing costs), fee private

**Deal qualification checklist:**

- [ ] ARV supportable by 3+ comps within 6 months
- [ ] Rehab estimate verified (walkthrough or contractor bid)
- [ ] Motivated seller (reason to sell below market)
- [ ] Title clear or clearable
- [ ] Buyer pool exists for this property type/area
- [ ] Spread is $15K+ (enough for end buyer profit + your fee)

### 5. Multi-Family / Commercial

Additional metrics for 5+ units:

```
Price Per Unit
Price Per SF
Expense Ratio = Operating Expenses ÷ EGI
Break-Even Occupancy = (Operating Expenses + Debt Service) ÷ Gross Potential Rent
Loan-to-Value = Loan Amount ÷ Purchase Price (or Appraised Value)
Debt Yield = NOI ÷ Loan Amount
```

**Value-Add Analysis:**

- Current NOI vs Pro Forma NOI (after improvements + rent increases)
- Cap rate expansion/compression in the market
- Forced appreciation = NOI increase ÷ Market Cap Rate

## Output Format

Present as a structured deal summary:

```markdown
## Deal Analysis: [Address]

### Property Overview

- Type: [SFR/Duplex/etc] | Beds/Baths: [X/Y] | SF: [N] | Year: [YYYY]
- Purchase Price: $XXX,XXX
- Condition: [Turnkey/Light Rehab/Heavy Rehab]

### Financial Summary

| Metric                                | Value |
| ------------------------------------- | ----- |
| [relevant metrics from analysis type] |

### Verdict

[GO / MAYBE / PASS] — [1-2 sentence rationale]

### Risks

- [Key risk 1]
- [Key risk 2]

### Assumptions

- [List key assumptions: vacancy rate, rent estimate source, rehab contingency, etc.]
```

## Rules

- Always state assumptions clearly — a deal analysis is only as good as its inputs.
- Use conservative estimates: higher vacancy, higher rehab, lower rents.
- Never present analysis as financial advice — it's for informational purposes.
- Pull actual tax and insurance data when possible instead of rules of thumb.
- For rehab estimates, note that they're rough — always recommend contractor bids.
- Account for ALL costs — closing costs, holding costs, and contingency are where new investors get burned.
- When comparing to benchmarks, note the market context (Class A/B/C, metro vs rural).
