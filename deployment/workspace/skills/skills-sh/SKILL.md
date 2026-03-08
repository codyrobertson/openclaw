---
name: skills-sh
description: Install community skills from skills.sh — the open skill directory for AI agents. Use when asked to find skills, install a skill, search for agent capabilities, or enhance the agent with new skills.
---

# Skills.sh — Agent Skills Directory

Open ecosystem of reusable skills for AI agents. Install community-contributed skills with a single command.

## When to Use

- "Find a skill for [topic]"
- "Install the [name] skill"
- "What skills are available for [domain]?"
- "Add [capability] to the agent"
- Looking for best practices or patterns for a specific technology

## Install a Skill

```bash
npx skillsadd <owner/repo>
```

This downloads the skill from the GitHub repo and installs it into the current project's skills directory.

### Examples

```bash
# Install Vercel React best practices
npx skillsadd vercel/react-best-practices

# Install a web design guidelines skill
npx skillsadd <owner>/web-design-guidelines

# Install any skill from the directory
npx skillsadd <github-owner>/<repo-name>
```

## Finding Skills

### Browse the directory

Visit https://skills.sh/ to search and browse the leaderboard of popular skills.

### Top skills (by installs)

- `find-skills` — Meta-skill for discovering other skills
- `vercel-react-best-practices` — React patterns and conventions
- `web-design-guidelines` — Frontend design principles
- Various domain-specific skills (Azure, marketing, testing, etc.)

## Skill Structure

Skills from skills.sh follow the standard SKILL.md format:

```
skills/<skill-name>/
  SKILL.md          # Skill definition with frontmatter
  scripts/          # Optional helper scripts
  references/       # Optional reference docs
```

## Integration with OpenClaw

Skills installed via `npx skillsadd` land in the project's skills directory. For the OpenClaw deployment workspace, install into:

```bash
cd ~/openclaw/workspace
npx skillsadd <owner/repo>
```

Or manually copy the SKILL.md into `deployment/workspace/skills/<name>/SKILL.md`.

## Rules

- Search skills.sh before building a skill from scratch — someone may have already built it.
- Vet skills before installing — read the SKILL.md content on GitHub first.
- Skills are just markdown files with frontmatter — safe to review, modify, or extend.
- When installing for the deployed agent, put skills in `deployment/workspace/skills/`.
