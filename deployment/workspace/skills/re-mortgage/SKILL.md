---
name: re-mortgage
description: Mortgage calculations — monthly payment estimates, affordability analysis, rate comparison scenarios, amortization, refinance analysis, and buyer pre-qualification sanity checks. Use when asked about mortgage payments, affordability, loan scenarios, or financing questions.
---

# Mortgage Calculator Skill

## When to Use

Any financing/payment question:

- "What's the payment on a $500K house?"
- "Can my buyer afford $600K?"
- "Compare 30yr vs 15yr"
- "Rate buydown analysis"
- "Should they refinance?"
- "FHA vs conventional for [scenario]"
- "How much house can they afford with $X income?"

## Core Calculations

### Monthly Payment (PITI)

```
P&I = Loan Amount × [r(1+r)^n] / [(1+r)^n - 1]
  where r = monthly rate (annual ÷ 12), n = total payments (years × 12)

Monthly Tax = Annual Property Tax ÷ 12
Monthly Insurance = Annual Homeowner's Insurance ÷ 12
Monthly PMI = (Loan Amount × PMI Rate) ÷ 12  [if LTV > 80%]
Monthly HOA = HOA Dues (if applicable)

PITI = P&I + Tax + Insurance + PMI + HOA
```

### Quick Estimates (when details unavailable)

| Component    | Rule of Thumb                                                |
| ------------ | ------------------------------------------------------------ |
| Property Tax | 1.0-1.5% of purchase price annually (varies wildly by state) |
| Insurance    | 0.35-0.75% of purchase price annually                        |
| PMI          | 0.5-1.5% of loan amount annually (depends on LTV and credit) |

**State tax rate examples:**
| State | Effective Rate |
|-------|---------------|
| TX | ~1.8% |
| NJ | ~2.2% |
| AZ | ~0.6% |
| CA | ~0.75% |
| FL | ~0.9% |
| IL | ~2.1% |
| NY | ~1.7% |

### Affordability (How Much House)

**Income-based:**

```
Max Monthly Housing = Gross Monthly Income × 0.28 (front-end DTI)
Max Monthly Debt = Gross Monthly Income × 0.36 (back-end DTI)
Max Housing Payment = Max Monthly Debt - Existing Monthly Debts

Work backwards from max payment to loan amount:
Max Loan = Payment × [(1+r)^n - 1] / [r(1+r)^n]
Max Purchase = Max Loan + Down Payment
```

**DTI limits by loan type:**
| Loan Type | Front-End DTI | Back-End DTI |
|-----------|--------------|-------------|
| Conventional | 28% | 36-45% |
| FHA | 31% | 43-50% |
| VA | No limit | 41% (guideline) |
| USDA | 29% | 41% |

### Loan Type Comparison

| Feature          | Conventional                | FHA                         | VA                            | USDA             |
| ---------------- | --------------------------- | --------------------------- | ----------------------------- | ---------------- |
| Min Down Payment | 3-5%                        | 3.5%                        | 0%                            | 0%               |
| Credit Score     | 620+                        | 580+ (3.5%), 500+ (10%)     | No minimum (lenders use 620+) | 640+             |
| PMI/MIP          | PMI until 80% LTV           | MIP for life (if <10% down) | No PMI (funding fee instead)  | Guarantee fee    |
| Loan Limit       | Conforming: $766,550 (2024) | Area-specific               | No limit                      | Area-specific    |
| Property Types   | Most                        | Owner-occupied, 1-4 units   | Owner-occupied                | Rural areas      |
| Upfront Costs    | None                        | 1.75% UFMIP                 | 1.25-3.3% funding fee         | 1% guarantee fee |

### Rate Buydown Analysis

**Temporary buydown (seller-paid):**

```
2-1 Buydown:
  Year 1: Rate - 2% → Payment = $[X] (savings: $[X]/mo)
  Year 2: Rate - 1% → Payment = $[X] (savings: $[X]/mo)
  Year 3+: Full rate → Payment = $[X]
  Total buydown cost = Sum of payment differences
```

**Permanent buydown (points):**

```
Cost per point = 1% of loan amount
Rate reduction = ~0.25% per point (varies by lender)
Monthly savings = [payment at higher rate] - [payment at lower rate]
Breakeven = Point cost ÷ Monthly savings = [X] months
```

### Refinance Analysis

```
Current Payment: $[X]
New Payment: $[X]
Monthly Savings: $[X]
Closing Costs: $[X]
Breakeven: Closing Costs ÷ Monthly Savings = [X] months
Remaining Loan Term Savings: Monthly Savings × Remaining Months - Closing Costs
```

**Refinance rules of thumb:**

- Worth it if: rate drop ≥ 0.5-0.75% AND you'll stay past breakeven
- Cash-out refi: typically max 80% LTV, higher rate than rate-and-term
- Don't restart 30yr if you've made significant progress on current loan (compare total interest)

## Output Format

### Payment Estimate

```markdown
## Payment Estimate: $[Purchase Price]

### Loan Details

|                |                       |
| -------------- | --------------------- |
| Purchase Price | $[X]                  |
| Down Payment   | $[X] ([X]%)           |
| Loan Amount    | $[X]                  |
| Interest Rate  | [X]%                  |
| Loan Term      | [X] years             |
| Loan Type      | [Conventional/FHA/VA] |

### Monthly Payment Breakdown

| Component             | Amount   |
| --------------------- | -------- |
| Principal & Interest  | $[X]     |
| Property Tax          | $[X]     |
| Homeowner's Insurance | $[X]     |
| PMI/MIP               | $[X]     |
| HOA                   | $[X]     |
| **Total PITI**        | **$[X]** |

### Affordability Check

| Metric                    | Value   | Guideline               |
| ------------------------- | ------- | ----------------------- |
| Required Income (28% DTI) | $[X]/yr | Min gross income needed |
| Front-End DTI             | [X]%    | Target: ≤28%            |
| Back-End DTI              | [X]%    | Target: ≤36-43%         |

### Cash to Close (Estimated)

| Item                                     | Amount   |
| ---------------------------------------- | -------- |
| Down Payment                             | $[X]     |
| Closing Costs (~2-3%)                    | $[X]     |
| Prepaid Items (~6mo tax + 1yr insurance) | $[X]     |
| **Total Cash Needed**                    | **$[X]** |
```

### Scenario Comparison

```markdown
## Loan Scenario Comparison: $[Purchase Price]

|                               | Scenario A  | Scenario B  | Scenario C  |
| ----------------------------- | ----------- | ----------- | ----------- |
| Down Payment                  | [X]% ($[X]) | [X]% ($[X]) | [X]% ($[X]) |
| Loan Amount                   | $[X]        | $[X]        | $[X]        |
| Rate                          | [X]%        | [X]%        | [X]%        |
| Term                          | [X] yr      | [X] yr      | [X] yr      |
| Monthly P&I                   | $[X]        | $[X]        | $[X]        |
| Monthly PITI                  | $[X]        | $[X]        | $[X]        |
| PMI                           | $[X]        | $[X]        | $[X]        |
| Total Interest (life of loan) | $[X]        | $[X]        | $[X]        |
| Cash to Close                 | $[X]        | $[X]        | $[X]        |
```

## Rules

- Always note that these are ESTIMATES — actual terms depend on lender, credit, and market.
- Never guarantee rates — always say "at [X]% rate" and note rates change daily.
- Include property tax and insurance in every payment estimate — P&I alone is misleading.
- Round monthly payments to nearest dollar for readability.
- When comparing scenarios, highlight the tradeoff (lower payment vs total interest vs cash needed).
- For current rate data, note the date and source.
- This is NOT financial advice — recommend buyers work with a licensed mortgage professional.
- Flag when a buyer's DTI is borderline — lender may decline even if numbers technically work.
