---
name: research
description: Deep research skill. Use when asked to research, investigate, analyze, or deep dive on any topic. Spawns threaded subagents with durable task tracking. Supports multi-phase research with source verification.
---

# Research Skill

## When to Use

Any time the user asks to research, investigate, look into, analyze, or deep dive.

## Protocol

### 1. Clarify Scope (5 seconds max)

Before spawning, determine:

- **What**: exact topic/question
- **Depth**: quick scan (5min) vs deep dive (10min)
- **Output**: list, report, CSV, or comparison
- **Constraints**: geography, date range, industry, etc.

If the request is clear, skip clarification and go.

### 2. Create a Durable Task

```bash
taskman create --name "Research: <topic>" --description "<what to find, output format, constraints>" --priority high
```

Note the task_id from the output.

### 3. Spawn a Research Subagent

The subagent prompt is critical. Structure it with phases:

    sessions_spawn(
      task: "TASK_ID=<id>.

    OBJECTIVE: <one sentence goal>

    RESEARCH PLAN:
    Phase 1 — Discovery: Run 3-5 varied search queries to map the landscape. Use different angles (industry terms, competitor names, technical terms). Save top 20 URLs.
    Phase 2 — Deep Read: Open the top 5-8 most promising URLs. Extract key data points, quotes, numbers. Cross-reference claims across sources.
    Phase 3 — Verify: For any critical claims, find a second source. Flag anything single-sourced.
    Phase 4 — Synthesize: Write structured output with citations. Save to disk.

    CONSTRAINTS: <date range, geography, industry, etc.>
    OUTPUT FORMAT: <csv/json/markdown report>
    SAVE TO: ~/.openclaw/workspace/research_output/<topic>_<date>.<ext>

    TOOLS (priority order):
    1. exa-search: python3 ~/.openclaw/workspace/skills/exa-search/scripts/search.py --query '<query>' --count 10
    2. agent-browser: agent-browser open <url> && agent-browser text
    3. scrapling: CURL_CA_BUNDLE=/etc/ssl/cert.pem ~/code_projects/.venv/bin/python3 -c \"from scrapling import Fetcher; page = Fetcher().get('<url>'); print(page.text[:5000])\"

    PROGRESS TRACKING:
    - taskman update <id> --status running (on start)
    - taskman checkpoint <id> --data '{\"phase\": \"...\", \"sources\": N, \"findings\": N}' (after each phase)
    - taskman append <id> --output 'Phase X complete: ...' (after each phase)
    - taskman complete <id> --result 'path/to/output' (on finish)

    QUALITY RULES:
    - Vary your search queries — don't repeat the same keywords
    - Read actual page content, don't just list URLs
    - Include dates on all data points (information decays)
    - Cite sources with URLs for every claim
    - Flag confidence level: HIGH (multi-source), MEDIUM (single credible source), LOW (unverified)
    - If a source is paywalled or blocked, note it and move on",

      label: "research-<short-topic>",
      mode: "run",
      runTimeoutSeconds: 600
    )

After spawning: post ONE short message summarizing what's being researched. Then STOP.

### 4. Search Query Strategy

Don't just search the topic verbatim. Use multiple angles:

| Query Type    | Example                                        |
| ------------- | ---------------------------------------------- |
| Direct        | "Phoenix real estate market 2025"              |
| Comparison    | "Phoenix vs Scottsdale home prices"            |
| Data-specific | "Maricopa County median home price statistics" |
| Expert/source | "NAR report Arizona housing"                   |
| Negative      | "Phoenix housing market risks downturn"        |
| Recent        | "Arizona real estate news this month"          |

Run 3-5 queries minimum. More angles = better coverage.

### 5. Reading Sources

Don't skim — extract:

- **Numbers**: prices, percentages, counts (with dates)
- **Trends**: up/down/stable, with timeframe
- **Quotes**: from named experts or officials
- **Comparisons**: vs competitors, vs last year, vs national avg
- **Red flags**: contradictions between sources, outdated data

### 6. Checkpoint Pattern

After each phase:

```bash
taskman checkpoint <id> --data '{"phase": "discovery", "queries_run": 5, "sources_found": 18, "top_urls": [...]}'
taskman append <id> --output "Discovery complete: 18 sources from 5 queries, narrowed to 8 for deep read"
```

Save intermediate results to disk after each phase — don't wait until the end.

### 7. Output Formats

**Report (default for open questions):**

```markdown
# Research: <Topic>

Date: YYYY-MM-DD

## Key Findings

1. Finding with [source](url) — confidence: HIGH
2. Finding with [source](url) — confidence: MEDIUM

## Data Points

| Metric | Value | Source | Date |
| ------ | ----- | ------ | ---- |

## Sources

1. [Title](url) — accessed YYYY-MM-DD
```

**CSV (for lists/databases):**
Save to `~/.openclaw/workspace/research_output/<topic>_<date>.csv`

**JSON (for programmatic use):**
Save to `~/.openclaw/workspace/research_output/<topic>_<date>.json`

### 8. Resume Pattern

When a task is stalled/failed:

```bash
taskman resume  # find the task
taskman get <id>  # read checkpoint data
```

Spawn a new subagent with checkpoint context:

    sessions_spawn(
      task: "RESUME TASK_ID=<id>. Previous progress: <checkpoint data>. Skip completed work. Continue from: <last checkpoint>. ...",
      ...
    )

## Rules

- ALWAYS create a taskman entry before spawning.
- ALWAYS checkpoint after each phase.
- ALWAYS save output files to disk.
- ALWAYS cite sources with URLs.
- ALWAYS include dates on data points.
- DO NOT use the built-in web_search tool.
- DO NOT tell the user to configure API keys.
- DO NOT list URLs without reading them first.
- DO NOT present single-source claims as fact without flagging confidence.
