---
name: anywrite
description: Create, update, search, and organize notes, tasks, and PKM objects in a local Anytype space — covers all 52 endpoints of the Anytype local API (spaces, objects, properties, tags, types, templates, lists, chat, files, members, search, auth) through one compiled CLI binary.
---

# anywrite

anywrite is a compiled Bun/TypeScript CLI that talks to the [Anytype](https://anytype.io) desktop app's local HTTP API. It covers all 52 endpoints of the Anytype local API — spaces, objects, properties, tags, types, templates, lists (sets + collections), chat, files, members, search, and auth — as a single binary with zero runtime dependencies. Anytype's official MCP server exposes 52 always-loaded tools to every session whether they're used or not; anywrite is the alternative that costs zero context until it's actually invoked, and works just as well from a plain terminal or any agent/script.

## When to Use This Skill

- You want to create, update, search, or organize notes, tasks, or knowledge-base objects in a local Anytype space, driven by natural language.
- You need to manage the structure of a space — properties, tags, types, templates, and lists (sets and collections) — or upload and attach files.
- You want to run structured search across a space, read or post chat messages inside a space, or verify that a batch of mutations actually landed.

## What This Skill Does

1. **Full local-API coverage in one binary**: Every one of the 52 Anytype local API endpoints is a data-driven entry in an endpoint registry (method, path, params, quirks). Spaces, objects, properties, tags, types, templates, lists, chat, files, members, search, and auth are all reachable — no MCP server, no per-tool context tax.
2. **Name-or-id resolution and format-aware writes**: `space`/`type`/`property` positionals accept a plain name or an id, and the CLI resolves names to ids automatically. `--property key=value` is format-aware — select/multi_select resolve tag names, checkbox takes true/false, multi-value formats take comma-separated lists.
3. **Agent-first, verifiable output**: JSON by default, a `--pretty` table view, a `--json` escape hatch for structured filter bodies, and a verbatim error envelope on any 4xx/5xx. A composite `verify` command re-fetches objects and checks specific property values so a caller can confirm a batch write landed instead of eyeballing raw JSON.

## How to Use

### Basic Usage

```
Create a task in my Anytype space called "Buy milk" with a body note, then confirm it was created.
```

### Advanced Usage

```
In my Anytype space, set up a "Stage" select property with a Backlog tag, a Ticket type, create a ticket named "Wire auth" in Backlog, then search for all Backlog tickets and mark the first one Shipped.
```

## Example

**User**: "Add a task 'Buy milk' to my space and verify it landed."

**Output**:
```
anywrite objects create <space> --type task --name "Buy milk" --body "notes here"
anywrite verify <space> <object_id> --pretty
```
The create returns the new object's id as JSON; `verify` re-fetches it, reports `found: true`, and exits 0 — a script/CI-friendly confirmation that the mutation actually took effect.

## Tips

- Anytype desktop must be running locally (default `http://localhost:31009`). Authenticate once with `anywrite auth` — a 4-digit code appears in the desktop app; the resulting key is stored locally and never printed by any command.
- The object body field is named differently per action: `--body` on create, `--markdown` on update; it comes back under `markdown` on get. Using the wrong flag is silently ignored.
- Icons: omit the flag entirely rather than passing an empty string — `--icon ""` returns a 400.
- Structured search filters go in the `--json '{"filters": ...}'` body (select conditions need the tag *id*, looked up via `tags list`); `--filter` is a separate URL query passthrough, not the filter body.
- `lists add`/`lists remove` only work on collections, not sets — sets are query-driven, read-only views. Delete is a soft archive everywhere and is idempotent.

## Common Use Cases

- Building structured content in Anytype from scratch: property → tags → type → objects → verify, all non-interactively.
- Find-and-update by property across a space: resolve a tag id, run a filtered search, update matched objects, and verify the change.
- Bulk import, file attach, and space chat — plus a scriptable `verify` step so an agent knows every write actually landed.

**Credit:** Based on Antheurus's anywrite CLI (https://github.com/Antheurus/anywrite), MIT-licensed. Anytype API design credit goes to the Anytype team.
