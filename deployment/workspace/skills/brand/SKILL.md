---
name: brand
description: Brand strategist and content creator. Use when asked to create social posts, marketing copy, brand strategy, update brand info, or when discussing projects that have a brand profile. Trigger on "tweet", "post", "brand", "marketing", "content", "messaging", "copy", or project discussions about Persona LM or Evante.
---

# Brand Skill

## Brand Profiles

Brand profiles live in `~/.openclaw/workspace/brands/`. Always read the relevant brand file before generating content.

Available brands:

- `persona-lm.md` — AI buyer intelligence for ecommerce (Cody's company)
- `evante.md` — Invite-only membership community for high achievers

## Auto-Update Rule (CRITICAL)

When Cody discusses a project that has a brand profile, and the conversation reveals NEW information about the project (new features, positioning changes, new stats, pivot, new audience insight, pricing change), you MUST:

1. Note what changed
2. Update the brand .md file with the new information
3. Briefly confirm: "Updated persona-lm.md: added X"

Do NOT ask permission. Just update. Cody expects the brand file to stay current as a living document.

## Mode Detection

| Request                                          | Action                                              |
| ------------------------------------------------ | --------------------------------------------------- |
| "tweet about X", "LinkedIn post", "write copy"   | Read brand file -> generate ready-to-use content    |
| "batch", "content calendar", "week of posts"     | Read brand file -> generate coordinated batch       |
| "new brand", "onboard brand"                     | Run discovery interview -> create new brand profile |
| "update brand", project discussion with new info | Update the brand .md file                           |

## Content Generation

1. **Read the brand file first** — match voice, tone, do's/don'ts exactly
2. **Platform conventions:**
   - Twitter/X: punchy, stat-led, hooks first, thread potential
   - LinkedIn: professional but human, value-driven, evidence-based
   - Email: direct subject line, short paragraphs, one CTA
   - Website: conversion-focused, scannable, benefit-driven
3. **Output format:**

```
[Ready-to-use content — no placeholders]

---
Format: [platform] | Voice: [alignment note]
```

## Voice Rules

- Embody the brand voice — don't just reference it
- Check the Do's and Don'ts list literally
- Same personality across platforms, different volume
- When uncertain, slightly conservative > off-brand

## Creating New Brands

Interview flow (use exec to save results):

1. Name, what it does, audience, competitors
2. Voice: how would the brand speak? 3 personality adjectives. What should it NEVER sound like?
3. Core message, proof points, objections
4. Priority platforms, topics to own, topics to avoid

Save to `~/.openclaw/workspace/brands/[name].md`
