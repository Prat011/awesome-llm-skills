---
name: ru-text
description: Use when writing, editing, or reviewing Russian-language text. Covers typography, info-style, editorial, UX writing, business correspondence. Auto-activates on Russian text output.
---

# ru-text

Russian text quality plugin with ~1,040 independently formulated rules across 7 domains. Works with Claude Code, Codex CLI, Gemini CLI, Cursor, and 43 other agents via `npx skills add talkstream/ru-text`.

## When to Use This Skill

- Writing or editing any Russian-language text
- Reviewing Russian content for typography, style, and grammar issues
- Creating UI microcopy, business emails, or articles in Russian
- Scoring Russian text quality on a 0–10 scale

## What This Skill Does

1. **Typography**: Applies 96 rules for Russian typographic conventions — guillemets, em dashes, non-breaking spaces, digit grouping, special characters
2. **Information Style**: Flags 97 stop-words, bureaucratic language, passive voice, and vague claims using principles informed by Russian editorial standards
3. **Grammar & Punctuation**: Checks 259 rules for agreement, capitalization, 57 comma-trap constructions, tautology, and pleonasm
4. **UX Writing**: Provides 217 patterns for buttons, error messages, empty states, forms, and notifications in Russian
5. **Business Writing**: Structures emails, messenger etiquette, tone management, and 43 clean phrase patterns
6. **Text Scoring**: Evaluates text on a 0.0–10.0 scale across 5 dimensions (typography, clarity, grammar, structure, reader precision)

## How to Use

### Basic Usage

```
Write a product description for a SaaS tool in Russian
```

The skill auto-activates and applies typography rules (guillemets, em dashes, NBSP), flags stop-words, and ensures reader-first structure.

### Advanced Usage

```
/ru-text:ru-score

Наша компания осуществляет деятельность в сфере предоставления
высококачественных услуг по обеспечению информационной безопасности.
```

Returns a 0–10 score with per-dimension breakdown and specific issues.

## Example

**User**: "Write a short 'About us' section for an IT company in Russian"

**Output**:
```
Мы защищаем данные 200 компаний в России и СНГ. За 2024 год предотвратили
1 400 инцидентов и сократили время реагирования клиентов с 4 часов до 12 минут.

Три направления: аудит инфраструктуры, мониторинг угроз и обучение сотрудников.
```

Notice: guillemets for quotes, em dashes where needed, specific numbers instead of "leading provider of innovative solutions", no bureaucratic language.

## Tips

- Your explicit style request always overrides default rules (casual, academic, SEO, literary)
- The skill loads domain-specific references on demand — only what your task needs
- Use `/ru-text:ru-score` to get a quantitative quality assessment before publishing
- A score of 7–8 is good for working texts; 9+ is rare and aspirational

## Common Use Cases

- Product landing pages and marketing copy in Russian
- README and documentation for Russian-language projects
- Business emails and messenger communication
- UI buttons, error messages, empty states, and tooltips
- Blog posts, articles, and editorial content
- AI agent responses in Russian (quality assurance)
