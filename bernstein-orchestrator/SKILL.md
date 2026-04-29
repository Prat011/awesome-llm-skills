---
name: bernstein-orchestrator
description: Use Bernstein to orchestrate parallel CLI coding agents (Claude Code, Codex CLI, Gemini CLI, OpenHands, Cursor, Aider, and more) on a single repository. Use when a coding task is large enough to decompose across roles (backend, frontend, qa, security, docs) and you want each role to run in an isolated git worktree under a deterministic scheduler.
---

# Bernstein Orchestrator

Bernstein is an open-source multi-agent orchestrator for CLI coding agents. Instead of asking one agent to do everything, you describe the work as a YAML plan with stages and steps; Bernstein spawns short-lived role-scoped agents (manager, backend, frontend, qa, security, devops, architect, docs, reviewer) in parallel git worktrees and reconciles their work through a deterministic Python scheduler. There are no LLM tokens spent on coordination — only on the actual coding tasks.

## When to Use This Skill

- You have a multi-step project that benefits from parallel execution (e.g. backend + frontend + tests + docs).
- You want to compare or combine output from multiple CLI coding agents (Claude Code, Codex CLI, Gemini CLI, Aider, OpenHands, Cursor, Goose, Qwen, Ollama, and 28 more) on the same codebase.
- You need quality gates, cost tracking with budgets, or HMAC-signed audit logs around an autonomous coding run.
- You want to expose orchestration to another LLM via MCP — Bernstein ships a first-class MCP server (`bernstein_run`, `bernstein_status`, `bernstein_tasks`, `bernstein_approve`, `bernstein_cost`, `load_skill`, etc.).

## What This Skill Does

1. **Plan loading**: Reads a `plan.yaml` describing stages, steps, roles, dependencies, and complexity hints. Skips LLM-based planning when a plan is provided.
2. **Role-scoped spawning**: Spawns short-lived agents (1-3 tasks each, then exit) in isolated git worktrees so they cannot stomp each other's edits.
3. **Quality gates**: Runs configurable lint/test/coverage/security gates; failed gates open retry tasks.
4. **Cost tracking**: Aggregates per-agent token spend and enforces per-run budgets; halts the run if a budget is breached.
5. **MCP server**: Exposes orchestration tools to outer LLMs so a parent agent can drive an entire Bernstein run with a few tool calls.

## How to Use

### Basic Usage

Install once:

```
pipx install bernstein
```

Then point Bernstein at the repository you want it to work on:

```
cd /path/to/repo
bernstein run plans/my-feature.yaml
```

A minimal `plans/my-feature.yaml`:

```yaml
project: my-feature
stages:
  - name: backend
    steps:
      - goal: "Add /users/{id}/avatar endpoint"
        role: backend
        complexity: medium
  - name: frontend
    depends_on: [backend]
    steps:
      - goal: "Wire avatar upload to new endpoint"
        role: frontend
  - name: qa
    depends_on: [frontend]
    steps:
      - goal: "Add e2e test for avatar upload"
        role: qa
```

### Advanced Usage

Drive Bernstein from another LLM via MCP. Once `bernstein mcp` is registered as an MCP server in your client, the outer agent can call:

```
bernstein_run(plan="plans/my-feature.yaml", budget_usd=5)
bernstein_status()
bernstein_tasks(status="open")
bernstein_approve(task_id="t-42")
```

To restrict which CLI agents are spawned, set `BERNSTEIN_ADAPTERS=claude,codex,aider` (any subset of the 37 adapters) before `bernstein run`.

## Example

**User**: "Use the Bernstein Orchestrator skill to add a /users/{id}/avatar endpoint and matching frontend, with tests, on the current repo."

**Output**:

```
$ bernstein run plans/avatar.yaml
[plan] loaded 3 stages, 3 steps
[spawn] backend: claude-code (task t-1)
[spawn] frontend: codex (task t-2, depends_on=t-1)
[spawn] qa: aider (task t-3, depends_on=t-2)
[gate] backend tests: PASS
[gate] frontend lint: PASS
[gate] qa e2e: PASS
[cost] $0.84 / $5.00 budget
[done] 3 tasks completed in 7m41s
```

**Inspired by:** real multi-agent coding workflows where a single CLI agent runs out of context before the work is done; Bernstein keeps each agent short-lived and stateless, with all state living in `.sdd/` files.

## Tips

- Start with `bernstein run --dry-run plans/foo.yaml` to see the task graph before spawning agents.
- Set per-stage budgets in the plan (`budget_usd: 1.0`) when you do not trust a particular role yet.
- The `mcp__bernstein__load_skill` tool exposes role-scoped progressive skill packs so spawned agents only load the docs they need.
- Pair with `using-git-worktrees` from this list — Bernstein already creates one worktree per agent, so do not pre-create them by hand.

## Common Use Cases

- Shipping a feature that touches backend, frontend, tests, and docs in one run.
- Comparing Claude Code vs. Codex vs. Aider on the same task and keeping the best diff.
- Running an overnight self-evolving improvement pass on your own repo (Bernstein develops itself this way).
