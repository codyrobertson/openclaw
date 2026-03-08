---
name: research
description: Deep research skill. Use when asked to research, investigate, analyze, or deep dive on any topic. Spawns threaded subagents with durable task tracking.
---

# Research Skill

## When to Use

Any time the user asks to research, investigate, look into, analyze, or deep dive.

## Protocol

### 1. Create a Durable Task

Before doing anything, create a task:

```bash
taskman create --name "Research: <topic>" --description "<what to find>" --priority high
```

Note the task_id from the output.

### 2. Spawn a Subagent

Include the task_id in the subagent's instructions so it can checkpoint progress.

**From Discord:**

    sessions_spawn(
      task: "TASK_ID=<id>. Research: <detailed description>. \n\nIMPORTANT: Use taskman to track progress:\n- Run: taskman update <id> --status running\n- After each batch: taskman checkpoint <id> --data '{...}' and taskman append <id> --output '...'\n- On completion: taskman complete <id> --result 'path/to/output'\n- Save all files to ~/openclaw/workspace/research_output/\n\nTools: exa-search for web search, agent-browser for browsing, scrapling for scraping.",
      label: "research-<short-topic>",
      mode: "run",
      runTimeoutSeconds: 600
    )

**From Telegram/CLI:** Same but threads are created automatically on Discord.

After spawning: post ONE short message. Then STOP.

### 3. Research Tools (priority order)

**a) Exa Search:**

```bash
python3 ~/.openclaw/workspace/skills/exa-search/scripts/search.py --query "<query>" --count 10
```

**b) Agent Browser:**

```bash
agent-browser open <url>
agent-browser snapshot
agent-browser text
```

**c) Scrapling:**

```bash
CURL_CA_BUNDLE=/etc/ssl/cert.pem ~/code_projects/.venv/bin/python3 -c "
from scrapling import Fetcher
page = Fetcher().get('<url>')
print(page.text[:5000])
"
```

### 4. Checkpoint Pattern (subagent must follow)

After each phase/batch of work:

```bash
# Save progress
taskman checkpoint <id> --data '{"phase": "batch_a", "items_found": 15, "last_query": "..."}'
taskman append <id> --output "Batch A complete: 15 AZ Shopify stores qualified"

# Save intermediate results to file
python3 -c "
import csv
with open('/Users/admin/.openclaw/workspace/research_output/<topic>_partial.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=[...])
    writer.writeheader()
    writer.writerows(data)
"
```

### 5. Resume Pattern

When a task is stalled/failed and needs resuming:

```bash
taskman resume  # find the task
taskman get <id>  # read checkpoint
```

Then spawn a new subagent with checkpoint context:

    sessions_spawn(
      task: "RESUME TASK_ID=<id>. Previous progress: <checkpoint data>. Skip completed work. Continue from: <last checkpoint>. ...",
      ...
    )

### 6. Output Format

Save final results to `~/openclaw/workspace/research_output/<topic>_<date>.csv` (or .json/.md).

## Rules

- ALWAYS create a taskman entry before spawning research.
- ALWAYS checkpoint after each phase.
- ALWAYS save output files to disk.
- DO NOT use the built-in web_search tool.
- DO NOT tell the user to configure API keys.
