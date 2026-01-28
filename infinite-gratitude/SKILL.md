---
name: infinite-gratitude
description: Multi-agent research skill that spawns 10 parallel Claude agents to conduct comprehensive research in 3 coordinated waves, reducing hours of research to minutes.
---

# Infinite Gratitude

A multi-agent research skill for Claude Code that transforms comprehensive research tasks from hours of manual work into minutes of automated, parallel processing. Uses 10 parallel agents organized in 3 research waves to gather, synthesize, and validate information.

## When to Use This Skill

- Conducting competitive analysis or market research
- Exploring new technologies or frameworks before adoption
- Gathering comprehensive information on complex topics
- Researching best practices across multiple domains
- Planning major projects that require extensive background research

## What This Skill Does

1. **Wave 1 - Parallel Discovery**: 10 agents independently research different aspects of your topic
2. **Wave 2 - Cross-Validation**: Agents verify and expand on each other's findings
3. **Wave 3 - Synthesis**: Consolidate all findings into actionable insights

## How to Use

### Basic Usage

```
Use infinite-gratitude to research [your topic]
```

### Advanced Usage

```
Use infinite-gratitude skill with focus on:
- Primary topic: [main subject]
- Specific angles: [list specific aspects to cover]
- Output format: [summary/detailed report/action items]
```

## Example

**User**: "Use infinite-gratitude to research pet AI recognition systems"

**Output**:
```
=== WAVE 1: Parallel Discovery (10 agents) ===
Agent 1: Competitor Analysis → Petnow (99% accuracy), industry leaders...
Agent 2: Dataset Survey → Oxford-IIIT Pet, Cat-faces-dataset...
Agent 3: Technical Approaches → ArcFace, MegaDescriptor, Siamese networks...
...

=== WAVE 2: Cross-Validation ===
Verified: Petnow uses Siamese + Self-Attention + 200K data
Expanded: Data quantity formula: 10K=85%, 50K=92%, 200K=99%
...

=== WAVE 3: Synthesis ===
Key Findings:
1. Nose print + facial features most reliable
2. ArcFace Loss > Triplet Loss for stability
3. Data quantity is the primary accuracy driver

Action Items:
- Expand dataset to 50K images
- Implement MegaDescriptor fine-tuning
- Add Self-Attention mechanism
```

**Real Case Study**: Pet AI research project reduced from 2+ days of manual research to comprehensive 9-report analysis in under 2 hours.

## Real-World Case Studies

### Case 1: Pet AI Recognition Research
- **Task**: Research state-of-the-art pet recognition AI
- **Result**: 9 comprehensive reports covering competitors, datasets, APIs, technical approaches
- **Time Saved**: ~16 hours → 2 hours

### Case 2: GitHub Promotion Campaign
- **Task**: Research effective GitHub star promotion strategies
- **Result**: Multi-platform strategy with community engagement tactics
- **Time Saved**: ~8 hours → 45 minutes

## Tips

- Start with a clear, specific research question
- Provide context about what you already know
- Specify the desired output format upfront
- Use for research phases, not implementation

## Requirements

- Claude Code CLI with multi-agent support
- API access for parallel agent spawning

## Repository

**GitHub**: [github.com/sstklen/infinite-gratitude](https://github.com/sstklen/infinite-gratitude)

**Inspired by:** The need for efficient, comprehensive research in AI development projects.
