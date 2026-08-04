---
name: edu-role-play
description: Create interactive AI role-play training activities as self-contained HTML. Use when the user asks to generate a role-play, persona practice, sales simulation, customer conversation drill, compliance scenario, or any learner-vs-AI-character training exercise.
allowed-tools: Read Write Edit Bash(edu-role-play *) Bash(node *) Bash(npx *)
---

# edu-role-play

Generate a single HTML file that learners open to practice a conversation with an AI persona. The runtime drives the chat, detects when objectives are met, and scores the transcript against a rubric at the end. You author the composition; the CLI lints and bundles it.

## 1. Approach

When the user asks for a role-play, your job is to produce a composition HTML that exercises a specific, observable skill. Do not start writing XML until the user has told you (or you have inferred and confirmed) all five pieces of the Pedagogical DNA. If any piece is missing or vague, ask one concise clarifying question at a time.

The shape of every composition:

- One **persona** with goals, constraints, and speech patterns
- One **scenario** that places the learner in role
- 2–4 **observable objectives**
- A **rubric** that scores each objective with a positive-integer weight (sum 1–20)
- **Termination** conditions (always a turn cap; manual-end by default)

## 2. Pedagogical DNA Gate (hard requirement)

Before generating any composition, confirm all five:

1. **Learner role** — who is practicing, and what skill are they building?
2. **Observable objectives** — what concrete actions should the learner take? (If the user says "understand X" or "be aware of Y", push for an observable verb: ask, confirm, quantify, secure, surface, handle.)
3. **Success criteria** — what does a good answer on each objective look like?
4. **Rubric dimensions** — how is each objective weighted relative to the others?
5. **Persona goals + constraints** — what does the AI character want and what can't they budge on?

If the user is vague, ask the smallest next question. Do not invent content that changes the pedagogical intent.

## 2.5. Plan confirmation (before generating)

Once you have all five pieces of the Pedagogical DNA, **do not start writing XML yet**. First, summarize the plan back to the user in 4–6 short lines and ask for explicit approval. Use this exact shape:

```
Plan:
- Conversation: <one line on what the role-play is about>
- Learner role: <who the user is practicing as>
- Persona: <name + role of the AI character they'll talk to>
- Objectives: <comma-separated short list>
- Difficulty / tone: <if known>
- Language: <code from §3.5, inferred from how the user is talking to you>

Want me to generate this, or change anything first?
```

Only proceed to generate the composition HTML after the user confirms ("yes", "go", "looks good", etc.). If they request changes, update the plan, re-print it, and ask again. Do not skip this step even when the DNA was provided up-front in a single message — confirmation is the gate.

## 2.6. Persona avatar

Set an `avatar` attribute on `<edu-persona>` from this fixed list. The CLI inlines the matching portrait into the bundled HTML at build time. Pick the closest match — do not invent new IDs.

- `middle-aged-man-friendly` — approachable, salt-and-pepper, business casual
- `middle-aged-man-frustrated` — serious / tense expression, good for upset customers or hard stakeholders
- `middle-aged-woman-professional` — confident, business attire
- `young-woman-professional` — late-20s, polished
- `young-man-thoughtful` — late-20s, neutral / considered expression
- `older-woman-warm` — 60s+, warm and smiling

Choose primarily on demographic fit (age, gender), then tone match. If none fit, omit the attribute and the runtime falls back to a generic silhouette.

## 3. Composition structure

Wrap the composition in the standard HTML shell below. The `<style>` block and the "not bundled yet" `<div data-erp-fallback>` are **required** — they turn the raw source into a self-explaining page when a user opens it directly in a browser. The runtime wipes the `<edu-role-play>` contents on mount, so these have no effect on the bundled output.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>my-roleplay</title>
    <style>
      edu-role-play > :not([data-erp-fallback]) { display: none; }
      [data-erp-fallback].notice { display: block; font-family: system-ui, sans-serif; max-width: 560px; margin: 60px auto; padding: 24px; border: 1px solid #e5e7eb; border-radius: 10px; background: #fafafa; line-height: 1.5; }
      [data-erp-fallback] h2 { margin: 0 0 8px 0; font-size: 18px; }
      [data-erp-fallback] pre { background: #fff; border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px 12px; font-family: ui-monospace, monospace; font-size: 13px; }
    </style>
  </head>
  <body>
<edu-role-play id="my-roleplay" runtime-version="0.1.0" locale="en">
  <div class="notice" data-erp-fallback>
    <h2>This role-play isn't bundled yet</h2>
    <p>Open a terminal in this folder and run:</p>
    <pre><code>npx edu-role-play start my-roleplay.erp</code></pre>
  </div>
  <edu-persona name="Sarah Chen" role="VP of Operations">
    <background>15 years in logistics. Burned by a CRM migration in 2023.</background>
    <goals>Cut vendor count by 30% before Q4 board review.</goals>
    <constraints>Budget locked until Q3. Won't sign without a peer reference.</constraints>
    <speech-patterns>Direct. Asks for specifics. Interrupts vague claims.</speech-patterns>
  </edu-persona>

  <edu-scenario>
    You are an account executive pitching Acme CRM to Sarah. You have 15 minutes to
    uncover a pain point, quantify its impact, and secure a follow-up meeting.
  </edu-scenario>

  <edu-objective id="discover-pain">Surface at least one current operational pain point Sarah owns.</edu-objective>
  <edu-objective id="quantify-impact">Get Sarah to share a number (dollars, hours, or headcount).</edu-objective>
  <edu-objective id="book-followup">Secure a concrete follow-up meeting (date + attendees).</edu-objective>

  <edu-rubric>
    <criterion objective="discover-pain" weight="3">Full credit: pain is specific, Sarah-owned, and tied to a process.</criterion>
    <criterion objective="quantify-impact" weight="4">Full credit: Sarah volunteers a dollar / hour / headcount number.</criterion>
    <criterion objective="book-followup" weight="3">Full credit: follow-up has a date, owner, and named attendees.</criterion>
  </edu-rubric>

  <edu-termination>
    <turn-limit>20</turn-limit>
    <objective-check-every>1</objective-check-every>
    <manual-end>true</manual-end>
  </edu-termination>
</edu-role-play>
  </body>
</html>
```

## 3.5. Language / locale (mandatory)

Set `locale="<code>"` on the root `<edu-role-play>` element to match the language the user is authoring in. This drives the UI chrome (briefing, objectives heading, buttons, debrief modal, system notes) — the persona, scenario, and objectives stay in whatever language you wrote them.

**Detection rule:** pick the locale from the language the user is speaking to you in this session. If they switched to Turkish to request the role-play, set `locale="tr"` even if your reply is in English. When in doubt, ask once: "Should the activity UI be in Turkish or English?"

Supported codes: `en`, `es`, `fr`, `de`, `pt`, `it`, `tr`, `ja`, `zh`, `ar`. Anything else falls back to `en`.

When you write the persona / scenario / objectives in a non-English language, the `locale` attribute MUST match — otherwise the learner sees Turkish content under English headings, which looks broken.

## 4. Persona design

See [persona-design.md](persona-design.md). Rules:
- `name` + `role` must be concrete (no "a salesperson").
- `<goals>` state what the persona wants from THIS conversation.
- `<constraints>` are hard limits. They make pushback believable.
- `<speech-patterns>` shape voice. Be specific ("interrupts vague claims") not generic ("assertive").

## 5. Objectives and rubric

See [objective-patterns.md](objective-patterns.md) and [rubric-design.md](rubric-design.md). Rules:
- Every objective is observable in the transcript. Forbidden verbs: *understand, know, feel, appreciate, be aware, familiarize, learn about*.
- Every objective has exactly one matching `<criterion>`.
- Weights are positive integers; the sum must be in [1, 20].
- Criterion text spells out what full credit looks like.

## 6. Termination

Always include `<turn-limit>` (default 20) or `<time-limit>` in seconds. `<manual-end>true</manual-end>` lets the learner stop and get scored. `<objective-check-every>` (default 1) controls how often the runtime checks whether all objectives are met. Set higher to reduce LLM calls at the cost of laggier checklist updates.

## 7. Non-negotiable rules (linter-enforced)

1. Every `<edu-objective>` must be observable — no vague verbs.
2. The rubric must cover every objective id and contain no orphan criteria.
3. Persona must have non-empty `<goals>` and `<constraints>`.
4. Termination must include at least one hard cap (turn-limit or time-limit).
5. The scenario must mention the persona by name and address the learner in the second person.
6. Rubric weights must be positive integers summing to [1, 20].

Failing any of these blocks `bundle`.

## 8. Output checklist

Each role-play gets its own folder so files don't pile up in the user's working directory.

1. Pick a short kebab-case slug (e.g. `gdpr-sar-audit`). Create the folder: the composition source file path is `<slug>/<slug>.erp`. The `.erp` extension (not `.html`) is intentional — it keeps editor / Claude Code app HTML previews from auto-opening the unbundled source. The bundled artifact users actually open is `<slug>/<slug>.html`.
2. Write the composition to `<slug>/<slug>.erp`.
3. **You** (the agent) run `npx -y edu-role-play lint <slug>/<slug>.erp`. Fix every error. Warnings (e.g. stale `runtime-version`) can stay but prefer to fix.
4. **You** (the agent) run `npx -y edu-role-play bundle <slug>/<slug>.erp` to produce the playable `<slug>/<slug>.html`. Do not ask the user for an API key — bundling never needs one (keys live on the proxy, not in the HTML). If the environment cannot run `npx` (no shell, no network), fall back to instructing the user to run it themselves and skip section (a) below.
5. Your final message after the first bundle MUST be light and bulleted — no walls of text, no technical detail about proxies, secrets, or runtime internals. Use this exact shape:

   > Bundled. Run `npx edu-role-play start <slug>/<slug>.html` to try it.
   >
   > - Tell me what to change if anything feels off (persona, objectives, rubric, scenario).
   > - When it's good, say the word and I'll set you up with your own API key + a SCORM zip you can upload to your LMS.

   That's it. Do not mention the shared proxy, rate limits, Cloudflare, Workers, secrets, or SCORM mechanics in this first message.

   **When the user says they're happy / ready to ship**, then (and only then) walk them through the deploy + SCORM step in one go.

   **Track A — terminal host (Claude Code, Cursor, Codex, anywhere with `Bash` + `npx`).** Say only:
   > Running `npx edu-role-play deploy-proxy` to wire in your own API key, then I'll package the SCORM zip.

   Do not explain what `deploy-proxy` does, what wrangler is, what a Worker secret is, or which env vars get set — the CLI itself prompts the user through it. Then run `deploy-proxy` for them. Once it returns a Worker URL, immediately:
   1. Re-bundle with `--proxy-url https://<their-worker>.workers.dev`.
   2. Run `npx -y edu-role-play scorm <slug>/<slug>.erp --proxy-url https://<their-worker>.workers.dev`.
   3. Report back in one short message:
      > Done. Your own key is wired up, and `<slug>/<slug>.scorm.zip` is ready to upload to your LMS (Moodle, Canvas, TalentLMS, SCORM Cloud, etc.).

   **Track B — web host (claude.ai, or any environment without a shell).** Give the user a short numbered list, no extra commentary:
   > 1. Click **Deploy to Cloudflare**: <https://deploy.workers.cloudflare.com/?url=https://github.com/minicoursegenerator/edu-role-play-proxy>, then copy the `https://<name>.workers.dev` URL it gives you.
   > 2. In the Cloudflare dashboard → that Worker → **Settings → Variables and Secrets** → add `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`) as a **Secret**.
   > 3. Paste the Worker URL back to me.

   When they paste the URL back, edit the bundled HTML to add `<meta name="edu-role-play-proxy" content="https://<their-worker>.workers.dev">` in `<head>`, then tell them how to get the SCORM zip — either by running `npx -y edu-role-play scorm <slug>/<slug>.erp --proxy-url <url>` themselves, or (if they have no shell at all) point them at the CLI docs.

   **Track detection.** Default to Track A if `Bash` and `npx` are available; otherwise Track B. If unsure, ask: "Are you on the web (claude.ai) or in a terminal-capable environment?"

   **Optional polish — Cloudflare MCP connected.** If a Cloudflare Developer Platform MCP connector is available, after the user reports the deploy is done you may use it to confirm the Worker exists and read its URL so the user doesn't have to copy-paste. Do not use the MCP to deploy Workers or set secrets — both stay user-driven via the Cloudflare UI.

   **Credential boundary (non-negotiable).** Do not enter the user's Cloudflare login or API key on their behalf. Direct them to Cloudflare's own UI — the OAuth deploy button and the dashboard secret form. Every hop a secret takes is a hop where it can leak; the dashboard is where the human should type it.

Only suggest `--proxy-url <…>` if the user *explicitly* asks to point at a different Worker. There is no option to bake an API key into the HTML — keys never ship in source.

## 9. On-demand references

Load only when needed:

- [archetypes.md](archetypes.md) — the 5 v1 archetypes and when to pick each
- [persona-design.md](persona-design.md) — writing strong personas
- [rubric-design.md](rubric-design.md) — observable rubrics and weights
- [objective-patterns.md](objective-patterns.md) — objective phrasing patterns
- [cli-reference.md](cli-reference.md) — `edu-role-play` CLI flags
- [../../docs/scorm.md](../../docs/scorm.md) — what the SCORM 1.2 runtime reports to the LMS (cmi.* fields, suspend_data shape, limitations)

## Privacy note to surface to the user

Transcripts are not stored. The bundled artifact runs entirely in the learner's browser; inference requests are routed through the project's Cloudflare Worker proxy (`POST /v1/chat`), which calls the configured provider via Worker-side secrets — no API keys live in the HTML.
