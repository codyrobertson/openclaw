---
name: gwcli-calendar
description: Google Calendar management via gwcli — view upcoming events, search events, create/update/delete events, list calendars. Use when asked about schedule, meetings, upcoming events, or to create/modify calendar events.
---

# Calendar Skill (gwcli)

## When to Use

Any calendar-related request:

- "What's on my calendar today?"
- "Any meetings this week?"
- "Schedule a meeting with [person]"
- "Move my 2pm to 3pm"
- "Cancel the meeting on Friday"
- "When am I free tomorrow?"
- "Create an event for [thing]"

## Tool

Install: `npm install -g google-workspace-cli` (provides `gwcli` command)

Always use `--format json` for parsing output.

## Commands

### List calendars

```bash
gwcli calendar list --format json
```

### View upcoming events

```bash
gwcli calendar events --format json                # Default upcoming
gwcli calendar events --days 7 --format json       # Next 7 days
gwcli calendar events --days 14 --limit 20 --format json
```

### Search events

```bash
gwcli calendar search "meeting" --format json
gwcli calendar search "standup" --format json
```

### Create event

```bash
# With explicit start/end
gwcli calendar create "Team Meeting" \
  --start "2026-03-10 10:00" \
  --end "2026-03-10 11:00"

# Natural time (relative)
gwcli calendar create "Lunch" --start "tomorrow 12:00"

# With location and description
gwcli calendar create "Client Call" \
  --start "2026-03-10 14:00" \
  --end "2026-03-10 15:00" \
  --location "Zoom" \
  --description "Quarterly review"
```

### Update event

```bash
gwcli calendar update <event-id> --title "New Title"
gwcli calendar update <event-id> --start "2026-03-10 14:00"
gwcli calendar update <event-id> --title "Rescheduled" --start "2026-03-11 10:00" --end "2026-03-11 11:00"
```

### Delete event

```bash
gwcli calendar delete <event-id>
```

## Patterns

### Daily briefing

```bash
# Today's events
gwcli calendar events --days 1 --format json

# Parse and present as schedule
```

### Check availability

```bash
# Get events for a date range
gwcli calendar events --days 3 --format json

# Identify gaps between events
```

### Schedule a meeting

```bash
# 1. Check availability
gwcli calendar events --days 7 --format json

# 2. Find open slot
# 3. Create event
gwcli calendar create "Meeting Name" --start "YYYY-MM-DD HH:MM" --end "YYYY-MM-DD HH:MM"
```

## Rules

- Always use `--format json` when parsing output programmatically.
- Confirm event creation details with user before running `gwcli calendar create`.
- Confirm before deleting events.
- When rescheduling, show the old and new times for confirmation.
- Use ISO-style dates: `YYYY-MM-DD HH:MM`
- Profile selection: use `--profile <name>` or set `GWCLI_PROFILE` env var.
