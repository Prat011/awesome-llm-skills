---
name: video-router
description: Routes a video-production brief to generation, composition, editing, or an end-to-end workflow before production begins.
---

# Video Router

Choose and state the primary production path before creating assets or editing media. This keeps the plan coherent while still allowing secondary techniques such as captions or generated B-roll.

## When to Use This Skill

- Starting a video request whose production method is not yet fixed
- Deciding how to use supplied footage, images, or references
- Planning a deliverable that may combine editing, generation, and motion graphics

## What This Skill Does

1. **Classifies the brief** by its dominant production object
2. **Selects one primary route** and identifies any supporting routes
3. **States the choice** so later work does not silently change direction

## Production Routes

- **Generate**: AI-created footage or imagery for cinematic scenes, characters, or B-roll
- **Compose**: deterministic motion graphics, typography, diagrams, captions, and explainers
- **Edit**: cutting, cleaning, reframing, captioning, or changing supplied footage
- **End-to-end**: a planned combination when multiple routes are essential to the final video

## How to Use

### Basic Usage

```text
Route this 60-second product explainer and state the primary production path.
```

### Advanced Usage

```text
Route this brief using the attached interview footage, a generated opener,
animated statistics, captions, and a final 16:9 export.
```

## Decision Guide

- “Explain,” “animate,” or “kinetic text” usually means **Compose**.
- “Create a cinematic scene” or “generate B-roll” usually means **Generate**.
- “Cut,” “trim,” “repurpose,” or “remove something from my clip” means **Edit**.
- Use **End-to-end** only when the finished deliverable genuinely depends on more than one route.
- Treat 16:9 as 1920×1080, 9:16 as 1080×1920, and 1:1 as 1080×1080 unless the brief specifies otherwise.

## Example

**User**: “Trim my interview, add a title card, animated statistics, and captions.”

**Output**:

```text
Route: End-to-end
Primary path: Edit, because the supplied interview is the core material.
Supporting path: Compose for the title card, statistics, and captions.
Canvas: 1920×1080 unless another aspect ratio is requested.
```

**Inspired by:** [OrkasVideoStudio's video-router skill](https://github.com/Orkas-AI/Orkas-VideoStudio/tree/main/packages/skills/video-router), MIT licensed.

## Tips

- Name the primary route in the plan before production starts.
- Do not silently switch routes when new information appears; explain the change.
- Keep planned media distinct from media that was actually produced.

## Common Use Cases

- Product explainers and launch videos
- Social clips made from existing footage
- Hybrid videos combining live footage and motion graphics
