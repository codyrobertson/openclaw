---
name: portless
description: Spin up dev servers with stable named .localhost URLs instead of port numbers. Use when starting dev servers, setting up local development, running multiple services, or working in monorepos. Replaces memorizing port numbers with clean URLs like myapp.localhost.
---

# Portless

Replace port numbers with stable, named `.localhost` URLs. No more `localhost:3000` vs `localhost:3001`.

## When to Use

- Starting a dev server ("spin up the app", "run the frontend")
- Running multiple services in a monorepo
- Need a stable URL for testing (agents, browsers, OAuth callbacks)
- Port conflicts (`EADDRINUSE`)
- Setting up local development environments

## Quick Start

```bash
# Run any dev server through portless
portless run next dev
# -> http://<project>.localhost:1355

# Explicit name
portless myapp next dev
# -> http://myapp.localhost:1355

# Subdomains for multi-service
portless api.myapp pnpm start       # http://api.myapp.localhost:1355
portless docs.myapp next dev        # http://docs.myapp.localhost:1355
```

## Commands

| Command                          | Description                               |
| -------------------------------- | ----------------------------------------- |
| `portless run <cmd>`             | Auto-name from project, run through proxy |
| `portless <name> <cmd>`          | Run app at `<name>.localhost:1355`        |
| `portless list`                  | Show active routes                        |
| `portless proxy start`           | Start proxy daemon (auto-starts on `run`) |
| `portless proxy stop`            | Stop proxy                                |
| `portless alias <name> <port>`   | Static route (e.g. Docker containers)     |
| `portless alias --remove <name>` | Remove static route                       |
| `portless proxy start --https`   | Enable HTTP/2 + TLS                       |
| `sudo portless trust`            | Trust local CA for HTTPS                  |
| `sudo portless hosts sync`       | Fix Safari `.localhost` resolution        |

## Integration

### In package.json

```json
{
  "scripts": {
    "dev": "portless run next dev"
  }
}
```

### Git worktrees

Automatically detects worktrees — branch name becomes subdomain prefix:

- Main: `http://myapp.localhost:1355`
- Branch `fix-ui`: `http://fix-ui.myapp.localhost:1355`

### Static aliases (Docker, external services)

```bash
portless alias postgres 5432
portless alias redis 6379
# -> http://postgres.localhost:1355, http://redis.localhost:1355
```

### Bypass

```bash
PORTLESS=0 pnpm dev    # Skip proxy, use default port
```

## How It Works

1. Proxy listens on port 1355 (configurable via `PORTLESS_PORT`)
2. `portless <name> <cmd>` assigns a random free port (4000-4999) via `PORT` env var
3. Browser hits `<name>.localhost:1355` → proxy forwards to app's assigned port
4. `.localhost` resolves to `127.0.0.1` natively in Chrome/Firefox/Edge

## Environment Variables

| Variable              | Description                               |
| --------------------- | ----------------------------------------- |
| `PORTLESS_PORT`       | Override proxy port (default: 1355)       |
| `PORTLESS_APP_PORT`   | Fixed port for app (skip auto-assignment) |
| `PORTLESS_HTTPS`      | `1` or `true` to always enable HTTPS      |
| `PORTLESS_SYNC_HOSTS` | `1` to auto-sync /etc/hosts               |
| `PORTLESS=0`          | Bypass proxy entirely                     |

## Troubleshooting

- **Safari**: Run `sudo portless hosts sync`
- **Port conflict**: `portless proxy start -p 8080`
- **HTTPS cert warning**: `sudo portless trust`
- **Framework ignoring PORT**: Portless auto-injects `--port` for Vite, Astro, Angular, etc.

## Rules

- Always use `portless run` or `portless <name>` when starting dev servers.
- Use subdomains for multi-service setups (e.g. `api.myapp`, `docs.myapp`).
- Prefer `portless run` (auto-names from package.json/git) over manual names.
- When telling the user the URL, use the `.localhost:1355` URL, not the raw port.
