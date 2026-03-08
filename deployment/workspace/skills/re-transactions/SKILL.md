---
name: re-transactions
description: Real estate transaction management — track deals through the pipeline, manage deadlines, contingency dates, document checklists, and milestone tracking from contract to close. Use when asked to track a deal, manage transaction timelines, or check on closing deadlines.
---

# Transaction Tracker Skill

## When to Use

Any transaction management request:

- "Track this deal at [address]"
- "When is the inspection deadline for [address]?"
- "What's the status of my deals?"
- "Create a closing checklist for [address]"
- "What deadlines are coming up?"
- "Update [address] — appraisal came in"

## Transaction Pipeline Stages

```
Prospect → Under Contract → Due Diligence → Clear to Close → Closed
```

### Stage Details

**1. Prospect / Pre-Contract**

- Showing scheduled/completed
- Offer drafted
- Offer submitted
- Counter-offer round(s)
- Offer accepted → move to Under Contract

**2. Under Contract**

- Earnest money deposited
- Title ordered
- Home inspection scheduled
- Disclosure review period

**3. Due Diligence**

- Home inspection completed
- Repair negotiations
- Appraisal ordered
- Appraisal completed
- Loan underwriting
- Survey (if required)
- HOA document review (if applicable)
- Insurance bound

**4. Clear to Close**

- Final loan approval (clear to close letter)
- Closing disclosure reviewed (3-day rule)
- Final walkthrough scheduled
- Closing scheduled
- Wire instructions received

**5. Closed**

- Documents signed
- Funds disbursed
- Keys delivered
- Commission received
- Post-close follow-up scheduled

## Critical Deadlines

Standard contract deadlines (adjust per your state/contract):

| Deadline              | Typical Timeframe                  | Consequence if Missed           |
| --------------------- | ---------------------------------- | ------------------------------- |
| Earnest money deposit | 1-3 business days after acceptance | Breach of contract              |
| Inspection period     | 10-17 days from acceptance         | Lose right to negotiate repairs |
| Inspection objection  | Within inspection period           | Acceptance of condition         |
| Appraisal contingency | 21-30 days                         | Lose right to renegotiate price |
| Loan commitment       | 21-30 days                         | Seller can terminate            |
| Closing date          | 30-45 days from acceptance         | Breach / per diem penalties     |
| Final walkthrough     | 1-3 days before closing            | Proceed without inspection      |

**State-specific notes:**

- AZ: BINSR (Buyer's Inspection Notice and Seller's Response) — 10-day default
- CA: 17-day default contingency period
- TX: Option period (typically 7-10 days, buyer pays option fee)
- FL: 15-day inspection period default
- Always verify against the actual executed contract

## Transaction Record Format

```markdown
## Transaction: [Address]

### Status: [Stage]

**Contract Date:** [date]
**Closing Date:** [target date]
**Days Until Close:** [N]

### Parties

- Buyer: [name] | Agent: [name] | Lender: [name]
- Seller: [name] | Agent: [name]
- Title: [company] | Escrow Officer: [name]

### Financial

- Purchase Price: $[amount]
- Earnest Money: $[amount] — [deposited/pending]
- Loan Type: [conventional/FHA/VA/cash]
- Down Payment: [X]%

### Key Dates

| Milestone           | Date   | Status     |
| ------------------- | ------ | ---------- |
| Contract signed     | [date] | ✅         |
| Earnest money due   | [date] | [✅/⏳/⚠️] |
| Inspection deadline | [date] | [✅/⏳/⚠️] |
| Appraisal deadline  | [date] | [✅/⏳/⚠️] |
| Loan commitment     | [date] | [✅/⏳/⚠️] |
| Closing disclosure  | [date] | [✅/⏳/⚠️] |
| Final walkthrough   | [date] | [✅/⏳/⚠️] |
| Closing             | [date] | [✅/⏳/⚠️] |

### Document Checklist

- [ ] Executed purchase agreement
- [ ] Earnest money receipt
- [ ] Seller disclosures
- [ ] Title commitment
- [ ] Home inspection report
- [ ] Repair addendum (if applicable)
- [ ] Appraisal report
- [ ] Loan approval / commitment letter
- [ ] Homeowner's insurance binder
- [ ] HOA docs (if applicable)
- [ ] Survey (if applicable)
- [ ] Closing disclosure (buyer + seller)
- [ ] Wire instructions
- [ ] Final walkthrough confirmation
- [ ] Settlement statement (HUD-1 / CD)

### Notes / Issues

- [date]: [note]
```

## Pipeline Dashboard

When asked for a status overview of all deals:

```markdown
## Active Transactions — [Date]

| #   | Address | Stage   | Price | Close Date | Days Left | Next Action |
| --- | ------- | ------- | ----- | ---------- | --------- | ----------- |
| 1   | [addr]  | [stage] | $[X]  | [date]     | [N]       | [action]    |
| 2   | [addr]  | [stage] | $[X]  | [date]     | [N]       | [action]    |

### Upcoming Deadlines (Next 7 Days)

| Date   | Address | Deadline   | Action Required |
| ------ | ------- | ---------- | --------------- |
| [date] | [addr]  | [deadline] | [what to do]    |

### Alerts

- ⚠️ [address]: [deadline] expires in [N] days — [action needed]
- ⚠️ [address]: [issue] — [recommendation]
```

## Storage

Save transaction records to:

```
~/openclaw/workspace/transactions/[address-slug].md
```

Pipeline dashboard:

```
~/openclaw/workspace/transactions/_pipeline.md
```

## Automations

### Deadline Alerts

When a transaction is tracked, calculate all deadline dates from the contract date and flag:

- **Red (⚠️)**: Deadline within 2 business days
- **Yellow (⏳)**: Deadline within 5 business days
- **Green (✅)**: Complete or >5 business days out

### Post-Close Triggers

After marking a transaction as Closed:

1. Schedule 30-day check-in (re-client skill)
2. Add to sphere database for quarterly touches
3. Request review/testimonial email
4. Calculate final commission and net

## Rules

- Always use calendar days unless contract specifies business days.
- Weekends and holidays matter — know your state's rules on deadline calculation.
- When in doubt about a deadline, flag it early rather than late.
- Keep notes timestamped — if a dispute arises, the timeline matters.
- Never share transaction details with unauthorized parties.
- Commission calculations are estimates until the settlement statement is final.
