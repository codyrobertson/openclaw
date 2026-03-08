---
name: agent-browser
description: Browse and interact with websites using agent-browser CLI. Use this for web research, form filling, scraping, and any task requiring real browser interaction.
---

# Agent Browser Skill

## Overview

Use `agent-browser` CLI via exec to browse, interact with, and extract data from websites. This is a headless Chromium browser controlled via shell commands.

## Quick Reference

### Navigation

```bash
agent-browser open <url>           # Navigate to URL
agent-browser back                 # Go back
agent-browser forward              # Go forward
agent-browser reload               # Reload page
agent-browser close                # Close current tab
```

### Reading Page Content

```bash
agent-browser snapshot             # Get accessibility tree (best for understanding page structure)
agent-browser text                 # Get all visible text
agent-browser html                 # Get page HTML
agent-browser title                # Get page title
agent-browser url                  # Get current URL
agent-browser screenshot           # Take screenshot (saves to file)
agent-browser pdf                  # Save page as PDF
```

### Interacting with Elements

Use `@ref` references from `snapshot` output (e.g. `@e2`, `@e5`):

```bash
agent-browser click @e2            # Click element by ref
agent-browser fill @e3 "text"      # Fill input field
agent-browser type "text"          # Type text at cursor
agent-browser press Enter          # Press a key
agent-browser hover @e5            # Hover over element
agent-browser select @e4 "option"  # Select dropdown option
```

CSS selectors also work:

```bash
agent-browser click "#submit-btn"
agent-browser fill "input[name=email]" "user@example.com"
```

### Semantic Finding

```bash
agent-browser find role button click --name "Submit"
agent-browser find label "Email" fill "test@test.com"
agent-browser find text "Sign in" click
```

### Tabs

```bash
agent-browser tabs                 # List open tabs
agent-browser tab <id>             # Switch to tab
agent-browser newtab <url>         # Open URL in new tab
```

### JavaScript Execution

```bash
agent-browser eval "document.title"
agent-browser eval "document.querySelectorAll('a').length"
```

### Cookies & Storage

```bash
agent-browser cookies              # List cookies
agent-browser cookie set name=val domain=.example.com
agent-browser storage              # Get localStorage
```

## Workflow Pattern

1. `agent-browser open <url>` - navigate to page
2. `agent-browser snapshot` - read the accessibility tree to understand page layout
3. Use `@ref` IDs from snapshot to interact: `agent-browser click @e5`, `agent-browser fill @e3 "query"`
4. `agent-browser snapshot` again to see updated state
5. `agent-browser text` or `agent-browser eval "..."` to extract specific data

## Tips

- Always run `snapshot` after navigation or interaction to see current page state
- Prefer `@ref` selectors from snapshot over CSS selectors (more reliable)
- Chain commands with `&&` for multi-step operations
- Use `text` for bulk content extraction, `snapshot` for understanding structure
- For login flows: open URL, snapshot, fill credentials, click submit, snapshot to verify
