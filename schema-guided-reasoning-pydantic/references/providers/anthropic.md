# Anthropic Claude Structured Outputs

Anthropic exposes two structured-output surfaces:

- **JSON outputs** via `output_config.format` for Claude's final response.
- **Strict tool use** via `strict: true` on tool definitions for tool input schemas.

Official docs:

- [Structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)
- [Strict tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/strict-tool-use)

This profile combines Anthropic documentation with live adversarial checks against `claude-sonnet-4-6` through an Anthropic-compatible gateway in May 2026. Treat it as a starting point and validate your real schema against your real Claude endpoint.

---

## Role in an SGR workflow

Claude can use constrained decoding for both final JSON outputs and strict tool inputs, but Anthropic's supported JSON Schema subset is narrower than full JSON Schema. SGR schemas should keep routing explicit, flatten inheritance-heavy structures, and avoid relying on constraints that Anthropic documents as SDK-validated rather than API-enforced.

---

## Contract and limitations

- Use `output_config.format` with `type: "json_schema"` for final structured JSON.
- Use `strict: true` on tools when tool input conformance matters.
- Both JSON outputs and strict tool use share the same JSON Schema limitations.
- Objects must use `additionalProperties: false`.
- `required` is supported; optional fields increase grammar complexity.
- `anyOf` is supported, but union parameters count against explicit complexity limits.
- `allOf` is supported with limitations; `allOf` with `$ref` is not supported.
- `$ref`, `$def`, and `definitions` are supported, but external `$ref` is not.
- `enum` supports strings, numbers, booleans, and nulls; complex enum values are not supported.
- String formats are limited to documented values such as `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, and `uuid`.
- `pattern` supports a practical regex subset; complex patterns can produce 400 errors.

---

## Constraints that are not API-enforced

Anthropic documents these as unsupported in the schema subset:

| Constraint family | Examples | SGR implication |
|---|---|---|
| Numerical constraints | `minimum`, `maximum`, `multipleOf` | Do not rely on constrained decoding; validate after response. |
| String length constraints | `minLength`, `maxLength` | Prefer enum / route structure for critical choices; validate after response. |
| Array constraints beyond `minItems` 0 or 1 | `minItems: 2`, `maxItems` | Use prompt policy + validation, or split the task into smaller structured steps. |
| `additionalProperties` values other than `false` | schema-valued or `true` forms | Keep exported SGR objects closed. |

Anthropic SDKs for Python, TypeScript, Ruby, and PHP may automatically transform unsupported features by removing constraints from the wire schema, adding constraint text to descriptions, and validating the parsed response against the original local model. That means a Pydantic constraint can exist in your code without being enforced by Claude's constrained decoder.

---

## Live adversarial results (`claude-sonnet-4-6`)

Each case used `output_config.format` with `type: "json_schema"` and a prompt that explicitly asked Claude to violate the schema.

| Constraint / keyword | Result | Observed behavior |
|---|---|---|
| `enum` / `Literal` | ✅ enforced | Prompt asked for forbidden value; output used allowed enum. |
| Required field | ✅ enforced | Prompt asked for `{}`; output included required key with an empty string. |
| `additionalProperties: false` | ✅ enforced | Prompt asked for an extra key; output omitted it. |
| `additionalProperties: true` | 💥 400 | API requires `additionalProperties: false`. |
| `minimum` / `maximum` on integer | 💥 400 | API rejected schema: `maximum`, `minimum` not supported for integer. |
| `minLength` / `maxLength` on string | ❌ not enforced | API accepted schema but returned the too-short prompt value. |
| Simple `pattern` | ✅ enforced | Prompt asked for lowercase `abc`; output returned uppercase `ABC`. |
| `minItems: 2` | 💥 400 | API supports only `minItems` values `0` or `1`. |
| `maxItems` | 💥 400 | API rejected `maxItems` as unsupported. |
| `anyOf` string/null | ✅ enforced | Prompt asked for number `42`; output converted to string `"42"`. |
| `type: ["string", "null"]` | ✅ enforced | Prompt asked for number `42`; output converted to string `"42"`. |
| `oneOf` | 💥 400 | API rejected schema type `oneOf` as unsupported. |
| Simple `allOf` without `$ref` | ✅ enforced | Prompt omitted parent field; output included both merged fields. |
| `allOf` with `$ref` | 💥 400 | API rejected merge: `allOf` schema contained `$ref`. |

---

## Property ordering

Anthropic preserves object property ordering with one important caveat: required properties appear first, followed by optional properties. If field order is part of your SGR path, mark reasoning checkpoints, route locks, and decision-impact fields as required.

---

## Invalid-output paths

Structured outputs can still fail to match the schema when:

- Claude refuses for safety reasons.
- The response reaches `max_tokens` and is truncated.

Branch on these cases before parsing into your Pydantic model.

---

## Complexity limits

Anthropic compiles schemas into grammars. Complex schemas can fail even when logically valid.

Documented explicit limits include:

- Up to **20** strict tools per request.
- Up to **24** optional parameters across all strict tool schemas and JSON output schemas.
- Up to **16** union parameters using `anyOf` or type arrays across all strict schemas.

For SGR, reduce optional fields, split large workflows into multiple requests, and avoid large mixed-union schemas.

---

## Preflight checklist

- [ ] Chosen surface is correct: `output_config.format` for final JSON, `strict: true` for tool inputs.
- [ ] Every exported object uses `additionalProperties: false`.
- [ ] Critical SGR path fields are required so ordering remains stable.
- [ ] No reliance on API enforcement for numeric bounds, string lengths, `multipleOf`, or array bounds beyond `minItems` 0/1.
- [ ] `allOf` is avoided, especially `allOf` with `$ref`; flatten inheritance when possible.
- [ ] Union count and optional-field count are within Anthropic limits.
- [ ] Caller handles refusal and `max_tokens` truncation before parsing.
