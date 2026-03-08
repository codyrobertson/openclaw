---
name: scrapling
description: Scrape and crawl websites using Scrapling framework. Use for web scraping, data extraction, bypassing anti-bot protections, and crawling. Handles Cloudflare, TLS fingerprinting, and dynamic JS-rendered pages.
---

# Scrapling Skill

## Overview

Scrapling is an adaptive web scraping framework installed at `~/code_projects/.venv`. It handles anti-bot bypass, adaptive element tracking, and concurrent crawling.

## Usage

Always use the venv Python with CURL_CA_BUNDLE set:

    CURL_CA_BUNDLE=/etc/ssl/cert.pem ~/code_projects/.venv/bin/python3 -c "
    from scrapling import Fetcher
    page = Fetcher().get('https://example.com')
    print(page.find('h1').text)
    "

## Fetcher Types

- **Fetcher** — fast HTTP with browser impersonation (default, use for most scraping)
- **StealthyFetcher** — advanced stealth with TLS fingerprint spoofing (anti-bot sites)
- **DynamicFetcher** — full Playwright browser for JS-heavy pages (requires playwright install)

## Common Patterns

### Basic scrape

    CURL_CA_BUNDLE=/etc/ssl/cert.pem ~/code_projects/.venv/bin/python3 << PYEOF
    from scrapling import Fetcher
    page = Fetcher().get("https://example.com")
    for link in page.find_all("a"):
        print(link.get("href"), link.text)
    PYEOF

### CSS selectors

    page.find(".article-title").text
    page.find_all("div.item", limit=10)
    page.find("a[href*=product]").get("href")

### Stealth mode (Cloudflare bypass)

    from scrapling import StealthyFetcher
    page = StealthyFetcher().get("https://protected-site.com")

### Extract structured data

    from scrapling import Fetcher
    page = Fetcher().get(url)
    items = []
    for card in page.find_all(".product-card"):
        items.append({
            "title": card.find(".title").text,
            "price": card.find(".price").text,
            "url": card.find("a").get("href"),
        })

## Environment

- Python: ~/code_projects/.venv/bin/python3 (3.12)
- CURL_CA_BUNDLE=/etc/ssl/cert.pem (required, already in ~/.openclaw/.env)
- Installed extras: all (curl_cffi, playwright, browserforge, beautifulsoup4)

## Tips

- Always set CURL_CA_BUNDLE=/etc/ssl/cert.pem before running
- Use Fetcher for speed, StealthyFetcher only when blocked
- page.find() returns first match, page.find_all() returns list
- Scrapling auto-retries on failure (3 attempts by default)
