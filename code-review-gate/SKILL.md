---
name: code-review-gate
version: 1.0.0
description: Automated pre-commit review — security scan, quality gates, and auto-fix suggestions. Catches secrets, dead code, and common anti-patterns before they hit main.
tags: [code-review, security, quality, pre-commit]
---

# Code Review Gate

Run this skill before every commit to main or before approving a PR. It produces a structured review that catches common problems automatically.

## When to Use

- Before merging any PR
- Before committing to main
- When asked "review this code" or "is this ready to ship?"

## Steps

1. **Identify changed files.** Run `git diff --name-only main...HEAD` (or equivalent). If no git repo, ask the user which files to review.

2. **For each changed file**, check these categories:

   **Security:**
   - Hardcoded secrets, API keys, tokens, passwords (regex: `/api[_-]?key|secret|token|password|auth.*=.*['\"][^'\"]{8,}/i`)
   - SQL injection patterns (string concatenation in queries)
   - eval() or exec() with user input
   - Insecure deserialization (pickle.loads with untrusted data)
   - CORS misconfiguration (Access-Control-Allow-Origin: *)
   - Missing auth checks on routes that modify data

   **Quality:**
   - Dead code (unreachable returns, unused imports, commented-out code blocks > 3 lines)
   - Functions > 50 lines (flag for refactoring)
   - Nested conditionals > 3 levels deep
   - Magic numbers without named constants
   - Console.log/print statements left in production code

   **Correctness:**
   - Off-by-one errors in loops and array access
   - Missing error handling on I/O operations (file, network, DB)
   - Race conditions in async code (missing await, unhandled promises)
   - Type mismatches between function signatures and callers

3. **Produce the review output** in this format:

   ```
   ## Code Review: [branch or files]

   **Verdict:** APPROVE / REQUEST CHANGES / NEEDS DISCUSSION

   ### Critical (must fix before merge)
   - [ ] [issue description] — `file:line`

   ### Warning (should fix soon)
   - [ ] [issue description] — `file:line`

   ### Suggestion (nice to have)
   - [ ] [issue description] — `file:line`

   ### Stats
   - Files reviewed: N
   - Critical issues: N
   - Warnings: N
   - Suggestions: N
   ```

4. **Auto-fix** where possible. For each issue found, if there's a safe mechanical fix (removing unused imports, adding `if err != nil` checks), apply it and note it in the review. Do NOT auto-fix security issues — flag them for human review.

5. **If verdict is APPROVE**, suggest a commit message in conventional format: `type(scope): description`.

## Pitfalls

- Don't review files you haven't read. Always read the full file, not just the diff context.
- Don't flag style preferences as critical. Use "suggestion" for formatting and naming debates.
- Don't auto-fix anything that changes runtime behaviour. Only remove dead code and add obvious safety checks.
- If the change is > 500 lines, ask the user to narrow the scope rather than reviewing everything at once.

## Source and licence

MIT-licensed source, worked example and installation instructions: [skyestrela/ai-agent-skill-preview](https://github.com/skyestrela/ai-agent-skill-preview).
