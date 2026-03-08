---
name: re-showings
description: Showing feedback collection and analysis — collect buyer agent feedback after showings, identify themes, generate seller reports, and inform pricing strategy. Use when asked to collect showing feedback, summarize agent comments, or create a showing report.
---

# Showing Feedback Skill

## When to Use

Any showing-related request:

- "Summarize showing feedback for [address]"
- "Create a showing feedback form"
- "What are agents saying about [listing]?"
- "Showing report for my seller at [address]"
- "3 showings this week, here's what they said..."
- "Feedback says price is too high — how do I present this?"

## Feedback Collection

### Standard Questions

After each showing, collect:

1. **Overall impression** (1-5 stars or Excellent/Good/Fair/Poor)
2. **Price perception**: "How does the price compare to other homes your buyer is considering?"
   - Well priced / Slightly high / Overpriced / Great value
3. **Buyer interest level**: "Is your buyer interested in writing an offer?"
   - Yes, writing offer / Considering / Unlikely / No
4. **Top positives**: "What did your buyer like most?" (open text)
5. **Top concerns**: "What were your buyer's concerns?" (open text)
6. **Condition feedback**: "How would you rate the property's condition?"
   - Move-in ready / Needs minor updates / Needs significant work
7. **Would they return?**: Yes / Maybe / No
8. **Additional comments**: (open text)

### Feedback Entry Format

```markdown
### Showing: [Date] at [Time]

- Agent: [Name], [Brokerage]
- Buyer type: [First-time / Move-up / Downsizer / Investor / Relocating]
- Overall: [X/5]
- Price: [Well priced / Slightly high / Overpriced / Great value]
- Interest: [Writing offer / Considering / Unlikely / No]
- Liked: [what they liked]
- Concerns: [what concerned them]
- Condition: [Move-in ready / Minor updates / Significant work]
- Return: [Yes / Maybe / No]
- Notes: [additional comments]
```

## Analysis & Reporting

### Feedback Summary Report

After collecting 3+ showings of feedback:

```markdown
## Showing Feedback Report: [Address]

**Period:** [date range]
**Total Showings:** [N]
**Feedback Received:** [N] of [N] ([X]%)

---

### Key Metrics

| Metric           | Result                                |
| ---------------- | ------------------------------------- |
| Average Rating   | [X.X] / 5                             |
| Interest Level   | [X]% considering or writing offer     |
| Price Perception | [X]% said well priced, [X]% said high |
| Would Return     | [X]% yes or maybe                     |

---

### Themes

**What buyers love (mentioned [X]+ times):**

1. [Theme] — mentioned by [N] of [N] agents
2. [Theme] — mentioned by [N] of [N] agents
3. [Theme] — mentioned by [N] of [N] agents

**Common concerns (mentioned [X]+ times):**

1. [Concern] — mentioned by [N] of [N] agents
2. [Concern] — mentioned by [N] of [N] agents
3. [Concern] — mentioned by [N] of [N] agents

**Price feedback distribution:**

- Great value: [N] ([X]%)
- Well priced: [N] ([X]%)
- Slightly high: [N] ([X]%)
- Overpriced: [N] ([X]%)

---

### Individual Feedback

[Each showing entry]

---

### Recommendations

Based on [N] showings over [X] days:

**If feedback is positive + offers coming:**

- Hold price, market is validating the position
- [Specific tactical recommendation]

**If feedback is mixed:**

- Address the top concern if possible (staging, decluttering, minor repair)
- Monitor for [X] more showings before considering price adjustment
- [Specific recommendation]

**If feedback is negative / price concerns dominant:**

- [X]% of agents say price is high — data supports a price adjustment
- Recommended new price: $[X] (based on [rationale])
- Expected impact: increased showing activity within [X] days

---

_Report generated [date]. [N] of [N] showing agents provided feedback._
```

### Presenting Tough Feedback to Sellers

When feedback indicates price is too high:

1. **Lead with data, not opinion**: "Here's what 8 buyer agents told us..."
2. **Show the pattern**: "6 of 8 agents mentioned price as a concern"
3. **Compare to market**: Show DOM vs market average, showing count vs expected
4. **Present options**:
   - Option A: Reduce to $[X] — expected to generate [outcome]
   - Option B: Hold price, address [concern] — expected to [outcome]
   - Option C: Hold price and wait — risk is [outcome]
5. **Recommend**: "Based on the feedback, I recommend Option [X] because..."

## Storage

Save feedback to:

```
~/openclaw/workspace/transactions/[address-slug]-showings.md
```

## Rules

- Never fabricate or embellish feedback — present agent comments accurately.
- Anonymize buyer details (no names, just type: "first-time buyer", "investor").
- Agent names can be included (they're industry professionals providing professional opinions).
- When feedback contradicts agent's pricing recommendation, present both perspectives honestly.
- Track feedback over time — patterns matter more than individual comments.
- Follow up with showing agents who didn't respond after 48 hours.
- For vacant properties, note that staging feedback is common and actionable.
