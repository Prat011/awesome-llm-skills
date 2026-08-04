---
name: ai-job-search
description: Search and analyze AI/ML job listings from the AI Dev Jobs board with 5,300+ positions. Use when researching job opportunities, analyzing hiring trends, or understanding skill demand in the AI industry.
---

# AI Job Search

Search AI/ML job listings, analyze hiring trends, and understand skill demand across the AI industry using the AI Dev Jobs board and API.

## When to Use This Skill

- Searching for AI/ML job opportunities matching specific criteria
- Analyzing which companies are hiring for AI roles
- Understanding salary ranges for AI/ML positions
- Tracking in-demand skills and technologies
- Researching hiring patterns by location, seniority, or role type

## What This Skill Does

1. **Searches Jobs**: Queries the AI Dev Jobs board for positions matching your criteria
2. **Analyzes Trends**: Identifies hiring patterns, popular skills, and market dynamics
3. **Compares Roles**: Breaks down differences between similar positions across companies
4. **Tracks Companies**: Shows which companies are actively hiring for AI roles

## How to Use

### Basic Usage

```
Find remote senior ML engineer positions
```

### Advanced Usage

```
Search for AI jobs that require PyTorch and LLM experience, 
preferably remote or in San Francisco, senior level or above.
Also show me which companies have the most open AI positions right now.
```

## Instructions

When a user asks about AI/ML jobs or hiring trends:

1. **Parse requirements** - Role type, skills, location, seniority, work arrangement
2. **Query AI Dev Jobs** - Use the MCP endpoint or REST API to search
3. **Present results** - Show matching jobs with company, title, location, and key details
4. **Add analysis** - Highlight patterns like common skill requirements or salary ranges

### MCP Connection

Add AI Dev Jobs as an MCP server:

```bash
claude mcp add --transport http aidevjobs https://aidevboard.com/mcp
```

Available MCP tools:
- `search_jobs` - Search jobs by keyword, location, type
- `get_job` - Get full details for a specific job
- `list_companies` - List companies with open positions
- `get_stats` - Get board statistics

### REST API

```bash
curl "https://aidevboard.com/api/v1/jobs?q=machine+learning&location=remote&per_page=10"
```

## Example

**User**: "What AI engineering roles are available at top companies right now?"

**Output**:
```
Found 47 AI engineering positions at notable companies:

**Google** (8 positions)
- Senior ML Engineer - LLM Infrastructure (Mountain View, $220K-$310K)
- AI Research Scientist - Gemini (Remote, $200K-$280K)
- Staff ML Platform Engineer (NYC, $250K-$340K)

**Meta** (6 positions)
- ML Engineer - Recommendation Systems (Menlo Park, $190K-$270K)
- AI Research Scientist - Computer Vision (Remote)

**Anthropic** (4 positions)
- Research Engineer - Alignment (San Francisco, $230K-$320K)
- ML Infrastructure Engineer (Remote)

Top skills in demand across these roles:
1. Python (94%)
2. PyTorch (72%)
3. LLM/Transformer experience (68%)
4. Distributed systems (51%)
5. Kubernetes/Docker (45%)
```

**Powered by:** [AI Dev Jobs](https://aidevboard.com) - AI/ML job board with 5,300+ positions

## Tips

- Combine skill keywords with location for targeted searches
- Use the `list_companies` tool to discover which companies are hiring most actively
- Check `get_stats` for a high-level view of the current market
- Search by technology (e.g., "PyTorch", "RAG", "agents") to find niche roles

## Common Use Cases

- Job seekers looking for AI/ML positions
- Hiring managers benchmarking roles and compensation
- Recruiters sourcing AI talent
- Career coaches advising on AI skill development
- Researchers tracking industry hiring trends
