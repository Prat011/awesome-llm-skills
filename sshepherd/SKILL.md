---
name: sshepherd
description: Operate a real remote server over SSH — health checks, docker/systemd control, log tailing, config edits, read-only Postgres introspection, and declarative deploys — without the agent ever seeing a password, private key, hostname, user, or port.
---

# sshepherd

sshepherd is a compiled Bun/TypeScript CLI for remote server operations over SSH, built so an AI agent can drive a real server without ever seeing a credential. The agent passes only a *name* — an ssh alias, a Postgres target, or a deploy recipe — that resolves to a real host entirely outside the process. OpenSSH does the actual authentication; sshepherd shells out to the system `ssh` binary and returns every response as the same typed JSON envelope, never a raw terminal dump.

## When to Use This Skill

- You want an agent to check on a server's health (disk, memory, CPU, ports, OOM history) or inspect and restart docker/systemd services, but you do not want the host, user, port, or password anywhere in the agent's context.
- You need to tail remote logs, read or write remote config files, or run a declarative, named deploy recipe against a box.
- You want read-only Postgres introspection (tables, activity, slow queries, size) or an SSH/security posture audit on a remote machine, with a hard guarantee that no raw command escape hatch exists.

## What This Skill Does

1. **Zero-knowledge SSH transport**: Every op shells out to the system `ssh` binary through a single execution path, so credential handling stays inside OpenSSH's trusted code path. The agent only ever passes an alias, pg-target, or recipe name — there is no host/user/port/ip field anywhere in the response shape, structurally.
2. **Registry-driven ops across 9 command groups**: `hosts`, `check`, `logs`, `services`, `deploy`, `config`, `db`, `files`, `security` — 52 ops total, each a curated read-only or confirm-gated action. There is no `exec "<any command>"` escape hatch; a raw shell command can only run as an authored step inside a versioned recipe file.
3. **Safe mutations and secret masking**: Every mutating op requires `--yes`, never prompts interactively, and writes an audit line (timestamp, alias, command, arg hash — never raw args). `.env`-shaped files are masked by default; `config put` backs up before overwriting and refuses any path not on an allowlist.

## How to Use

### Basic Usage

```
Check the health of my lms-server box and tell me if it's low on memory or has any OOM history.
```

### Advanced Usage

```
Do a dry-run of the "demo" deploy recipe against my server, and if the plan looks right, run it. Then tail the last 100 lines of the app container's logs to confirm it came up.
```

## Example

**User**: "Is my lms-server running out of disk, and are all its containers healthy?"

**Output**:
```
sshepherd check disk lms-server        -> disk usage per mount, JSON envelope
sshepherd services ps lms-server       -> running containers + status
sshepherd services healthcheck lms-server lms-app  -> per-container health verdict
```
Every response echoes back only the alias `lms-server` — never the real hostname, user, or port — and the agent reports the verdict without any credential ever entering its context.

## Tips

- Call the binary by its absolute path — it is not placed on `PATH`. Use `sshepherd <group> --help` to list a group's actions and flags before invoking.
- Output is JSON to stdout by default; add `--pretty` for a human table/key-value view.
- Every mutating op needs `--yes`; without it the op returns a `CONFIRMATION_REQUIRED` envelope and refuses before touching ssh. Success and failure both get an audit line.
- Use `files download` (two positionals: remote source, local destination) to pull a secrets-bearing file straight to disk — it never returns the bytes in the JSON envelope, unlike `files cat`.
- `db query` takes a single read-only `SELECT`; the real boundary is the read-only DB role on the target, so treat the client-side SELECT check as a UX guardrail, not the security boundary.

## Common Use Cases

- Agent-driven server health triage: disk/memory/CPU/ports/OOM checks and docker/systemd service inspection and restarts, with zero credential exposure.
- Declarative, named deploys with `--dry-run` plan preview, `deploy status`/`logs`, and a `[rollback]` block that `deploy rollback` refuses to run without.
- Read-only Postgres introspection and SSH/security posture audits (`ssh-audit`, `listeners`, `authorized-keys`, `fail2ban`) on remote boxes.

**Credit:** Based on Antheurus's sshepherd CLI (https://github.com/Antheurus/sshepherd), MIT-licensed.
