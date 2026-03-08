# TOOLS.md - Local Notes

## CRITICAL: Web Search & Browsing

**DO NOT use or reference the built-in `web_search` tool. It is disabled. DO NOT mention Brave API keys.**

For web search: use the `exa-search` skill via exec:

    python3 ~/.openclaw/workspace/skills/exa-search/scripts/search.py --query "your query" --count 5

EXA_API_KEY is already configured in the environment. Just run the command.

For web browsing: use `agent-browser` via exec:

    agent-browser open https://example.com
    agent-browser snapshot
    agent-browser click @e2
    agent-browser text

**Never tell the user to configure API keys for web search. It already works.**

---

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Mail Tool (Zoho)

Ownership: This mailbox belongs to Claude Mackenzie (AI).
When describing access, say you use Claude Zoho account by default for mail tasks.

Use: `~/.openclaw/workspace/tools/mailtool.py`

Examples:

```bash
# List recent inbox messages
~/.openclaw/workspace/tools/mailtool.py list --limit 20

# Read one message by sequence id
~/.openclaw/workspace/tools/mailtool.py read --id 123

# Search inbox
~/.openclaw/workspace/tools/mailtool.py search --query 'FROM "alerts@example.com"' --limit 10

# Send email
~/.openclaw/workspace/tools/mailtool.py send \
  --to someone@example.com \
  --subject "Test from OpenClaw" \
  --body "Hello from Claude"
```

Environment variables required:

- `ZOHO_EMAIL`
- `ZOHO_PASSWORD`

Optional:

- `ZOHO_IMAP_HOST` (default: `imap.zoho.com`)
- `ZOHO_IMAP_FALLBACK_HOST` (default: `imappro.zoho.com`)
- `ZOHO_SMTP_ENDPOINTS` (CSV `host:port:mode`, default includes `smtp.zoho.com` + fallback `smtppro.zoho.com`)

### mail wrapper

Use short command form:

```bash
mail list --limit 20
mail read --id 123
mail search --query FROM\ "alerts@example.com" --limit 10
mail send --to someone@example.com --subject "Hi" --body "Hello"
```

### Important path note

In agent exec sessions, bare `mail` may resolve to `/usr/bin/mail` (Apple Mail CLI) instead of the Zoho wrapper.
Use absolute path for reliability:

- `/Users/admin/bin/mail ...`

## Google Workspace CLI (gwcli)

Install: `npm install -g google-workspace-cli` (provides `gwcli` command)

Gmail, Calendar, and Drive access via OAuth. Multi-profile support.

```bash
# Gmail
gwcli gmail list --unread --format json
gwcli gmail search "from:person@example.com" --format json
gwcli gmail read <message-id> --format json
gwcli gmail reply <message-id> --body "Response"
gwcli gmail send --to user@example.com --subject "Subject" --body "Body"

# Calendar
gwcli calendar events --days 7 --format json
gwcli calendar create "Meeting" --start "2026-03-10 10:00" --end "2026-03-10 11:00"
gwcli calendar update <event-id> --title "New Title"
gwcli calendar delete <event-id>

# Drive
gwcli drive list --format json
gwcli drive search "name contains 'report'" --format json
gwcli drive download <file-id> --output ~/Downloads/file.pdf
gwcli drive export <doc-id> --format pdf
```

Config: `~/.config/gwcli/` — profiles stored under `profiles/<name>/`.
Always use `--format json` for structured output. Use `--profile <name>` for multi-account.

See skills: `gwcli-gmail`, `gwcli-calendar`, `gwcli-drive` for full command reference.

## OTP Tool (Redis-backed)

Path: `~/.openclaw/workspace/mcp_servers/otp_server.py`

Dependencies:

- `redis` (python package)
- Running Redis server (default `redis://localhost:6379/0`)

Security env:

- `OTP_PEPPER` (set a long random value; do not use default in production)

Examples:

```bash
# Issue OTP
~/.openclaw/workspace/mcp_servers/otp_server.py issue \
  --user cody \
  --purpose login \
  --ttl 300 \
  --max-attempts 5 \
  --cooldown 30 \
  --hourly-limit 10 \
  --pretty

# Verify OTP
~/.openclaw/workspace/mcp_servers/otp_server.py verify \
  --user cody \
  --purpose login \
  --code 123456 \
  --pretty

# Revoke OTP
~/.openclaw/workspace/mcp_servers/otp_server.py revoke \
  --user cody \
  --purpose login \
  --pretty
```

## QR Tool (TOTP / generic QR)

Path: `~/.openclaw/workspace/mcp_servers/qr_server.py`

Dependencies:

- `pyotp`
- `qrcode[pil]`

Examples:

```bash
# Generate otpauth URI + random secret
~/.openclaw/workspace/mcp_servers/qr_server.py totp-uri \
  --account claude-mackenzie@anon.design \
  --issuer OpenClaw \
  --pretty

# Generate TOTP QR PNG
~/.openclaw/workspace/mcp_servers/qr_server.py totp-qr \
  --account claude-mackenzie@anon.design \
  --issuer OpenClaw \
  --out ~/.openclaw/workspace/tmp/totp.png \
  --pretty

# Generate generic text QR PNG
~/.openclaw/workspace/mcp_servers/qr_server.py text-qr \
  --text "hello" \
  --out ~/.openclaw/workspace/tmp/hello.png \
  --pretty
```

### Short wrappers

Use short commands:

```bash
otp issue --user cody --purpose login --pretty
otp verify --user cody --purpose login --code 123456 --pretty
qr totp-uri --account claude-mackenzie@anon.design --issuer OpenClaw --pretty
qr totp-qr --account claude-mackenzie@anon.design --issuer OpenClaw --out ~/.openclaw/workspace/tmp/totp.png --pretty
```

## OTP Approval Bridge

Path: `~/.openclaw/workspace/mcp_servers/otp_gate.py`
Wrapper: `/Users/admin/bin/otp-gate`

Manual tool. Use only when the user explicitly requests OTP-gated approval flow.

Examples:

```bash
# 1) Auto mode
otp-gate run --user cody -- -- echo hello

# 2) Explicit challenge for a command
otp-gate challenge --user cody --purpose approval -- -- launchctl list

# 3) Approve and execute pending command
otp-gate approve --user cody --request-id <REQUEST_ID> --code <OTP>
```

Notes:

- Challenge response includes `request_id` and temporary `otp_code`.
- In production, route `otp_code` to DM/email and do not echo it in chat.
- Pending requests expire with OTP TTL (default 300s).

### Email check (forced direct path)

Command:

```bash
/Users/admin/bin/mail list --limit 5
```

Policy:

- No OTP
- No approval prompt

### Discord Status Channel (required shape)

Use this exact shape for status posts:

```json
{
  "action": "send",
  "channel": "discord",
  "target": "1467276025854431253",
  "message": "status {starting} - <task>"
}
```

And on completion:

```json
{
  "action": "send",
  "channel": "discord",
  "target": "1467276025854431253",
  "message": "status {ending} - <task>"
}
```

Notes:

- `target` must be raw channel ID (or `channel:1467276025854431253`).
- Do not use mention format `<#1467276025854431253>`.
- Do not set `channel` to the numeric channel ID.

## Discord Subagent Threading

**THREADS WORK. YOU MUST USE THEM.**

When spawning subagents from Discord, you MUST include `thread: true` in EVERY `sessions_spawn` call:

    sessions_spawn(task: "...", thread: true, mode: "run")

This is NOT optional. The `thread` parameter MUST be set to `true` for Discord spawns.

**CORRECT** (always do this from Discord):

```json
{ "task": "...", "thread": true, "mode": "run" }
```

**WRONG** (never do this from Discord):

```json
{ "task": "...", "mode": "run" }
```

```json
{ "task": "...", "mode": "session" }
```

Note: `mode: "session"` also requires `thread: true`. If you want a persistent session, use `{"task": "...", "thread": true, "mode": "session"}`.

From Telegram or CLI, omit `thread` entirely (threads are Discord-only).

DO NOT explain threading limitations. DO NOT say threads are disabled. They are enabled and working. Just include `thread: true`.

## Agent Browser (web browsing & interaction)

Use `agent-browser` via exec for browsing websites, filling forms, scraping content, and any web interaction task.

Preferred over the built-in `browser` tool for research and web interaction tasks.

### Quick workflow

```bash
# 1. Open a page
agent-browser open https://example.com

# 2. Read the page structure (accessibility tree with clickable refs)
agent-browser snapshot

# 3. Interact using @ref IDs from snapshot
agent-browser click @e2
agent-browser fill @e3 "search query"
agent-browser press Enter

# 4. Read updated state
agent-browser snapshot
agent-browser text          # bulk text extraction
```

### Key commands

- `open <url>` - navigate
- `snapshot` - accessibility tree with @ref IDs (use this to understand page)
- `text` - get all visible text
- `click @e<N>` - click element
- `fill @e<N> "value"` - fill input
- `press Enter` / `press Tab` - keyboard
- `screenshot` - save screenshot
- `eval "js expression"` - run JavaScript
- `find role button click --name "Submit"` - semantic find
- `tabs` / `newtab <url>` / `close` - tab management

### Tips

- Always `snapshot` after navigating or interacting to see current state
- Use `@ref` selectors from snapshot (e.g. `@e5`) - more reliable than CSS selectors
- For multi-step flows: chain with `&&`
- For login: open, snapshot, fill creds, click submit, snapshot to verify

## X Tool (xurl)

Current local status:

- `xurl` is installed at `/opt/homebrew/bin/xurl`
- `xurl auth apps list` currently reports: `No apps registered`
- `xurl whoami` currently returns `401 Unauthorized`

Operational rule:

- Do not use generic identity language like "AI cannot access X."
- Report concrete local status instead (configured vs not configured), then give exact setup steps.

Setup checklist (when credentials are available):

```bash
# 1) Register app credentials (from your X developer app)
xurl auth apps add my-x-app --client-id <CLIENT_ID> --client-secret <CLIENT_SECRET>

# 2) Set default app
xurl auth default my-x-app

# 3) Complete auth flow (oauth2 or oauth1 as needed)
xurl auth login --app my-x-app

# 4) Verify
xurl whoami
```

## Task Manager (taskman) — Durable Task Persistence

All significant work MUST be tracked as a task. Tasks survive gateway restarts, subagent death, and timeouts.

### Workflow

1. **Before spawning a subagent**, create a task:

```bash
taskman create --name "Research: Shopify leads" --description "Find 100 qualified leads" --priority high
```

2. **Pass the task_id to the subagent** in the task description so it can update progress.

3. **Subagent updates progress** as it works:

```bash
taskman update <id> --status running --progress 25
taskman checkpoint <id> --data '{"batch_a_done": true, "leads_found": 23}'
taskman append <id> --output "Completed Batch A: 23 AZ Shopify stores found"
```

4. **On completion:**

```bash
taskman complete <id> --result "~/openclaw/workspace/research_output/leads.csv"
```

5. **On failure:**

```bash
taskman fail <id> --reason "Exa API rate limited after 50 queries"
```

6. **To resume stalled work:**

```bash
taskman resume          # shows all resumable tasks with checkpoints
taskman get <id>        # see full checkpoint data
```

Then spawn a new subagent with the checkpoint data in its task description.

### Commands

```
taskman create   --name "..." --description "..." [--priority high]
taskman list     [--status pending|running|done|failed|stalled]
taskman get      <id>
taskman update   <id> --status running [--progress 45] [--checkpoint '{}']
taskman checkpoint <id> --data '{}'
taskman append   <id> --output "progress note"
taskman complete <id> [--result "path or summary"]
taskman fail     <id> --reason "why"
taskman resume   # list resumable tasks
taskman stale    # mark tasks with no update in 10min as stalled
```

### Rules

- EVERY subagent task gets a taskman entry. No exceptions.
- Checkpoint after each batch/phase of work.
- Save all output files to `~/openclaw/workspace/research_output/`.
- When resuming: read the checkpoint, skip completed work, continue from where it stopped.
