---
name: minimax-image-generator
description: Generate images from text prompts using the MiniMax image generation API — covers the global and China endpoints, the image-01 models, the full request schema, and both URL and base64 response handling.
---

# MiniMax Image Generator — Text-to-Image Generation

Generate images from natural-language prompts using the MiniMax `image_generation` API. This skill documents the exact endpoints, request schema, and response formats so an agent can produce images reliably and read the results correctly.

## Core Principle — THE IRON LAW

**"NEVER REPORT AN IMAGE AS GENERATED WITHOUT A SUCCESSFUL API RESPONSE."**

Do not fabricate image URLs, base64 payloads, or file paths. Every image you report must come from an `image_generation` call whose response has `base_resp.status_code == 0` and a non-empty `data.image_urls` (or base64 image list). If `base_resp.status_code` is non-zero, surface the error — do not invent a result.

## When to Use This Skill

Use this skill whenever the user's request involves any of these:

- Generating an image from a text description (text-to-image)
- Producing UI mockups, icons, illustrations, concept art, or marketing visuals from a prompt
- Creating multiple variations of an image from a single prompt
- Rendering images at a specific aspect ratio or exact pixel dimensions
- Producing reproducible images by fixing a random seed
- Any mention of: "generate an image", "text to image", "make a picture of", "create an illustration", "MiniMax image", "image-01"

**Do NOT use** this skill for speech, video, or music generation — those are separate MiniMax capabilities with different endpoints.

## Required Setup

- **API Key**: Bearer token from the MiniMax platform
- **Auth Header**: `Authorization: Bearer <MINIMAX_API_KEY>`
- **Content-Type**: `application/json`

### Regional Endpoints

Pick the endpoint that matches the account region. The request and response schemas are identical across regions.

| Region      | Endpoint                                          |
|-------------|---------------------------------------------------|
| Global      | `POST https://api.minimax.io/v1/image_generation`  |
| Mainland CN | `POST https://api.minimaxi.com/v1/image_generation` |

Do not mix regions: use the API key issued for the same platform as the endpoint host.

## Models

| Model            | Notes                                                        |
|------------------|--------------------------------------------------------------|
| `image-01`       | Default general-purpose text-to-image model                  |
| `image-01-live`  | Text-to-image model tuned for illustration / live-art styles |

Use `image-01` unless the user asks for the illustration-oriented variant.

## Request Schema

```
POST /v1/image_generation
Content-Type: application/json
Authorization: Bearer <MINIMAX_API_KEY>

{
  "model": "image-01",
  "prompt": "A serene mountain lake at sunrise, photorealistic",
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 1,
  "prompt_optimizer": true
}
```

**Fields:**

| Field               | Type    | Required | Description                                                                  |
|---------------------|---------|----------|------------------------------------------------------------------------------|
| `model`             | string  | Yes      | Model id: `image-01` or `image-01-live`.                                      |
| `prompt`            | string  | Yes      | Text description of the image to generate.                                    |
| `subject_reference` | array   | No       | Reference image(s) used to keep a consistent subject across generations.      |
| `aspect_ratio`      | string  | No       | Output aspect ratio, e.g. `1:1`, `16:9`, `9:16`, `4:3`, `3:4`.                |
| `width`             | integer | No       | Explicit output width in pixels (use with `height` instead of `aspect_ratio`). |
| `height`            | integer | No       | Explicit output height in pixels (use with `width` instead of `aspect_ratio`). |
| `response_format`   | string  | No       | `url` (default) or `base64` — how generated images are returned.              |
| `seed`              | integer | No       | Fixed random seed for reproducible output.                                    |
| `n`                 | integer | No       | Number of images to generate in one call.                                     |
| `prompt_optimizer`  | boolean | No       | When `true`, the service refines the prompt before generation.                |

**Sizing rule:** provide either `aspect_ratio`, or the `width`/`height` pair — not both. If neither is given, the model uses its default size.

## Response Handling

A successful call returns image data plus a status block. Always check `base_resp.status_code` first.

```json
{
  "data": {
    "image_urls": [
      "https://.../generated-image-0.png",
      "https://.../generated-image-1.png"
    ]
  },
  "metadata": {
    "success_count": 2,
    "failed_count": 0
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

**Fields to read:**

| Field                    | Meaning                                                          |
|--------------------------|------------------------------------------------------------------|
| `data.image_urls`        | List of generated image URLs (when `response_format` is `url`).  |
| `metadata.success_count` | How many images were generated successfully.                     |
| `metadata.failed_count`  | How many generations failed within the batch.                    |
| `base_resp.status_code`  | `0` means success; any other value means the request failed.     |

### URL vs base64

- **`response_format: "url"`** (default): images are returned in `data.image_urls`. **These URLs expire 24 hours after generation** — download and persist any image the user needs to keep before the TTL elapses.
- **`response_format: "base64"`**: images are returned as base64-encoded strings in the response instead of URLs. Decode them and write the bytes to a file; nothing needs to be downloaded and there is no expiry to worry about.

### Reading a batch

When `n > 1`, iterate over `data.image_urls` (or the base64 list). Cross-check `metadata.success_count` and `metadata.failed_count`: if `failed_count > 0`, tell the user some images in the batch did not render and offer to retry.

## Recommended Workflow

1. Turn the user's request into a clear, descriptive `prompt`.
2. Choose the model (`image-01` by default).
3. Set sizing via `aspect_ratio` **or** `width`/`height`.
4. Choose `response_format`: `url` for quick previews, `base64` when the user needs the bytes directly.
5. Set `n` if the user wants multiple options; set `seed` if they want reproducibility.
6. POST to the region-appropriate endpoint.
7. Verify `base_resp.status_code == 0`, then read `data.image_urls` (or base64 payloads).
8. If `response_format` is `url`, remind the user the URLs expire in 24 hours and offer to save the files.

## Example

**User**: "Generate three 16:9 concept images of a cozy reading nook."

**Request**:
```json
{
  "model": "image-01",
  "prompt": "A cozy reading nook by a large window, warm lighting, plants, soft blanket",
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 3,
  "prompt_optimizer": true
}
```

**Output**:
```
Generated 3 images (success_count: 3, failed_count: 0).

1. https://.../nook-0.png
2. https://.../nook-1.png
3. https://.../nook-2.png

Note: these URLs expire in 24 hours — say the word and I'll download them locally.
```

## Tips

- Keep prompts concrete and visual; describe subject, style, lighting, and composition.
- Use `seed` to iterate on the same base image while tweaking the prompt.
- Prefer `base64` when the workflow needs to persist images immediately without a follow-up download step.
- Use `subject_reference` when the user needs the same character or subject to recur across images.

## Common Use Cases

- **Product & marketing visuals**: hero images, banners, ad creative from a brief.
- **UI & design mockups**: quick illustrative placeholders for layouts.
- **Editorial illustration**: article headers and blog artwork with `image-01-live`.
- **Batch exploration**: generate several variations (`n > 1`) to pick from.

## Error Handling

Always inspect `base_resp.status_code` and `base_resp.status_msg`:

| Symptom                      | Likely cause                    | Resolution                                                |
|------------------------------|---------------------------------|-----------------------------------------------------------|
| `base_resp.status_code != 0` | Request rejected by the service | Read `status_msg`, fix the offending field, retry.        |
| Missing `data.image_urls`    | No image produced               | Check `metadata.failed_count` and the status message.     |
| `failed_count > 0`           | Part of the batch failed        | Retry the failed portion of the batch.                    |
| Expired image link           | URL past its 24-hour TTL        | Regenerate, or use `response_format: "base64"` next time. |
| Auth error                   | Invalid or wrong-region API key | Verify the key matches the endpoint region.               |

## Reference

- **Global docs**: https://platform.minimax.io/docs/api-reference/image-generation-t2i
- **Mainland CN docs**: https://platform.minimaxi.com/docs/api-reference/image-generation-t2i

**Credit:** Based on the MiniMax image generation API reference.
