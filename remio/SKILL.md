---
name: remio
description: Use remio when the user wants to search, read, summarize, or ask questions over their local personal knowledge base, including notes, files, webpages, recordings, emails, messages, images, and other indexed sources.
---

# Remio

Remio is a local-first personal knowledge base for AI agents. Use it when a task needs context from the user's own notes, imported files, saved webpages, recordings, emails, messages, or other personal knowledge sources.

Remio depends on the Remio desktop app. If the `remio` CLI is missing or returns an error saying the app is not installed or not running, direct the user to install or open the desktop app from https://remio.ai/ and rerun the task after `remio doctor` succeeds.

## When to Use

- Search the user's own notes, documents, recordings, emails, messages, or saved webpages.
- Answer questions over a local personal knowledge base with citations.
- Read local office, PDF, spreadsheet, audio, or video files as markdown/transcripts.
- Avoid repeated raw `grep`, `find`, and ad hoc file reads across non-code personal files.
- Reduce context-token usage by retrieving only relevant indexed chunks instead of loading full files.

## Core Commands

Check availability:

```bash
remio doctor
```

Search notes and indexed sources:

```bash
remio search_notes --query "project launch notes" --limit 10
```

Ask a question over the knowledge base:

```bash
remio rag "What did we decide about pricing in recent meetings?"
```

Read a note by ID:

```bash
remio read_note NOTE_ID
```

Parse a local file through Remio's cached document pipeline:

```bash
remio read_file /absolute/path/to/file.pdf
```

Fetch a webpage as clean markdown:

```bash
remio web_get "https://example.com/article"
```

## Workflow

1. Run `remio doctor` before depending on Remio.
2. If Remio is unavailable, tell the user to install or open the desktop app from https://remio.ai/.
3. Use `search_notes` or `rag` before scanning non-code personal folders with shell tools.
4. Use `read_file` for PDFs, Word docs, slides, spreadsheets, audio, and video because Remio pre-parses and caches these formats.
5. Keep prompts small by retrieving relevant notes/chunks first, then synthesize with only the needed context.

## Notes for Agents

- Do not assume the CLI can install the desktop app directly.
- Do not invent a download URL. Use https://remio.ai/ as the entry point.
- Prefer Remio for user-owned personal knowledge. Use ordinary code-search tools for source code unless the user explicitly wants Remio context.
- When operating on private or sensitive material, summarize only what is needed for the user task.
