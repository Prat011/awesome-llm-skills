---
name: saas-idea-validator
description: Guides solo founders through structured SaaS idea validation. Problem definition, market signals, competitor landscape, and go/no-go recommendation. Use before building anything.
---

# SaaS Idea Validator

Guides solo SaaS founders through structured idea validation before writing any code. Prevents building a product nobody wants by forcing a disciplined evaluation workflow.

## When to Use This Skill

- You have a SaaS idea and want to validate it before building
- You are choosing between multiple product ideas
- A friend or client suggested "you should build X" and you want to check if it is viable
- You are transitioning from freelance/agency work to a product business

## What This Skill Does

1. **Problem articulation**: Describe the problem in customer language, not solution language. Forces "who has this problem, how often, and what do they do about it today?"
2. **Market signal detection**: Searches for real demand signals such as Reddit threads, Twitter complaints, forum discussions, and "how do I..." queries that indicate people actively looking for a solution.
3. **Competitor mapping**: Identifies direct competitors, indirect competitors, and "good enough" alternatives. Analyzes positioning, pricing, and gaps.
4. **Willingness-to-pay assessment**: Evaluates whether the problem is painful enough and frequent enough that people would pay. Flags "vitamin vs painkiller" distinction.
5. **Go/no-go recommendation**: Structured report with evidence, risk assessment, confidence level, and concrete next steps.

## How to Use

### Basic Usage

```
Validate my SaaS idea: [describe your idea in 2-3 sentences]
```

### Advanced Usage

```
I have 3 SaaS ideas. Help me validate and rank them:
1. [Idea A]
2. [Idea B]
3. [Idea C]
Constraints: solo founder, $0 ad budget, 60 days to first revenue.
```

## Example Output

User validates "a tool that auto-generates changelogs from git commits for SaaS companies." Output includes:

- **Problem**: SaaS teams spend 1-2 hours per release writing changelogs. Git commits are too technical for customers.
- **Market signals**: 15+ Reddit threads, Twitter discussions with 47+ replies seeking solutions.
- **Competitors**: Canny.io (side feature), Beamer (weak git integration), Headway (no AI). Gap: AI-generated changelogs from git diffs.
- **Willingness to pay**: Recurring problem every 1-2 weeks, target market pays $20-100/mo for dev tools. VERDICT: Willing to pay.
- **Recommendation: GO (Confidence: High)**. Clear demand, competitors validate market, low technical barrier, first revenue possible in 30 days.

## Common Use Cases

- Validating a SaaS product idea before committing weeks of build time
- Comparing multiple ideas to decide which to build first
- Stress-testing an idea against real market evidence
- Getting a structured outside perspective when too close to an idea

## Tips

- Be specific about the target customer. "Developers" is too broad. "Solo React developers deploying on Vercel who hate writing documentation" is specific enough.
- Weak market signals are the most important data ? do not ignore them.
- Competitors existing is good news: it means the market exists.
- Run this on every idea, even ones you "know" will work. Confirmation bias is the #1 startup killer.

Inspired by the [SaaS Founder Claude Code Skill Pack](https://github.com/ttcd77/saas-founder-claude-pack) ? 10 custom Claude Code commands for solo SaaS founders. This skill is a free, open-source sample.

