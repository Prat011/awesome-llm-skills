---
name: agenttrace-session-audit
description: Use when you need to inspect AI coding agent session logs with agenttrace for cost, tool failures, latency, anomalies, health, diffs, or CI gate evidence.
---

# Agenttrace Session Audit

Use agenttrace to audit local AI coding agent sessions before reporting status, closing a task, or tightening CI gates. It works best when the user wants evidence from Claude Code, Codex CLI, Gemini CLI, Aider, Cursor exports, OpenCode, or similar JSONL-style logs.

## When to Use This Skill

- The user asks what happened in recent AI coding sessions.
- You need a cost, token, failure, latency, anomaly, or health summary.
- You need a Markdown, JSON, HTML, or text report for a PR, release note, or incident note.
- You need to enforce a lightweight quality gate in CI based on session health.

## What This Skill Does

1. **Find sessions**: Use agenttrace's doctor command to locate supported session directories.
2. **Summarize behavior**: Produce overview, latest-session, waste, and comparison reports.
3. **Create evidence**: Save Markdown, JSON, HTML, or text output for review.
4. **Gate risky runs**: Use health, critical-session, and tool-failure thresholds in CI.

## How to Use

### Basic Usage

```bash
agenttrace --doctor
agenttrace --overview
agenttrace --latest -f markdown -o agenttrace-report.md
```

If the user provides a specific log directory:

```bash
agenttrace -d /path/to/session-logs --overview -f markdown -o agenttrace-report.md
```

### Chinese Output

```bash
agenttrace --overview --lang zh
agenttrace --latest --lang zh -f markdown -o agenttrace-report.zh.md
```

### CI Gate

```bash
agenttrace --overview --fail-under-health 75 --max-tool-fail-rate 20 --fail-on-critical
```

## Example

**User**: "Audit the last Codex and Claude Code runs and tell me if anything looks risky."

**Output**:

```text
Ran agenttrace --doctor to confirm detected session directories, then generated a latest-session Markdown report. The risky areas are repeated tool failures in one session, elevated latency during file reads, and a health score below the CI gate threshold. No destructive actions were taken.
```

## Tips

- Run `agenttrace --version` first when the local installation is unclear.
- Prefer `--doctor` before assuming where logs live.
- Use `-d` when the user provides an export directory.
- Use `-f json` when another tool needs to parse the result.
- Do not delete or rewrite session logs unless the user explicitly asks.

## Common Use Cases

- Summarize AI coding agent cost and token usage after a long task.
- Compare multiple sessions before choosing which implementation path to keep.
- Generate PR evidence showing failures, latency, health, and diffs.
- Add a CI guardrail for critical sessions or low average health.

**Inspired by:** local-first agent observability workflows using [agenttrace](https://github.com/luoyuctl/agenttrace).
