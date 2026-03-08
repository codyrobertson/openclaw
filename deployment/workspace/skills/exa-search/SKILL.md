---
name: exa-search
description: Perform web searches using Exa's API. Use this skill for live web research when EXA_API_KEY is configured.
---

# Exa Search Skill

## Overview

This skill performs programmatic web search via Exa and prints structured results.

## Prerequisite

Set your Exa API key:

```bash
export EXA_API_KEY="<your_exa_api_key>"
```

Optional:

```bash
export EXA_API_URL="https://api.exa.ai/search"
```

## Usage

```bash
python3 skills/exa-search/scripts/search.py --query "your search query" --count 5
```

## Useful Options

- `--api-key <key>`: override env key for one command
- `--api-url <url>`: override API endpoint
- `--timeout <seconds>`: HTTP timeout (default `20`)
- `--count <n>`: desired result count (clamped to `1..100`)
- `--raw`: print raw JSON response

## Expected Behavior

- Missing key: exits non-zero with clear setup error
- API/network errors: exits non-zero with details
- Success: prints result list (or raw JSON with `--raw`)
