---
name: bandaid
description: Forces root-cause fixes instead of symptom patches. Use when debugging a bug, a failing or flaky test, a CI run that went red, or any "just make it pass" request.
---

# bandaid

Stop patching symptoms. A fix that hides the error is not a fix; it is the bug wearing a costume. `bandaid` forces a reproduction before any edit, isolates the real cause, and gates the agent's own diff so swallowed errors, removed guards, disabled tests, and silenced checkers cannot land.

Install the full skill (SKILL.md + scanner script) with:

```bash
npx skills add F0Rextasy/bandaid
```

Source: [F0Rextasy/bandaid](https://github.com/F0Rextasy/bandaid)

## When to Use This Skill

- Debugging a bug, a failing or flaky test, or a CI run that went red
- A "just make the test pass" or "make the error go away" request
- Reviewing an AI-generated fix that might only hide the failure
- Before reporting any bugfix as complete

## What This Skill Does

1. **Reproduce first**: no code edits until the failing path runs and the exact error is captured
2. **Isolate the cause**: follow the traceback to the one `file:line` where correct data becomes incorrect data
3. **Fix at the cause**: rejects symptom patches — `except: pass`, guards downgraded to `return None`, skipped tests, `eslint-disable`, `continue-on-error`
4. **Gate the diff**: runs the bundled scanner over the agent's own diff; exit 1 means bandaids found, so success cannot be reported

## How to Use

### Basic Usage

```
Use the bandaid skill to fix this failing test.
```

### Advanced Usage

```
Use the bandaid skill, then gate the whole branch:
python scripts/bandaid.py --base main --strict
```

## Example

**User**: "The checkout test went red, make it pass."

**Output**:
```
Reproduction: pytest tests/test_checkout.py::test_total → ValueError: total must be positive
Cause: src/checkout.py:6 — discount loop returns None on an empty cart
Fix: clamp applied at the cause; guard kept
Gate: python scripts/bandaid.py → clean (exit 0)
```

## Tips

- An intentional shortcut must carry a reason on the line itself: `# bandaid: allow -- <reason>` — stripped before matching, always counted
- Suspect-level findings pass by default; add `--strict` in CI to fail them too
- `--format json` gives machine output for hooks and CI annotations

## Common Use Cases

- CI went red and someone (or an agent) proposes deleting or skipping the test
- A `try/except` or `catch {}` added around the failing call with no handling
- A linter, type checker, or `raise`/`assert` silenced to make the failure stop appearing
