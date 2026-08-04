---
name: chatbot-designer
description: Design chatbots, conversational agents, and AI assistants for business, customer support, or internal use cases.
---

# Chatbot Designer

Design effective conversational agents for business, customer support, internal analytics, enablement, and operational workflows. Use this skill to turn a rough chatbot idea into a clear product brief, use-case map, conversation flow, example dialogues, and data/integration plan.

## When to Use This Skill

- Designing a new chatbot, AI assistant, or conversational agent.
- Improving an existing assistant that has unclear scope, weak fallback handling, or scattered user intents.
- Mapping business workflows into simple chatbot conversations.
- Planning the data sources, rules, and AI reasoning layer for an assistant.
- Preparing a practical bot design document for stakeholders, developers, or operations teams.

## What This Skill Does

1. **Defines the bot purpose**: Clarifies the problem, target users, value proposition, and success criteria.
2. **Maps use cases**: Identifies the top user intents and the workflows the bot must support.
3. **Designs conversation flow**: Creates entry prompts, decision paths, clarifying questions, handoff points, and fallback handling.
4. **Plans intelligence**: Separates deterministic rules, data retrieval, integrations, and AI reasoning.
5. **Shapes outputs**: Chooses tone, answer structure, response length, and guidance style.

## Instructions

When invoked, produce a practical chatbot design using this framework.

### Step 1 - Define Purpose

Clarify:

- What problem the bot solves.
- Who the target users are.
- What the bot should and should not do.
- What a successful interaction looks like.

If the user has not provided enough context, make reasonable assumptions and label them as assumptions.

### Step 2 - Use Case Mapping

Identify the top 5 user intents. For each intent, include:

- User goal.
- Trigger phrase examples.
- Required data or system capability.
- Recommended workflow type: Q&A, recommendation, troubleshooting, task execution, escalation, or guided decision.

### Step 3 - Conversation Design

Design:

- Entry prompts.
- Decision tree or routing logic.
- Clarifying questions.
- Fallback handling.
- Escalation or human handoff rules.
- Memory or feedback behavior, if relevant.

Keep flows short. Prefer one or two clarifying questions over long forms.

### Step 4 - Intelligence Layer

Specify:

- Data sources such as Excel, databases, APIs, SharePoint, CRM, knowledge bases, or uploaded files.
- Which behaviors should be rules-based.
- Which behaviors can use AI reasoning.
- Guardrails to avoid hallucination, privacy issues, or unsafe actions.
- Feedback capture and review loop if the bot should improve over time.

### Step 5 - Output Design

Define:

- Tone: professional, friendly, concise, advisory, or support-oriented.
- Format: short answer, guided steps, table, recommendation, checklist, or escalation note.
- Source notes or confidence language.
- What the bot should do when data is missing.

## Output Format

Use this exact structure unless the user requests a different format:

1. **Bot Overview**
2. **Use Cases**
   - Provide a table with columns: Intent, User Need, Workflow, Data Needed, Success Response.
3. **Conversation Flow**
   - Include entry prompts, routing, clarifying questions, fallback, and handoff.
4. **Example Dialogues**
   - Provide 2-3 realistic examples.
5. **Data + Integration Plan**
   - List sources, rules vs AI reasoning, logging/feedback, and implementation notes.

## How to Use

### Basic Usage

```text
Use the chatbot-designer skill to design a customer support chatbot for an ecommerce store.
```

### Business Assistant Usage

```text
Use the chatbot-designer skill to design an internal sales dashboard assistant that answers metric questions, explains trends, and records user feedback.
```

### Improvement Usage

```text
Use the chatbot-designer skill to improve this existing assistant. Focus on fallback handling, top intents, and feedback learning loop.
```

## Example

**User**: "Design a chatbot for an internal dashboard that answers sales questions and learns from feedback."

**Output**:

```markdown
1. Bot Overview
The assistant helps business users ask natural-language questions about sales, traffic, targets, and performance drivers. It should answer from approved data only and record feedback for review.

2. Use Cases
| Intent | User Need | Workflow | Data Needed | Success Response |
|---|---|---|---|---|
| Metric Q&A | Understand current performance | Q&A | Sales and traffic tables | Short answer with value, trend, and source |
| Ranking | Find top/bottom drivers | Recommendation | Category/brand data | Ranked list with metric basis |
| Target tracking | Check progress | Q&A | Target file and actuals | Hit rate and gap to target |
| Troubleshooting | Explain missing answer | Troubleshooting | Load status and schema | Clear reason and next step |
| Feedback | Improve future answers | Feedback loop | Q&A log | Captured approve/disapprove signal |

3. Conversation Flow
Entry prompts: "Ask about GMV, traffic, target, or category trend." Route by intent, metric, and scope. If scope is ambiguous, ask one clarifying question. If data is missing, say what is missing and avoid guessing.

4. Example Dialogues
User: "What is Baby traffic trend?"
Bot: "Baby traffic is up versus the first loaded date. Source: traffic rows for the selected period."

User: "Why no SKU inbound split?"
Bot: "Inbound/outbound data is only reliable at category and brand level, so I cannot split SKU safely."

5. Data + Integration Plan
Use Excel actuals, target files, and approved source tables. Keep calculations rules-based. Use AI reasoning only for wording and intent detection. Store feedback for weekly human review before changing business rules.
```

## Tips

- Keep conversations simple and fast.
- Design for the user's most common decisions, not every possible edge case.
- Prefer short answers with clear source notes.
- Use clarifying questions only when they materially improve the answer.
- Separate rules-based facts from AI-generated interpretation.
- Do not let feedback automatically rewrite business logic; use a human approval loop.
- Build fallback paths for missing data, ambiguous scope, unsupported requests, and low confidence.

## Common Use Cases

- Internal analytics assistants.
- Customer support bots.
- Sales enablement assistants.
- Operations troubleshooting bots.
- HR or IT helpdesk assistants.
- Knowledge-base Q&A agents.
- AI assistants embedded in dashboards.

**Inspired by:** Practical chatbot design workflows for internal business assistants and dashboard Q&A agents.
