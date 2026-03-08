---
name: re-compliance
description: Real estate compliance checker — Fair Housing Act review, advertising compliance, MLS accuracy, state-specific disclosure requirements, and marketing material audit. Use when asked to review listing copy, check marketing compliance, or audit communications for Fair Housing violations.
---

# Compliance Checker Skill

## When to Use

Any compliance review request:

- "Review this listing for Fair Housing"
- "Is this description compliant?"
- "Check my marketing email"
- "Audit these social media posts"
- "Fair Housing review for [copy]"
- "Am I allowed to say [phrase]?"
- Also proactively when generating listing copy or marketing content

## Fair Housing Act (FHA) — Core Rules

### Protected Classes (Federal)

It is illegal to discriminate based on:

1. **Race**
2. **Color**
3. **National Origin**
4. **Religion**
5. **Sex** (includes sexual orientation and gender identity per 2021 HUD guidance)
6. **Familial Status** (families with children under 18, pregnant women)
7. **Disability** (physical or mental)

**State/local additions may include:** Age, marital status, source of income, military/veteran status, political affiliation, student status, domestic violence victim status, genetic information.

### Prohibited Language in Advertising

**NEVER use these in any listing, ad, or marketing material:**

| Category              | Prohibited                                                                                                                     | Why                                 |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------- |
| **Race/Color/Origin** | "Caucasian neighborhood", "diverse area", "ethnic", "integrated", "minority", "oriental", "Hispanic area"                      | Describes demographics              |
| **Religion**          | "Christian community", "near synagogue" (as selling point), "church neighborhood"                                              | Religious preference                |
| **Familial Status**   | "perfect for couples", "no children", "adult community" (unless 55+ exempt), "bachelor pad", "singles only", "family-friendly" | Preference or exclusion of families |
| **Sex/Gender**        | "man cave", "she shed" (debated), "bachelor", "master bedroom" (some MLS systems now use "primary")                            | Gender preference                   |
| **Disability**        | "walking distance" (debated), "perfect for able-bodied", "no wheelchairs", "handicapped" (use "accessible")                    | Disability discrimination           |
| **Steering Language** | "ideal for [any demographic]", "great for [ethnic group]", "perfect for [religion]"                                            | Directs specific groups             |

### Compliant Alternatives

| Instead of                        | Use                                                                                 |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| "Family-friendly neighborhood"    | "Near parks and schools"                                                            |
| "Perfect for young professionals" | "Close to downtown and transit"                                                     |
| "Master bedroom"                  | "Primary bedroom" or "Owner's suite"                                                |
| "Walking distance to..."          | "Close proximity to..." or "[X] miles from..."                                      |
| "Church community"                | "Near community gathering spaces"                                                   |
| "Exclusive neighborhood"          | "Established neighborhood"                                                          |
| "Integrated area"                 | [Don't describe demographics at all]                                                |
| "Safe neighborhood"               | "Well-maintained neighborhood" (but even this is coded — best to describe features) |
| "No children"                     | [Cannot say this unless 55+ community with HUD exemption]                           |
| "Man cave / She shed"             | "Bonus room" or "Workshop" or "Studio"                                              |

### The Bright Line Rule

**Describe the property and its features — NEVER describe the people who live there, should live there, or would be ideal for it.**

✅ "3-bed home near Scottsdale Unified schools with a fenced backyard and community pool"
❌ "Perfect family home in a community of young families near great schools"

Both describe the same property. Only one is compliant.

## Compliance Audit Checklist

When reviewing any marketing material, check:

### Listing Descriptions

- [ ] No references to protected classes
- [ ] No demographic descriptions of neighborhood residents
- [ ] No steering language ("ideal for", "perfect for [group]")
- [ ] No exclusionary language ("no children", "adults only")
- [ ] Accessibility features described neutrally
- [ ] "Primary bedroom" not "master bedroom" (MLS-dependent)
- [ ] Square footage matches MLS / public records
- [ ] Bed/bath count accurate
- [ ] Disclosures included where required by state
- [ ] Broker attribution included (state requirement in many jurisdictions)

### Social Media & Ads

- [ ] Fair Housing logo or statement (required in some jurisdictions)
- [ ] Equal Housing Opportunity phrase or logo
- [ ] No discriminatory targeting (Facebook settled DOJ case on this)
- [ ] No lifestyle imagery that excludes protected classes
- [ ] Agent license number (required in many states)
- [ ] Brokerage name (required in most states)

### Email Marketing

- [ ] CAN-SPAM compliance (unsubscribe link, physical address)
- [ ] No discriminatory language
- [ ] Brokerage identification
- [ ] License number (state-dependent)

### Print Materials

- [ ] Equal Housing Opportunity logo
- [ ] Agent license number
- [ ] Brokerage name and address
- [ ] No discriminatory imagery or language

## State-Specific Requirements

### Common State Requirements (verify current rules)

| Requirement                        | States                       |
| ---------------------------------- | ---------------------------- |
| Agent license # in all advertising | Most states                  |
| Brokerage name in all advertising  | Most states                  |
| Equal Housing logo on print        | Many states                  |
| Seller disclosure form             | Most states (varies by form) |
| Lead paint disclosure (pre-1978)   | Federal — all states         |
| Transfer disclosure statement      | CA, and others               |
| Property condition report          | NY, and others               |

## Review Output Format

```markdown
## Compliance Review: [material type]

### Status: [PASS / ISSUES FOUND / FAIL]

### Issues

| #   | Line/Section    | Issue            | Severity       | Fix                     |
| --- | --------------- | ---------------- | -------------- | ----------------------- |
| 1   | "[quoted text]" | [violation type] | [High/Med/Low] | [suggested replacement] |

### Checklist Results

- [✅/❌] Fair Housing language
- [✅/❌] Protected class references
- [✅/❌] Steering language
- [✅/❌] Accuracy (sqft, beds, baths)
- [✅/❌] Required disclosures
- [✅/❌] Agent/broker identification
- [✅/❌] Equal Housing statement (if required)

### Corrected Version

[Full corrected text, ready to use]
```

## Rules

- When in doubt, flag it. Better to over-flag than to miss a violation.
- Fair Housing violations can result in fines of $16,000+ (first offense) to $100,000+ and license suspension.
- This checker catches common issues but is NOT a substitute for legal review on questionable cases.
- State and local rules vary — always verify against your jurisdiction's specific requirements.
- Proactively check all content generated by other RE skills (re-listings, re-social, re-client).
- HUD testers actively check real estate advertising — compliance isn't optional.
