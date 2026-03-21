---
name: skillfold-cli
description: Use the skillfold compiler to manage multi-agent pipeline configs
version: 1.19.0
---

# Skillfold CLI

Use the skillfold compiler to manage multi-agent pipeline configs. Compile, validate, inspect, and visualize pipelines defined in skillfold.yaml.

## Commands

- `npx skillfold` - Compile the pipeline config
- `npx skillfold init [dir]` - Scaffold a new pipeline project
- `npx skillfold validate` - Validate config without compiling
- `npx skillfold list` - Display pipeline summary
- `npx skillfold graph --html` - Interactive pipeline visualization
- `npx skillfold run --target claude-code` - Execute the pipeline
- `npx skillfold search [query]` - Find skills on npm

## Targets

Compile to any platform:

- `--target claude-code` - .claude/agents/*.md
- `--target cursor` - .cursor/rules/*.mdc
- `--target codex` - AGENTS.md
- `--target copilot` - .github/instructions/*.md
- `--target gemini` - .gemini/agents/*.md
- `--target windsurf` - .windsurf/rules/*.md

## Install

```bash
npm install -g skillfold
```

Source: https://github.com/byronxlg/skillfold
