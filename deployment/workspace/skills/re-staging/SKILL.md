---
name: re-staging
description: Virtual staging and room decoration — AI-powered room visualization, virtual staging descriptions, before/after concepts, furniture layout suggestions, renovation visualization, and design style recommendations. Use when asked to virtually stage a room, suggest decor, visualize renovations, or create room design concepts.
---

# Virtual Staging & Room Decorator Skill

## When to Use

Any staging or room design request:

- "Virtually stage this empty room"
- "What would this room look like with modern furniture?"
- "Stage this listing for photos"
- "Suggest decor for [room]"
- "What design style for this property?"
- "Before/after concept for this kitchen"
- "Renovation visualization for [room]"
- "What paint color for [room]?"

## Staging Approach

### Step 1: Assess the Space

From a photo or description, identify:

- Room type (living room, bedroom, kitchen, dining, office, etc.)
- Room dimensions (estimate from photo or ask)
- Existing features (flooring, windows, fireplace, built-ins)
- Architectural style (modern, traditional, mid-century, craftsman, etc.)
- Natural light direction and quality
- Color of existing finishes (floors, cabinets, counters, trim)
- Target buyer demographic (luxury, first-time, investor, family)

### Step 2: Select Design Style

Match style to property and target buyer:

| Property Type             | Recommended Styles                            |
| ------------------------- | --------------------------------------------- |
| Modern/Contemporary build | Modern minimalist, Scandinavian, Contemporary |
| Mid-century home          | Mid-century modern, Retro modern              |
| Traditional/Colonial      | Transitional, Updated traditional             |
| Craftsman/Bungalow        | Modern craftsman, Warm contemporary           |
| Luxury/High-end           | Luxury contemporary, Curated eclectic         |
| Condo/Urban               | Modern minimalist, Urban contemporary         |
| Farmhouse/Rural           | Modern farmhouse, Rustic contemporary         |
| Fixer/Flip                | Clean contemporary (show potential)           |
| Rental/Investment         | Neutral contemporary (broad appeal)           |

### Step 3: Generate Staging Concept

For each room, specify:

```markdown
### [Room Name] — Staging Concept

**Style:** [design style]
**Color Palette:** [primary], [secondary], [accent]
**Mood:** [warm/cool/bright/cozy/dramatic/airy]

**Furniture:**

- [Main piece] — [material, color, style, approximate size]
- [Secondary piece] — [details]
- [Accent piece] — [details]

**Textiles:**

- [Rug] — [size, material, pattern, color]
- [Curtains/drapes] — [style, color, length]
- [Throw pillows] — [colors, textures, count]
- [Blanket/throw] — [material, color, placement]

**Lighting:**

- [Overhead] — [type, style]
- [Table/floor lamps] — [style, placement]
- [Accent lighting] — [type, placement]

**Decor/Accessories:**

- [Wall art] — [style, size, placement]
- [Plants] — [type, size, placement]
- [Books/objects] — [style, arrangement]
- [Mirrors] — [style, placement]

**Key focal point:** [what draws the eye]
**Photo angle suggestion:** [best angle for listing photos]
```

## AI Image Generation

When the user wants actual visual staging (not just descriptions), use image generation:

### Prompt Engineering for Room Staging

**Structure:**

```
[Interior photo style], [room type] with [furniture description],
[design style] style, [color palette], [lighting description],
[key features], real estate photography, professional staging,
high quality, photorealistic
```

**Examples:**

Empty living room → Staged:

```
Professional real estate photo, spacious living room staged with
a light gray linen sectional sofa, walnut coffee table, cream
shag rug, two navy accent pillows, modern floor lamp, large
abstract art on wall, fiddle leaf fig plant in corner,
contemporary minimalist style, warm natural lighting from
large windows, hardwood floors, clean and inviting,
photorealistic, 4K quality
```

Kitchen renovation visualization:

```
Professional interior photo, modern kitchen renovation with white
shaker cabinets, quartz waterfall island countertop, brushed gold
hardware, subway tile backsplash, stainless steel appliances,
pendant lights over island, light oak hardwood floors, bright and
airy, modern farmhouse style, photorealistic
```

### Room-by-Room Staging Guidelines

**Living Room:**

- Anchor with a sofa (facing toward the room, not wall)
- Coffee table proportional to sofa (⅔ length)
- Area rug large enough for front legs of all seating on it
- Odd number groupings for accessories
- One large art piece > many small ones
- Plants add life (1-3 per room)

**Primary Bedroom:**

- Bed centered on main wall (not under window if possible)
- Matching nightstands with lamps
- Layered bedding (fitted sheet, flat sheet, duvet, throw, pillows)
- Minimal personal items (no family photos for listings)
- Bench or accent chair if space allows
- Soft, neutral palette for broad appeal

**Kitchen:**

- Clear counters (max 3 items visible: knife block, fruit bowl, plant)
- Fresh towels
- Open shelving styled with matching dishes (if applicable)
- Pendant lights on (warm bulbs)
- Fruit bowl, herb plant, or cookbook as accents

**Dining Room:**

- Table set for 4-6 (not fully formal — approachable)
- Simple centerpiece (low, not blocking views across table)
- Chairs pushed in, aligned
- Pendant/chandelier at correct height (30-34" above table)

**Bathroom:**

- White towels, rolled or neatly folded
- Matching soap dispenser and tray
- Small plant (succulents, air plants)
- Candle (unlit, for visual)
- Clear counters otherwise

**Home Office:**

- Clean desk with minimal accessories
- Good task lighting
- Plants
- Bookshelf styled (books + objects, not overstuffed)
- Ergonomic chair (shows functionality)

**Outdoor/Patio:**

- Clean outdoor furniture grouping
- Outdoor rug
- Potted plants
- String lights or lanterns
- Set a table scene (glasses, plates — lifestyle shot)

## Renovation Visualization

For before/after renovation concepts:

```markdown
### Renovation Concept: [Room]

**Current State:** [description of existing condition]

**Proposed Changes:**
| Element | Current | Proposed | Est. Cost |
|---------|---------|----------|-----------|
| Cabinets | [oak/dated/etc] | [white shaker/etc] | $[X]-$[X] |
| Countertops | [laminate/tile] | [quartz/granite] | $[X]-$[X] |
| Backsplash | [none/dated] | [subway tile/etc] | $[X]-$[X] |
| Flooring | [carpet/vinyl] | [LVP/hardwood] | $[X]-$[X] |
| Lighting | [fluorescent/dated] | [recessed/pendant] | $[X]-$[X] |
| Hardware | [brass/dated] | [brushed nickel/gold] | $[X]-$[X] |
| Paint | [beige/dated] | [SW Agreeable Gray/etc] | $[X]-$[X] |
| **Total** | | | **$[X]-$[X]** |

**Expected ROI:** [X]-[X]% of renovation cost recouped at sale
**Target buyer appeal improvement:** [description]
```

### Popular Paint Colors for Staging (2024-2025)

| Color            | Brand/Code | Best For                          |
| ---------------- | ---------- | --------------------------------- |
| Agreeable Gray   | SW 7029    | Whole house, universal appeal     |
| Repose Gray      | SW 7015    | Living, bedroom — slightly cooler |
| Accessible Beige | SW 7036    | Warm interiors, traditional       |
| White Dove       | BM OC-17   | Trim, ceilings, cabinets          |
| Simply White     | BM OC-117  | Clean, modern interiors           |
| Hale Navy        | BM HC-154  | Accent walls, offices, exteriors  |
| Iron Ore         | SW 7069    | Front doors, accent trim          |

## Rules

- Virtual staging should be clearly labeled as "virtually staged" in listings — NAR and most MLS systems require this disclosure.
- Don't virtually remove structural defects (cracks, water damage, mold) — that's misrepresentation.
- Virtual staging should be realistic — don't add windows, remove walls, or change room dimensions.
- Can virtually: add furniture, change wall color, change flooring appearance, add decor, remove personal items, improve lighting.
- Cannot virtually: add rooms, change layout, remove visible damage, add features that don't exist (fireplace, pool).
- Keep staging neutral for listings — bold personal taste reduces buyer pool.
- For renovation visualizations, always note that costs are estimates and vary by market and contractor.
