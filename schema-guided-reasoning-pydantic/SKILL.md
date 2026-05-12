---
name: schema-guided-reasoning-pydantic
description: Design or refactor a Pydantic schema for LLM structured output using Schema-Guided Reasoning (SGR). Use when designing response_format/output_config schemas, adding route locks with Literal fields, choosing Cascade/Routing/Cycle patterns, checking OpenAI/Gemini/Anthropic/xAI structured output compatibility, or making a model follow a specific reasoning path via constrained decoding.
---

# Schema-Guided Reasoning for Pydantic

Design **Schema-Guided Reasoning (SGR)** into Pydantic models used as LLM structured-output protocols: constrained decoding supplies shape; **the schema supplies the reasoning path**—ordered checkpoints, explicit branches, bounded repetition—so outputs stay auditable and testable.

Use **prompt + schema** together; neither replaces the other.

**Calling APIs with your Pydantic schema:** copy-ready OpenAI (`chat.completions.parse`) and Gemini (`google-genai` + `model_json_schema()`) snippets live in [`references/api-call-examples.md`](references/api-call-examples.md). Provider transport constraints live in [`references/providers/`](references/providers/).

## Provider enforcement: empirical data, not permanent truth

The constraint enforcement tables in `references/cross-cutting-caveats.md` and per-provider files are based on **adversarial tests run against real APIs at a specific point in time**, plus official documentation where a keyword was not directly exercised. Provider SO implementations change—new model versions, API updates, and backend changes can silently alter which constraints are enforced.

**Before relying on any constraint as a hard guarantee:**
1. Test your actual schema adversarially against your actual provider.
2. Re-verify after any provider or model upgrade.
3. Always validate server-side with `model_validate` regardless of what the table says.

Treat the tables as a useful starting point, not a specification.

---

## Non-negotiable guardrails

1. Encode route choice with single-value `Literal[...]` fields (branch locks).
2. Do **not** rely on post-validation for **core route admissibility**—that belongs in structure.
3. In each branch/result object, order fields: **reasoning → route locks → decision-impact fields → evidence/detail**. If there is no scoring, keep the same intent: reasoning first, then branch identity, then payload that changes decisions, then supporting detail.

## Workflow

1. **Route matrix** — branch × allowed codes × required fields × decision/score impact.
2. **Map to SGR patterns** — Cascade (ordered steps), Routing (explicit branch), Cycle (bounded lists). Details: [`references/patterns.md`](references/patterns.md).
3. **Choose a schema shape** compatible with your provider’s transport (split branch containers when arrays cannot carry unions). Keep one **canonical** semantic schema; add **derived** variants only where a provider forces them: [`references/README.md`](references/README.md).
4. **Encode constraints** — `Literal`, bounded numeric/list constraints where proven safe, `extra="forbid"` on objects you export. **Required/null and strict subsets are provider-specific** → [`references/providers/openai-structured-outputs.md`](references/providers/openai-structured-outputs.md), [`references/providers/gemini.md`](references/providers/gemini.md), [`references/providers/anthropic.md`](references/providers/anthropic.md), [`references/providers/xai.md`](references/providers/xai.md).
5. **Align the prompt** — same branch names, code sets, and required fields as the schema.
6. **Preflight** — validate exported JSON Schema against the rules for **your** endpoint before runtime (keywords, size, nesting).
7. **Tests** — invalid routes, missing decision fields, extra keys, export smoke checks, and **caller handling** for provider edge responses (e.g. refusal/incomplete where applicable).

## SGR pattern mapping

### Cascade

Ordered fields force thought sequence (e.g. summarize → score → final decision).

### Routing

Branch models with branch-specific literals; for strict transports prefer **separate containers per branch** over mixed union arrays.

### Cycle

Bounded lists (`Annotated` / min-max items) for repeated findings or steps.

*(Expanded playbook: [`references/patterns.md`](references/patterns.md).)*

## Route enforcement strategy

- **Primary:** schema shape — branch literals, branch-local code/status sets, required decision-critical fields.
- **Secondary:** `model_validator` / service checks — only for invariants you cannot express structurally.

## Field order standard

Per branch/result model, prefer:

1. `reasoning`
2. Branch route fields (`dimension`, `code`, `status`, … as literals)
3. Decision-impact fields (`materiality`, severity, outcome, …)
4. Evidence anchors / refs
5. Supporting optional fields (per provider rules for “optional”)

Example (judge-like): `reasoning` → `dimension` → `code` → `materiality` → `evidence_refs` → notes.

## Multi-branch collection blueprint

Prefer **separate arrays per branch family** instead of `list[Union[A,B]]` when the transport rejects unions in items:

- `verdict_findings` / `justification_findings`
- `positives` / `risks`
- `matched_items` / `missing_items`

Each item model carries its branch literal and its own code set; empty list means “none for that branch.” Use this to avoid `oneOf` inside array items when the API is strict.

## Quality checklist

- [ ] Route locks are single-value literals; branch code sets do not overlap wrongly across branches.
- [ ] Reasoning-first field order on branch objects.
- [ ] Canonical schema documented; provider derivatives only where required.
- [ ] Preflight passed for **your** provider file (OpenAI / Gemini / Anthropic / xAI).
- [ ] Prompt enumerates same branches and literals as the schema.
- [ ] Tests cover bad routes, missing critical fields, export constraints, and non-parse success paths.

## References

**External**

- OpenAI Structured Outputs (upstream guide): [developers.openai.com — structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- Gemini Structured Output (upstream guide): [ai.google.dev — structured output](https://ai.google.dev/gemini-api/docs/structured-output)
- Anthropic Structured Outputs (upstream guide): [docs.claude.com — structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)
- Anthropic Strict Tool Use (upstream guide): [docs.claude.com — strict tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/strict-tool-use)
- xAI Structured Outputs (upstream guide): [docs.x.ai — structured outputs](https://docs.x.ai/docs/guides/structured-outputs)
- SGR overview: [abdullin.com — schema-guided-reasoning](https://abdullin.com/schema-guided-reasoning/)
- SGR patterns: [patterns](https://abdullin.com/schema-guided-reasoning/patterns)
- Structured output caveats (general): [structured-output](https://abdullin.com/structured-output/)

**Local**

| | |
|--|--|
| Index of all reference docs | [`references/README.md`](references/README.md) |
| Pattern playbook | [`references/patterns.md`](references/patterns.md) |
| Templates | [`references/templates.md`](references/templates.md) |
| Cross-cutting caveats (all providers) | [`references/cross-cutting-caveats.md`](references/cross-cutting-caveats.md) |
| OpenAI transport | [`references/providers/openai-structured-outputs.md`](references/providers/openai-structured-outputs.md) |
| Gemini transports | [`references/providers/gemini.md`](references/providers/gemini.md) |
| Anthropic Claude transport | [`references/providers/anthropic.md`](references/providers/anthropic.md) |
| xAI / Grok transport | [`references/providers/xai.md`](references/providers/xai.md) |
| API examples (OpenAI + Gemini + Pydantic) | [`references/api-call-examples.md`](references/api-call-examples.md) |
