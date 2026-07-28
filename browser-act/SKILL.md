---
name: browser-act
description: "Use BrowserAct when an AI agent needs authenticated browser automation, JS-rendered extraction, screenshots, parallel sessions, verification handling, or human handoff."
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "2.0.2"
  install: "uv tool install browser-act-cli --python 3.12"
  homepage: "https://www.browseract.com"
  requires:
    runtime: "Python 3.12+, uv package manager"
  permissions:
    - "Network access for CLI installation and optional verification assistance"
    - "Filesystem access to the BrowserAct CLI data directory for local profiles and session logs"
    - "CDP access to local Chrome only when the user explicitly confirms chrome-direct use"
---

# BrowserAct Browser Automation

Built by [BrowserAct](https://www.browseract.com) - browser automation CLI for AI agents. The canonical Skill is maintained at [browser-act/skills](https://github.com/browser-act/skills/tree/main/browser-act).

## When to Use This Skill

- Use when a task needs a real browser, authenticated state, or JavaScript-rendered content.
- Use for navigation, clicks, form input, screenshots, DOM extraction, or network capture.
- Use when multiple browser sessions or isolated accounts must run in parallel.
- Use when verification or a manual handoff may be required to complete a workflow safely.

## What This Skill Does

1. Loads BrowserAct instructions that match the installed CLI version.
2. Guides agents through browser selection, session ownership, interaction, verification, and cleanup.
3. Applies confirmation gates before browser creation, login, form submission, uploads, and other sensitive operations.
4. Keeps cookies, profiles, page content, and session data local except when the user invokes optional verification assistance.

## How to Use

Install the CLI after the user approves the external package installation:

```bash
uv tool install browser-act-cli --python 3.12
```

After this Skill is invoked, load the complete version-matched operating guide before running any browser command:

```bash
browser-act get-skills core --skill-version 2.0.2
```

Do not truncate that output. It contains the current browser inventory, session rules, safety directives, command reference, and error-handling workflow.

## Example Requests

```text
Open this authenticated dashboard, export the visible table, and verify the row count.
```

```text
Run the same browser workflow across two isolated accounts and return separate results.
```

```text
Inspect this JavaScript-rendered page, capture the relevant network response, and save a screenshot.
```

## Safety and Privacy

- Ask for confirmation before installing the CLI, creating a browser, logging in, submitting a form, or uploading a file.
- Never reuse or close a browser session owned by another conversation.
- Keep credentials, cookies, profiles, and extracted page data local.
- Escalate verification and manual-only steps through the documented human handoff flow.

## Limitations

- The Skill requires Python 3.12+, `uv`, and a compatible BrowserAct CLI installation.
- Site permissions, terms, access controls, and rate limits still apply.
- Login challenges, CAPTCHAs, MFA, and destructive actions can require explicit user participation.
- Command details are intentionally served by the CLI and may differ across installed versions.

## License

MIT License. Copyright (c) 2026 BrowserAct. See `LICENSE.txt`.
