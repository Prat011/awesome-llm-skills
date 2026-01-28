---
name: claude-api-cost-optimization
description: Teaches cost optimization strategies for Claude API that can reduce costs by 50-90% using Batch API, Prompt Caching, Extended Thinking, and model selection.
---

# Claude API Cost Optimization

A comprehensive skill for optimizing Claude API costs, providing strategies and techniques that can reduce API expenses by 50-90% without sacrificing output quality.

## When to Use This Skill

- Building production applications with Claude API
- Processing large volumes of requests
- Running batch analysis or data processing jobs
- Developing cost-sensitive AI features
- Optimizing existing Claude integrations

## What This Skill Does

1. **Batch API Optimization**: 50% cost reduction for non-time-sensitive tasks
2. **Prompt Caching**: 90% reduction on repeated context through cache hits
3. **Extended Thinking Optimization**: Strategic use of reasoning budgets
4. **Model Selection**: Right-sizing models for different task complexities

## How to Use

### Basic Usage

```
Apply claude-api-cost-optimization to my current API integration
```

### Advanced Usage

```
Analyze my API usage and suggest:
- Which requests should use Batch API
- Where to implement Prompt Caching
- Optimal model selection for each endpoint
- Extended Thinking budget recommendations
```

## Example

**User**: "Optimize my document processing pipeline that uses Claude API"

**Output**:
```
=== Cost Analysis ===
Current: $500/month (100K requests, Sonnet 4)

=== Optimization Recommendations ===

1. Batch API (50% savings)
   - Suitable tasks: Document classification, bulk summarization
   - Implementation: Queue requests, process in 24h batches
   - Savings: $150/month

2. Prompt Caching (90% on cache hits)
   - Cacheable: System prompts, document templates, few-shot examples
   - Cache prefix: 2,048+ tokens recommended
   - Expected hit rate: 70%
   - Savings: $180/month

3. Model Selection
   - Haiku for: Simple classification, extraction
   - Sonnet for: Standard analysis, generation
   - Opus for: Complex reasoning only
   - Savings: $80/month

=== Projected Monthly Cost ===
Before: $500/month
After: $90/month
Total Savings: 82%
```

## Key Strategies

### 1. Batch API (50% Cost Reduction)
```python
# Queue non-urgent requests for batch processing
batch_request = {
    "custom_id": "doc-001",
    "params": {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": "..."}]
    }
}
# Results available within 24 hours at half price
```

### 2. Prompt Caching (Up to 90% Reduction)
```python
# Mark static content for caching
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": large_document,  # 2,048+ tokens
                "cache_control": {"type": "ephemeral"}
            },
            {"type": "text", "text": user_query}
        ]
    }
]
# Subsequent requests with same prefix: 90% cheaper
```

### 3. Extended Thinking Optimization
```python
# Set appropriate thinking budgets
thinking_budget = {
    "simple_tasks": 1024,    # Classification, extraction
    "medium_tasks": 4096,    # Analysis, summarization  
    "complex_tasks": 16000,  # Multi-step reasoning
}
# Avoid over-allocating thinking tokens
```

### 4. Model Selection Guide
| Task Complexity | Model | Cost/1M tokens |
|----------------|-------|----------------|
| Simple | Haiku | $0.25 |
| Standard | Sonnet | $3.00 |
| Complex | Opus | $15.00 |

## Tips

- Audit your current usage before optimizing
- Start with Batch API for the quickest wins
- Implement Prompt Caching for repetitive contexts
- Monitor cache hit rates and adjust prefix lengths
- Use model tiering based on task complexity

## Common Use Cases

- Document processing pipelines
- Chatbot and assistant applications
- Data analysis and extraction
- Content generation at scale
- Research and summarization tasks

## Repository

**GitHub**: [github.com/sstklen/claude-api-cost-optimization](https://github.com/sstklen/claude-api-cost-optimization)

**Inspired by:** Real-world production deployments requiring cost-effective AI integration.
