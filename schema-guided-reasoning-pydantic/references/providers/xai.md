# xAI (Grok)

xAI's API is OpenAI-compatible. Use the OpenAI Python SDK with the xAI base URL.

**Python:** same pattern as OpenAI — `chat.completions.create` with `response_format` → [`../api-call-examples.md`](../api-call-examples.md#openai-python-sdk-parse) (substitute xAI base URL and model).

Official docs: [xAI Structured Outputs](https://docs.x.ai/docs/guides/structured-outputs).

---

## Adversarial enforcement results (grok-3-mini)

### Enforced (adversarial, no `strict: true` needed)

| Constraint | Pydantic | Result |
|---|---|---|
| `enum` / Literal route lock | `Literal[...]` | ✅ |
| Required fields | BaseModel default | ✅ |
| `additionalProperties: false` | `ConfigDict(extra="forbid")` | ✅ |
| `maximum` / `minimum` | `Field(le=, ge=)` | ✅ |
| `exclusiveMaximum` / `exclusiveMinimum` | `Field(lt=, gt=)` | ✅ |
| `maxLength` / `minLength` (string) | `Field(max_length=, min_length=)` on str | ✅ |
| `multipleOf` | `Field(multiple_of=)` | ✅ |
| `maxItems` / `minItems` | `Field(max_length=, min_length=)` on list | ✅ |
| `pattern` | `Field(pattern=)` | ✅ |
| Nested object (2 levels) | nested BaseModel | ✅ |
| `$defs` / `$ref` reuse | shared sub-models | ✅ |
| `anyOf` (nullable `T \| None`) | `Optional[T]` | ✅ |
| `anyOf` (`Union[A, B]`) | `Union[A, B]` | ✅ |
| `oneOf` (discriminated union) | Literal-discriminated union | ✅ |

### Not enforced

| Constraint | Result | Note |
|---|---|---|
| `allOf` (schema inheritance) | ❌ returns `{}` | xAI documents multi-subschema `allOf` as best-effort; flatten parent fields into child model |

Unlike OpenAI, xAI does not require `strict: true` for constraint enforcement to apply.

The official docs separate guaranteed constraints from best-effort keywords. `allOf` with more than one subschema, `not`, `if` / `then` / `else`, unsupported `format` values, and constraints above documented limits are accepted but not structurally enforced; validate if strict conformance matters.

---

## SGR implication

Use the same schema you designed for OpenAI (with `strict: true`). No special transport derivative needed for xAI based on current observations. Still validate server-side—empirical coverage here is one model and one model version.

---

## Available models (as of May 2026)

`grok-3`, `grok-3-mini`, `grok-4-*` series. Check `/v1/models` for the current list.
