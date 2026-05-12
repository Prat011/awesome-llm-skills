# API call examples (Pydantic schema → provider)

Copy-ready **Python** patterns: ship a JSON Schema derived from Pydantic and read structured output. Transport constraints stay in the provider profiles under [`providers/`](./providers/).

**Sources:** [openai-python `helpers.md` — Structured Outputs parsing](https://github.com/openai/openai-python/blob/main/helpers.md); [googleapis/python-genai — JSON response schema](https://github.com/googleapis/python-genai) (see repository README / codegen instructions for `GenerateContentConfig` + `response_json_schema`).

---

## OpenAI Python SDK parse

The OpenAI Python SDK converts your Pydantic model to JSON Schema, sends it on the request, and parses a successful assistant message into that model (`message.parsed`). On refusal, use `message.refusal`.

```python
from pydantic import BaseModel
from openai import OpenAI

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str

client = OpenAI()
completion = client.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor."},
        {"role": "user", "content": "solve 8x + 31 = 2"},
    ],
    response_format=MathResponse,
)

message = completion.choices[0].message
if message.parsed:
    print(message.parsed.final_answer)
else:
    print(message.refusal)
```

**SGR:** replace `MathResponse` with your route-locked root model (`Literal` branch locks, reasoning-first order, `ConfigDict(extra="forbid")` on exported objects).

**Transport:** the exported schema must meet [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) rules (summary in `providers/openai-structured-outputs.md`).

---

## Gemini Python SDK JSON schema

Install: `pip install google-genai`. Create a client (Gemini Developer API key or Vertex—see SDK docs), set `response_mime_type` and pass schema via `response_json_schema` (dict or `model_json_schema()`).

```python
from pydantic import BaseModel
from google import genai
from google.genai import types

class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Give me information for the United States.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_json_schema=CountryInfo.model_json_schema(),
    ),
)

text = response.text
assert text is not None
parsed = CountryInfo.model_validate_json(text)
print(parsed.name)
```

**SGR:** swap `CountryInfo` for your SGR root model.

**Transport:** enforcement varies by surface (native vs OpenAI-compatible); see `providers/gemini.md` before relying on string or array bound keywords.

The same SDK also accepts a raw JSON Schema `dict` under `response_json_schema` when you are not using Pydantic—still pair with `response_mime_type="application/json"` (see upstream examples in python-genai).
