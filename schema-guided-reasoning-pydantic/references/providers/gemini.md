# Google Gemini (structured output transports)

Gemini exposes **two** ways to get typed JSON. Behavior differs between **native** Gemini structured output and **OpenAI-compatible** HTTP surfaces—plan SGR transports accordingly.

**Python (`google-genai`):** `GenerateContentConfig` + `model_json_schema()` → [`../api-call-examples.md`](../api-call-examples.md#gemini-python-sdk-json-schema).

Official docs:

- [Gemini API structured output](https://ai.google.dev/gemini-api/docs/structured-output)
- [Vertex AI structured output](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/control-generated-output)
- [Gemini OpenAI compatibility](https://ai.google.dev/gemini-api/docs/openai)

---

## Native Gemini structured output (`google-genai` SDK)

More permissive around optional/nullable fields and nested schemas than strict OpenAI mode. Still validate exported schema for your SDK/version. Apply SGR in-schema (route literals, branch containers, reasoning order); do not rely on descriptions alone.

Gemini documents a JSON Schema subset. Unsupported fields can be ignored rather than rejected on some Gemini/Vertex surfaces, so do not assume that a keyword present in a generated Pydantic schema is part of the constrained output contract.

---

## OpenAI-compatible route (`/v1beta/openai/`)

Unlike OpenAI, Gemini enforces constraints **without** needing `strict: true` in the request. Tested on `gemini-2.0-flash` using adversarial prompts (prompt instructs the model to violate the schema):

### Enforced (adversarial)

| Constraint | Pydantic | Result |
|---|---|---|
| `maximum` / `minimum` | `Field(le=, ge=)` | ✅ |
| `maxItems` on arrays | `Field(max_length=)` on list | ✅ |
| Single-value `enum` / Literal route lock | `Literal[...]` | ✅ |
| Required fields | BaseModel default | ✅ |
| `additionalProperties: false` | `ConfigDict(extra="forbid")` | ✅ |
| Nested object (2 levels) | nested BaseModel | ✅ |
| `anyOf` (nullable `T \| None`) | `Optional[T]` / `T \| None` | ✅ |
| `anyOf` (`Union[A, B]`) | `Union[A, B]` | ✅ |
| `oneOf` (discriminated union) | Literal-discriminated union | ✅ |

### Not enforced

| Constraint | Pydantic | Result | Note |
|---|---|---|---|
| `exclusiveMaximum` / `exclusiveMinimum` | `Field(lt=, gt=)` | ❌ | Model ignores exclusive bounds |
| `maxLength` / `minLength` (string) | `Field(max_length=, min_length=)` on str | ❌ | Model ignores length bounds |
| `multipleOf` | `Field(multiple_of=)` | ❌ | Model ignores |
| `pattern` | `Field(pattern=)` | ❌ | Model follows prompt, ignores pattern |
| `minItems` on arrays | `Field(min_length=)` on list | ⚠️ partial | Intermittent enforcement |
| `allOf` (inheritance) | subclassing BaseModel | ❌ | Returns `{}` — schema not resolved |
| `const` inside `$defs` | `Literal[...]` in sub-model via `$ref` | ⚠️ | May not be enforced; use direct `enum` |

**`pattern`, string/number bounds, and `allOf` are not enforced on Gemini OpenAI-compatible.** Validate these server-side.

### Critical: `max_tokens` must be generous

Gemini 2.5 Flash is verbose. When the schema contains open-ended `string` fields (e.g. `reasoning: str`), the model generates more text than a small token budget allows. With `max_tokens=200` and a reasoning field, responses were truncated mid-JSON in 4/5 runs. With `max_tokens=800`, all 5/5 passed.

**Rule:** set `max_tokens ≥ 800` for any SGR schema containing reasoning fields or other long strings. For multi-finding Cycle schemas, use more.

### SGR implication

- Keep a **canonical** semantic schema.
- For this transport: set generous `max_tokens`; back `pattern`, string/number bounds, and `allOf` with server-side validation.
- Treat `minItems` as probabilistic; prefer branch containers over complex union arrays.
- Avoid schema inheritance (`allOf`) — flatten parent fields into the child model instead.
