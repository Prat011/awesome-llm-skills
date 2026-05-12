# Cross-cutting caveats (all providers)

These apply regardless of which structured-output API you call.

---

## Schema constraints without enforcement are just hints

Passing a JSON Schema to the API does not automatically enforce every field in it. **Whether a constraint is actually enforced depends on the provider and how you call the API.**

> ⚠️ **This data was collected at a point in time.** Provider SO implementations change. Treat the table below as a starting reference, not a permanent guarantee. [Test your schema against the actual provider before relying on it.](#empirical-verification-workflow)

From adversarial testing (prompt instructs model to violate the schema, 3–5 runs per cell), plus Anthropic live checks where noted:

### Scalar / value constraints

| Constraint | Pydantic field | OpenAI (no strict) | OpenAI (strict=True) | Gemini OpenAI-compat | Anthropic | xAI |
|---|---|---|---|---|---|---|
| `enum` / Literal route lock | `Literal[...]` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `maximum` / `minimum` | `Field(le=, ge=)` | ❌ | ✅ | ✅ | 💥 raw 400 / SDK-validated | ✅ |
| `exclusiveMaximum` / `exclusiveMinimum` | `Field(lt=, gt=)` | ❌ | ✅ | ❌ | ⚠️ docs unsupported | ✅ |
| `maxLength` / `minLength` (string) | `Field(max_length=, min_length=)` | ❌ | ✅ | ❌ | ❌ accepted, not enforced | ✅ |
| `multipleOf` | `Field(multiple_of=)` | ❌ | ✅ | ❌ | ⚠️ docs unsupported | ✅ |
| `pattern` | `Field(pattern=)` | ❌ | ✅ | ❌ | ✅ simple subset / complex 400 | ✅ |

### Collection / structure constraints

| Constraint | Pydantic field | OpenAI (no strict) | OpenAI (strict=True) | Gemini OpenAI-compat | Anthropic | xAI |
|---|---|---|---|---|---|---|
| Required fields | default BaseModel | ❌ | ✅ | ✅ | ✅ | ✅ |
| `additionalProperties: false` | `ConfigDict(extra="forbid")` | ❌ | ✅ | ✅ | ✅ required | ✅ |
| `maxItems` / `minItems` | `Field(max_length=, min_length=)` on list | ❌ | ✅ | ✅ / ⚠️ partial | 💥 `maxItems` 400; `minItems` only 0/1 | ✅ |
| Nested object (2 levels) | nested `BaseModel` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `$defs` / `$ref` reuse | shared sub-models | ❌ | ✅ | ⚠️ partial¹ | ✅ no external refs | ✅ |

### Composition keywords

| Keyword | OpenAI (strict=True) | Gemini OpenAI-compat | Anthropic | xAI |
|---|---|---|---|---|
| `anyOf` (nullable `T \| None`) | ✅ | ✅ | ✅ with union limits | ✅ |
| `anyOf` (`Union[A, B]`) | ✅ | ✅ | ✅ with union limits | ✅ |
| `oneOf` (discriminated union) | 💥 400 API error | ✅ | 💥 400 API error | ✅ |
| `allOf` (schema inheritance) | 💥 400 API error | ❌ returns `{}` | ✅ simple / 💥 400 with `$ref` | ❌ returns `{}` |

¹ Gemini resolves `$defs` for structure, but `const` values inside `$defs` refs may not be enforced (model followed the prompt instead). Use `enum` in direct schemas rather than `const` inside `$defs` on Gemini.

Anthropic column combines official documentation with live `claude-sonnet-4-6` checks through an Anthropic-compatible gateway. Unsupported constraints may be stripped by SDK helpers and validated after the response, rejected with 400 when sent raw, or accepted but not enforced (`minLength` / `maxLength`). See [`providers/anthropic.md`](./providers/anthropic.md).

**Consequence:** always add service-side `model_validate` / post-validation after parsing. Treat constraints the provider does not enforce as policy (prompt + validation), not schema guarantees.

---

## Empirical verification workflow

Before relying on any constraint as a hard guarantee in your stack:

1. Write a **minimal schema** with only that constraint.
2. Send a prompt that explicitly instructs the model to violate it (adversarial).
3. Run ≥ 3 times (provider output can be non-deterministic).
4. If ≥ 1 violation is observed → constraint is not reliably enforced → validate server-side.

Provider SO implementations can change without notice (new model version, API update). Re-verify after provider upgrades if the constraint is safety/correctness critical.

---

## OpenAI: `strict: true` is mandatory

Without `strict: true`, OpenAI enforces none of the constraints above—the model follows the prompt, not the schema. See [`providers/openai-structured-outputs.md`](./providers/openai-structured-outputs.md).

---

## Anthropic: SDK transformation can hide enforcement gaps

Anthropic SDK helpers can remove unsupported constraints from the schema sent to Claude, append them to descriptions, and validate the parsed response locally. This is useful, but for SGR it means a Pydantic constraint is not necessarily part of the constrained-decoding grammar. See [`providers/anthropic.md`](./providers/anthropic.md).

---

## Schema descriptions are not a reliable policy channel

Some runtimes treat `Field(description=...)` as hidden prompt context; others ignore it.

- Do not put mandatory behavioral rules only in descriptions.
- Encode routing and admissibility in types (`Literal`, required fields, bounded collections).
- Duplicate critical policy in the prompt when it must hold.

**Smoke test:** ship a tiny schema whose only instruction lives in `description`. If behavior ignores it, descriptions are not dependable in your stack.

---

## Over-constrained schemas hurt accuracy

Constrained decoding can truncate reasoning quality when the schema is tighter than necessary.

**Mitigation via SGR:** keep mandatory checkpoints (Cascade), explicit branches (Routing), bounded repetition (Cycle), and drop decorative constraints that do not change decisions.

---

## Prompt + schema are joint contracts

- Prompt carries task policy and edge handling.
- Schema carries the output protocol, branch locks, and reasoning checkpoints.

Neither layer alone substitutes for the other.
