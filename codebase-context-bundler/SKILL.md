---
name: codebase-context-bundler
description: Automatically inspects, sanitizes, and bundles multi-file codebases or git diffs into token-counted, secret-safe prompts for Claude Code, Codex, and Gemini CLI. Prevents credential leaks and optimizes context window consumption.
---

# Codebase Context Bundler

This skill helps AI coding agents and developers safely bundle multi-file repositories or recent git diffs into clean, token-optimized context prompts while automatically shielding sensitive credentials.

## When to Use This Skill

- Providing full repository context to Claude Code, Codex, or Gemini CLI for architectural refactoring
- Generating pull request code review prompts from uncommitted or staged changes
- Auditing codebase token consumption before making expensive API calls
- Packaging subfolders into Anthropic XML `<documents>` format
- Preventing accidental prompt leakage of `.env`, `.pem`, private keys, and certificates

## What This Skill Does

1. **Intelligent Traversal**: Traverses project directories while strictly honoring `.gitignore` rules and skipping binary/build artifacts.
2. **Secret Shielding**: Automatically detects and excludes sensitive files (`.env`, `.pem`, `.key`, keystores, and credentials).
3. **Token Budgeting**: Computes accurate BPE token approximations for Claude and GPT models to prevent context overflows.
4. **Git Diff Mode**: Isolates only changed or staged files to keep prompts concise for PR reviews.
5. **Multi-Format Export**: Generates Claude XML tags (`<documents><document>`), Markdown code blocks, or JSON structures.

## How to Use

### Basic Context Generation

```
Bundle the current repository into Claude XML context
```

### Git Diff & PR Review Mode

```
Bundle only my uncommitted git changes with token estimates for a code review prompt
```

### Command-line Quick Execution

Using the zero-dependency [`ctxpack`](https://github.com/abzurdd/ctxpack) CLI:

```bash
# Preview token estimates without printing files
npx @abzurdd/ctxpack . --stats

# Bundle uncommitted git changes and copy to clipboard
npx @abzurdd/ctxpack . --diff --xml --copy
```

## Example

**User**: "Bundle this repo for Claude with secret protection"

**Output**:
```markdown
# Codebase Context: my-app

## Summary
- **Files Included**: 14
- **Total Lines**: 1,240
- **Estimated Tokens (Claude)**: ~12,450
- **Safety**: 2 sensitive files automatically shielded (.env.local, cert.pem)

## Directory Structure
my-app/
├── src/
│   ├── index.ts
│   └── utils.ts
└── package.json

## File Contents
...
```

**Inspired by:** Abhishek Chattopadhyay's [`ctxpack`](https://github.com/abzurdd/ctxpack) prompt engineering toolkit.

## Tips

- Use `--diff` when asking for code reviews to drastically reduce token usage and cost.
- Always check `.env.example` is present while keeping `.env` excluded.
- Works natively with Claude Code, Codex CLI, and Gemini CLI.

## Related Use Cases

- Codebase onboarding for new AI assistants
- PR and pre-commit security audits
- Token-efficient context management for agent subtasks
