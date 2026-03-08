---
name: gwcli-drive
description: Google Drive file management via gwcli — list files, search, download, and export Google Docs/Sheets/Slides. Use when asked to find files in Drive, download documents, export spreadsheets, or search for files.
---

# Google Drive Skill (gwcli)

## When to Use

Any Drive-related request:

- "Find that document about [topic]"
- "Download the [filename] from Drive"
- "What files are in my Drive?"
- "Export that Google Sheet as Excel"
- "Search Drive for [keyword]"
- "Get the PDF from [folder]"

## Tool

Install: `npm install -g google-workspace-cli` (provides `gwcli` command)

Always use `--format json` for parsing output.

## Commands

### List files

```bash
gwcli drive list --format json                    # Recent files
gwcli drive list --limit 50 --format json         # More results
gwcli drive list --folder <folder-id> --format json  # Specific folder
```

### Search files

```bash
gwcli drive search "name contains 'report'" --format json
gwcli drive search "mimeType = 'application/pdf'" --format json
gwcli drive search "modifiedTime > '2026-03-01'" --format json
gwcli drive search "name contains 'Q1' and mimeType = 'application/vnd.google-apps.spreadsheet'" --format json
```

Search uses Google Drive query syntax:

- `name contains 'keyword'`
- `fullText contains 'keyword'`
- `mimeType = 'application/pdf'`
- `modifiedTime > 'YYYY-MM-DD'`
- `'<folder-id>' in parents`
- Boolean operators: `and`, `or`, `not`

Common MIME types:

- Google Docs: `application/vnd.google-apps.document`
- Google Sheets: `application/vnd.google-apps.spreadsheet`
- Google Slides: `application/vnd.google-apps.presentation`
- PDF: `application/pdf`

### Download file

```bash
gwcli drive download <file-id>
gwcli drive download <file-id> --output ~/Downloads/report.pdf
```

### Export Google Docs/Sheets/Slides

```bash
# Google Docs
gwcli drive export <doc-id> --format pdf
gwcli drive export <doc-id> --format docx

# Google Sheets
gwcli drive export <sheet-id> --format xlsx
gwcli drive export <sheet-id> --format csv

# Google Slides
gwcli drive export <slide-id> --format pptx
gwcli drive export <slide-id> --format pdf
```

## Patterns

### Find and download a document

```bash
# 1. Search for it
gwcli drive search "name contains 'contract'" --format json

# 2. Download
gwcli drive download <file-id> --output ~/Downloads/contract.pdf
```

### Export spreadsheet data

```bash
# 1. Find the sheet
gwcli drive search "name contains 'budget'" --format json

# 2. Export as CSV for processing
gwcli drive export <sheet-id> --format csv
```

## Rules

- Always use `--format json` when parsing output programmatically.
- Drive access is read-only (list, search, download, export). No upload/delete.
- Save downloaded files to `~/Downloads/` or `~/openclaw/workspace/` unless user specifies.
- Profile selection: use `--profile <name>` or set `GWCLI_PROFILE` env var.
