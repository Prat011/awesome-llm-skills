# Schema-Guided Reasoning for Pydantic

An LLM skill for building strict Pydantic schemas for structured output using **Schema-Guided Reasoning (SGR)**.

## Installation

### Claude Code (global — all projects)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/feodal01/schema-guided-reasoning-pydantic \
  ~/.claude/skills/schema-guided-reasoning-pydantic
```

### Codex CLI (global — all projects)

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/feodal01/schema-guided-reasoning-pydantic \
  ~/.agents/skills/schema-guided-reasoning-pydantic
```

### Project-local (checked into repo, shared with team)

```bash
# Claude Code
mkdir -p .claude/skills
git clone https://github.com/feodal01/schema-guided-reasoning-pydantic \
  .claude/skills/schema-guided-reasoning-pydantic

# Codex CLI
mkdir -p .agents/skills
git clone https://github.com/feodal01/schema-guided-reasoning-pydantic \
  .agents/skills/schema-guided-reasoning-pydantic
```

After installing, Claude Code picks up the skill automatically (no restart needed for existing sessions if the directory already existed; restart once if it's a new directory). Codex detects skill changes automatically.

### Invoke

```
# Explicit
/schema-guided-reasoning-pydantic

# Or just describe what you need — the skill triggers automatically:
Design a strict Pydantic schema for a judge that evaluates answer faithfulness.
```

---

## What problem it solves

LLM APIs without a JSON Schema on the structured-output endpoint don't guarantee valid JSON on every call—agents silently fail when parsing breaks. This skill covers two things:

1. How to build a correct Pydantic-derived JSON Schema for **constrained decoding** so the model server enforces the shape.
2. How to use **Schema-Guided Reasoning (SGR)** to go further—encoding the reasoning *path* (ordered checkpoints, branch locks, bounded lists) into the schema itself so the model thinks in the structure you need, not around it.

## Who uses this

Engineers building LLM-as-judge pipelines, evaluators, classifiers, extraction workflows, and agent handoff schemas where downstream code depends on which reasoning branch ran—not just whether the JSON parsed.

## How to use

```
Use the Schema-Guided Reasoning for Pydantic skill to design a strict schema
for an LLM judge that evaluates whether a generated answer is faithful
to source evidence.
```

The skill walks through:

- Building a **route matrix** (branch × codes × required fields × decision impact)
- Mapping branches to SGR patterns: **Cascade**, **Routing**, **Cycle**
- Encoding branch locks with `Literal[...]` fields
- Checking the exported JSON Schema against provider constraints
- Ready-to-copy API call examples for **OpenAI** (`chat.completions.parse`) and **Gemini** (`google-genai` + `model_json_schema()`)
- Provider transport profiles for **OpenAI**, **Gemini**, **Anthropic**, and **xAI**

## Contents

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill instructions |
| `references/patterns.md` | SGR pattern playbook |
| `references/templates.md` | Copy-paste Pydantic templates |
| `references/cross-cutting-caveats.md` | Caveats that apply to all providers |
| `references/api-call-examples.md` | OpenAI and Gemini API call examples |
| `references/providers/openai-structured-outputs.md` | OpenAI Structured Outputs rules and limits |
| `references/providers/gemini.md` | Gemini native vs OpenAI-compatible quirks |
| `references/providers/anthropic.md` | Anthropic `output_config.format` and strict tool use caveats |
| `references/providers/xai.md` | xAI / Grok Structured Outputs behavior |

## Attribution

Based on Schema-Guided Reasoning patterns by Rinat Abdullin:
- Overview: https://abdullin.com/schema-guided-reasoning/
- Patterns: https://abdullin.com/schema-guided-reasoning/patterns
- Structured output caveats: https://abdullin.com/structured-output/
