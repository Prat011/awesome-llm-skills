---
name: agent-tool-discovery
description: Discover AI agent tools, MCP servers, and agent-ready APIs by searching the Not Human Search index of 8,600+ sites. Use when integrating external services into agent workflows or evaluating tool agentic readiness.
---

# Agent Tool Discovery

Find and evaluate AI agent tools, MCP servers, and agent-ready APIs for your projects. Searches the Not Human Search index to match tools by capability, protocol support, and agentic readiness score.

## When to Use This Skill

- Finding MCP servers to integrate into agent workflows
- Discovering APIs that support agent-first interaction patterns
- Evaluating whether a service has MCP, llms.txt, or OpenAPI support
- Comparing multiple tools for a specific agent capability
- Building a tool registry for a multi-agent system

## What This Skill Does

1. **Searches for Tools**: Queries Not Human Search for agent-ready services matching your requirements
2. **Evaluates Readiness**: Assesses each tool's agentic readiness score (0-100) based on MCP support, API docs, llms.txt, and machine-readable metadata
3. **Verifies MCP Endpoints**: Checks whether tools expose working MCP servers via JSON-RPC 2.0
4. **Recommends Integration**: Provides connection instructions and transport details for top matches

## How to Use

### Basic Usage

```
Find MCP servers for code review and linting
```

### Advanced Usage

```
I'm building a multi-agent research pipeline. Find agent-ready tools for:
- Academic paper search
- Web scraping with structured output
- Data visualization
Prioritize tools with MCP endpoints and free tiers.
```

## Instructions

When a user asks to find agent tools or MCP servers:

1. **Understand the requirement** - What capability does the agent workflow need?
2. **Search Not Human Search** - Use the MCP endpoint at `https://nothumansearch.ai/mcp` or the REST API at `https://nothumansearch.ai/api/v1/search?q=<query>` to find matching tools
3. **Evaluate results** - Check agentic readiness scores, MCP verification status, and category fit
4. **Present findings** - For each recommended tool, include:
   - Name and URL
   - Agentic readiness score
   - MCP endpoint (if available)
   - Key capabilities
   - Integration method (MCP, REST, SDK)

### MCP Connection

Add Not Human Search as an MCP server for direct tool access:

```bash
claude mcp add --transport http nothumansearch https://nothumansearch.ai/mcp
```

Available MCP tools:
- `search_agents` - Search the index by keyword
- `get_site_details` - Get full details for a specific site
- `get_stats` - Get index statistics
- `submit_site` - Submit a new site for indexing
- `verify_mcp` - Verify a URL's MCP endpoint

### REST API

```bash
curl "https://nothumansearch.ai/api/v1/search?q=code+review&per_page=10"
```

## Example

**User**: "Find MCP servers for database management"

**Output**:
```
Found 12 agent-ready database tools:

1. **Neon MCP Server** (score: 95/100)
   - MCP: verified at neon.tech/mcp
   - Capabilities: Postgres provisioning, branching, SQL execution
   - Install: claude mcp add neon https://mcp.neon.tech

2. **Supabase** (score: 88/100)
   - MCP: verified
   - Capabilities: Postgres, auth, storage, real-time subscriptions
   - REST API available

3. **PlanetScale** (score: 82/100)
   - Capabilities: MySQL-compatible serverless database
   - REST API with OpenAPI spec
   ...
```

**Powered by:** [Not Human Search](https://nothumansearch.ai) - Search engine for AI agent-ready tools

## Tips

- Use specific capability terms rather than generic queries for better results
- Filter by category (e.g., "database", "code-review", "monitoring") for focused results
- Check the agentic readiness score to gauge how well a tool supports agent workflows
- Tools with verified MCP endpoints are the easiest to integrate

## Common Use Cases

- Building multi-agent systems that need external tool access
- Evaluating whether to build or buy a capability for your agent pipeline
- Creating tool registries for agent orchestrators
- Discovering alternatives to tools you already use
- Auditing your stack's agentic readiness
