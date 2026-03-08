---
name: gwcli-gmail
description: Gmail management via gwcli — list, search, read, reply, draft, send, archive, and trash emails. Use when asked to check email, read messages, send emails, reply to threads, or manage inbox.
---

# Gmail Skill (gwcli)

## When to Use

Any email-related request:

- "Check my email"
- "Any unread emails?"
- "Read that email from [person]"
- "Reply to [person]'s email"
- "Send an email to [person] about [topic]"
- "Search emails for [topic]"
- "Archive/trash that email"
- "Draft an email to [person]"

## Tool

Install: `npm install -g google-workspace-cli` (provides `gwcli` command)

Always use `--format json` for parsing output. Use `--profile <name>` if multiple accounts.

## Commands

### List emails

```bash
gwcli gmail list                        # Recent emails (default 10)
gwcli gmail list --unread               # Unread only
gwcli gmail list --limit 20             # More results
gwcli gmail list --format json          # JSON for parsing
```

### Search emails

```bash
gwcli gmail search "from:boss@example.com"
gwcli gmail search "subject:invoice is:unread"
gwcli gmail search "after:2026/03/01 from:client"
gwcli gmail search "has:attachment filename:pdf"
```

Search uses Gmail's native query syntax:

- `from:`, `to:`, `subject:`, `label:`
- `is:unread`, `is:starred`, `is:important`
- `has:attachment`, `filename:`
- `after:YYYY/MM/DD`, `before:YYYY/MM/DD`
- `newer_than:2d`, `older_than:1w`

### Read email

```bash
gwcli gmail read <message-id> --format json
gwcli gmail thread <thread-id> --format json    # Full thread
```

### Send email

```bash
gwcli gmail send --to user@example.com --subject "Subject" --body "Message body"
gwcli gmail send --to user@example.com --cc other@example.com --subject "Subject" --body "Body"
```

### Draft email (compose without sending)

```bash
gwcli gmail draft --to user@example.com --subject "Subject" --body "Draft body"
gwcli gmail send <draft-id>    # Send an existing draft
```

### Reply to email

```bash
gwcli gmail reply <message-id> --body "Thanks for your email"
```

### Archive / Trash

```bash
gwcli gmail archive <message-id>
gwcli gmail trash <message-id>
```

## Patterns

### Check inbox (default flow)

```bash
# 1. Get unread emails
gwcli gmail list --unread --format json

# 2. Read specific email
gwcli gmail read <id> --format json

# 3. Reply if needed
gwcli gmail reply <id> --body "Response here"
```

### Search and summarize

```bash
# Find all emails from someone
gwcli gmail search "from:person@example.com" --format json --limit 20

# Parse JSON, summarize threads
```

## Rules

- Always use `--format json` when parsing output programmatically.
- For sending: confirm recipients and content with the user before `gwcli gmail send`.
- Drafting (`gwcli gmail draft`) is safe — it doesn't send. Use this when unsure.
- Do NOT send emails without explicit user approval.
- Do NOT archive/trash without confirmation unless user says "clean up" or similar.
- Profile selection: use `--profile <name>` or set `GWCLI_PROFILE` env var.
