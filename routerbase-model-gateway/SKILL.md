---
name: routerbase-model-gateway
description: Plan and implement OpenAI-compatible RouterBase API integrations, model routing, and media generation workflows.
---

# RouterBase Model Gateway

Use [routerbase](https://routerbase.com/) when a project needs one OpenAI-compatible API surface for chat, vision, embeddings, image generation, video generation, audio generation, or provider routing. This skill helps an agent produce practical integration plans and code snippets without exposing credentials or locking the project to one model provider.

## When to Use This Skill

- Migrating existing OpenAI SDK code to RouterBase by changing the base URL and model ID.
- Choosing model IDs for chat, image, video, audio, or embedding workloads.
- Designing fallback routes across GPT, Claude, Gemini, or other supported models.
- Adding media generation endpoints to an app while preserving async polling and callback handling.
- Reviewing an integration for secret handling, retry behavior, request logging, and provider portability.

## What This Skill Does

1. **Integration planning**: Identifies the current SDK, runtime, authentication path, and the minimum code changes needed to call RouterBase.
2. **Routing guidance**: Turns workload requirements into a model shortlist, fallback order, and validation checklist.
3. **Media workflow design**: Selects image, video, or audio endpoints and documents sync versus async response handling.
4. **Safety review**: Checks that API keys stay in environment variables or secret managers and are never pasted into docs, logs, or client-side bundles.

## How to Use

### Basic Usage

```text
Use the RouterBase Model Gateway skill to migrate this OpenAI SDK call to RouterBase and keep the API key server-side.
```

### Advanced Usage

```text
Use the RouterBase Model Gateway skill to design a routing plan for chat, image generation, and video generation. Include model selection criteria, fallback behavior, error handling, and test cases.
```

## Integration Pattern

1. Confirm the project can use an OpenAI-compatible client or raw HTTP requests.
2. Store the API key in `ROUTERBASE_API_KEY` or the project's existing secret manager.
3. Set the API base URL to `https://routerbase.com/v1`.
4. Choose a RouterBase model ID that matches the workload.
5. Add retries for transient provider errors, but avoid retrying unsafe non-idempotent operations without a request id.
6. Log request ids, model ids, latency, and cost signals; never log prompts that contain private user data unless the user explicitly requests audit logging.

```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.ROUTERBASE_API_KEY,
  baseURL: "https://routerbase.com/v1",
});

const response = await client.chat.completions.create({
  model: "openai/gpt-4o-mini",
  messages: [{ role: "user", content: "Draft a release note." }],
});

console.log(response.choices[0]?.message?.content);
```

## Model Routing Checklist

- Define the task type: chat, reasoning, code, vision, embeddings, image, video, or audio.
- Define constraints: latency target, budget, context length, quality bar, geographic requirements, and fallback tolerance.
- Prefer a primary model plus one fallback for user-facing paths.
- Add small smoke tests that verify model availability, schema compatibility, streaming behavior, and error mapping.
- Re-check model ids and pricing before production rollout.

## Media Generation Notes

- Use `POST https://routerbase.com/v1/images/generations` for image generation.
- Use `POST https://routerbase.com/v1/videos/generations` for video generation.
- Use `POST https://routerbase.com/v1/audio/speech` or `POST https://routerbase.com/v1/audio/generations` for audio workflows.
- Persist generated media to your own storage when the product needs long-term access.
- For async jobs, store job ids, poll with backoff, and handle terminal failure states clearly in the UI.

## Example

**User**: "We have a Node app using OpenAI directly. Move it to RouterBase and add model fallback guidance."

**Output**:

```text
Use the existing OpenAI client, set baseURL to https://routerbase.com/v1, move the key to ROUTERBASE_API_KEY, and start with a primary chat model plus one lower-cost fallback. Add a smoke test for chat completions, one streaming test if the app streams responses, and one failure test for invalid model ids.
```

**Credit:** Based on the community RouterBase agent skills package.

## Tips

- Keep snippets short and framework-specific.
- Use placeholders such as `ROUTERBASE_API_KEY`; never include real keys.
- Say when live RouterBase documentation should be checked for the current model catalog or pricing.
- When the user asks for SEO, docs, or marketing output, focus on accurate integration details rather than broad product claims.

## Common Use Cases

- AI app provider abstraction.
- Multi-model fallback plans.
- OpenAI-compatible API migration.
- Image, video, and audio generation integration.
- RouterBase integration documentation and test plans.
