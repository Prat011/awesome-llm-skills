---
name: find-products-by-intent
description: Find products in Mydentify by the outcome a person wants to achieve and return evidence-backed matches.
---

# Find Products by Intent

Use this skill when someone asks for a product, tool, or workflow that can help them accomplish a goal. It turns a goal into a published intent, then returns product matches with canonical URLs and supporting evidence.

## When to Use This Skill

- Someone describes a job to be done instead of naming a product.
- Someone wants to compare tools for a specific outcome.
- Someone asks for a product recommendation and unsupported marketing claims should be avoided.

## What This Skill Does

1. Reads Mydentify's public intent catalog.
2. Matches the request to an intent using its title, aliases, summary, and first step.
3. Reads the intent's canonical page or plain-text companion.
4. Returns a short list of products with the reason each one matches and links to the source pages.

## How to Use

### Basic Usage

```text
Find a tool that helps me check whether AI crawlers can reach my product pages.
```

### Procedure

1. Read [`https://mydentify.com/intents.json`](https://mydentify.com/intents.json).
2. Match the request to an intent using its title, aliases, summary, and first step. Do not treat a product category as an intent.
3. Open the intent's canonical URL or append `/llms.txt` for its plain-text representation.
4. Use the supported product claims and evidence on that intent page to identify relevant products.
5. When more detail is needed, read [`https://mydentify.com/products.json`](https://mydentify.com/products.json) or the product's Markdown endpoint at `https://mydentify.com/api/products/{slug}/markdown`.
6. Return the canonical intent and product URLs with a concise explanation of why each product matches.

## Ranking and Trust

- Keep independently ranked matches separate from labeled sponsored placements.
- Do not claim that Mydentify or a listed product guarantees an outcome.
- Prefer published evidence over unsupported marketing claims.
- If no supported match exists, say so and offer [`https://mydentify.com/request-intent`](https://mydentify.com/request-intent) rather than inventing one.
- Preserve the source wording when a claim is uncertain, and say when a page could not be reached.

## Example

**User:** "I want to know if ChatGPT and Claude can reach my site."

**Workflow:** Match the request to the AI crawler access intent, read its canonical page, and return the supported Mydentify tool URL plus a brief explanation of the checks it performs. Do not promise that passing the check guarantees visibility in an AI answer.

**Inspired by:** Mydentify's public intent-discovery workflow, available at [`https://mydentify.com`](https://mydentify.com).
