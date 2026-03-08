---
name: re-openhouse
description: Open house management — sign-in sheet processing, lead categorization, automated follow-up sequences, visitor tracking, and post-open-house reporting. Use when asked about open house prep, processing sign-in data, or following up with open house visitors.
---

# Open House Management Skill

## When to Use

Any open house related request:

- "Process these open house sign-ins"
- "Follow up with my open house visitors"
- "Prep checklist for my open house Saturday"
- "Categorize these open house leads"
- "Open house report for [address]"
- "How many visitors at my open houses this month?"

## Pre-Open House

### Preparation Checklist

```markdown
## Open House Prep: [Address] — [Date] [Time]

### Marketing (1-2 weeks before)

- [ ] MLS open house scheduled
- [ ] Zillow/Redfin/Realtor.com listing updated with open house
- [ ] Social media posts scheduled (IG, FB — see re-social skill)
- [ ] Neighborhood door-knock or postcard drop (50-100 homes)
- [ ] Email blast to database
- [ ] Directional signs ordered/confirmed

### Property Prep (day before / morning of)

- [ ] Seller out of property (with pets)
- [ ] All lights on, blinds open
- [ ] Temperature comfortable
- [ ] Fresh flowers / staging touches
- [ ] Clean and decluttered
- [ ] Neutral scent (no candles — allergy risk)
- [ ] Lock all valuables / medications
- [ ] Lock/disable security cameras (or post notice)

### Agent Prep

- [ ] Sign-in system ready (tablet or paper)
- [ ] Business cards
- [ ] Property flyers / brochures
- [ ] Comparable sales printout
- [ ] Neighborhood guide
- [ ] Bottled water / light refreshments
- [ ] Directional signs placed
- [ ] Feedback forms for buyers
```

## Sign-In Processing

### Input Formats

Accept sign-in data in any format:

- Photo of paper sign-in sheet → transcribe
- CSV/spreadsheet export from digital sign-in app
- Text dump of names/emails/phones
- Raw data pasted in

### Data Extraction

From sign-in data, extract and normalize:

```markdown
| #   | Name   | Phone   | Email   | Agent? | Pre-Approved? | Looking to Buy? | Timeline   | Notes   |
| --- | ------ | ------- | ------- | ------ | ------------- | --------------- | ---------- | ------- |
| 1   | [name] | [phone] | [email] | [Y/N]  | [Y/N/Unknown] | [Y/N]           | [timeline] | [notes] |
```

### Lead Categorization

Categorize each visitor into a follow-up tier:

| Tier            | Criteria                                                   | Follow-Up              |
| --------------- | ---------------------------------------------------------- | ---------------------- |
| **A — Hot**     | Pre-approved, actively looking, no agent, within timeline  | Call within 2 hours    |
| **B — Warm**    | Interested but not pre-approved, or has agent but browsing | Email within 24 hours  |
| **C — Curious** | Neighbors, not looking to buy, just browsing               | Add to nurture list    |
| **D — Agent**   | Buyer's agent previewing for client                        | Professional follow-up |
| **X — Skip**    | Incomplete info, illegible, or clearly not a lead          | No follow-up           |

**Categorization signals:**

- Has a buyer's agent → Tier B or D (respect the relationship)
- Pre-approved + no agent + timeline < 6 months → Tier A
- "Just looking" + neighbor → Tier C (but may refer or sell their own home)
- Asked detailed questions about price/terms → Tier A or B
- Left quickly, minimal interaction → Tier C

## Follow-Up Sequences

### Tier A — Hot Lead (use re-client skill for full sequences)

```
Hour 0-2: Phone call
  "Hi [Name], this is [Agent] from today's open house at [Address].
   Great to meet you! I noticed you seemed interested — do you have
   a few minutes to chat about what you're looking for?"

Hour 2-4 (if no answer): Text
  "Hey [Name]! [Agent] here from the open house at [Address].
   Would love to chat about the property or help you find something
   similar. What works for you?"

Day 1: Email with property details + similar listings

Day 3: Market data for their area of interest

Day 7: Check-in + new listings matching criteria
```

### Tier B — Warm Lead

```
Day 0: Email
  Subject: Great meeting you at [Address]!

  [Personalized recap of conversation + property highlights +
   offer to help with search even if they have an agent]

Day 3: Similar listings email

Day 7: Market insight for their area of interest

Day 14: Soft check-in
```

### Tier C — Nurture (Neighbors)

```
Day 1: Email
  Subject: Thanks for stopping by [Address]!

  [Friendly neighbor email — "If you know anyone looking to move
   to the neighborhood, I'd love to help" + market value update
   for their home if they're curious]

Add to quarterly sphere touches.
```

## Post-Open House Report

```markdown
## Open House Report: [Address]

**Date:** [date] | **Time:** [start]-[end]
**Weather:** [conditions]

### Attendance

- Total visitors: [N]
- Unique groups/parties: [N]
- Represented by agents: [N]

### Lead Breakdown

| Tier              | Count | %    |
| ----------------- | ----- | ---- |
| A — Hot           | [N]   | [X]% |
| B — Warm          | [N]   | [X]% |
| C — Nurture       | [N]   | [X]% |
| D — Agent Preview | [N]   | [X]% |

### Feedback Themes

**Positive:**

- [What visitors liked — mentioned X times]

**Concerns:**

- [What concerned visitors — mentioned X times]

**Price Perception:**

- [x] said well priced
- [x] said high
- [x] no comment

### Follow-Up Status

| Name   | Tier | Follow-Up      | Status    |
| ------ | ---- | -------------- | --------- |
| [name] | A    | Called [date]  | [outcome] |
| [name] | B    | Emailed [date] | [pending] |

[etc]

### Recommendations

- [Tactical recommendation based on turnout and feedback]
- [Price/staging/marketing adjustment if needed]

### Comparison to Previous Open Houses

| Date   | Visitors | A-Tier | Offers |
| ------ | -------- | ------ | ------ |
| [date] | [N]      | [N]    | [N]    |
| [date] | [N]      | [N]    | [N]    |
```

## Storage

Save open house data to:

```
~/openclaw/workspace/transactions/[address-slug]-openhouse-[date].md
```

## Rules

- Call Tier A leads within 2 hours — speed to lead is everything.
- Always respect existing agent relationships — if visitor has an agent, communicate professionally.
- Never pressure or hard-sell at an open house — be helpful, knowledgeable, approachable.
- Keep sign-in data secure — it contains PII (names, phones, emails).
- Track conversion: open house visitor → client → closing. This data informs whether open houses are worth the time.
- For paper sign-ins with illegible handwriting, note what's readable and mark the rest as unclear.
