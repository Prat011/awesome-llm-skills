---
name: notion-research-documentation
description: Searches across your Notion workspace, synthesizes findings from multiple pages, and creates comprehensive research documentation saved as new Notion pages. Turns scattered information into structured reports with proper citations and actionable insights.
---

# Research & Documentation

Enables comprehensive research workflows: search for information across your Notion workspace, fetch and analyze relevant pages, synthesize findings, and create well-structured documentation.

## Quick Start

When asked to research and document a topic:

1. **Search for relevant content**: Use `Notion:notion-search` to find pages
2. **Fetch detailed information**: Use `Notion:notion-fetch` to read full page content
3. **Synthesize findings**: Analyze and combine information from multiple sources
4. **Create structured output**: Use `Notion:notion-create-pages` to write documentation

## Research Workflow

### Step 1: Search for relevant information

```
Use Notion:notion-search with the research topic
Filter by teamspace if scope is known
Review search results to identify most relevant pages
```

### Step 2: Fetch page content

```
Use Notion:notion-fetch for each relevant page URL
Collect content from all relevant sources
Note key findings, quotes, and data points
```

### Step 3: Synthesize findings

Analyze the collected information:
- Identify key themes and patterns
- Connect related concepts across sources
- Note gaps or conflicting information
- Organize findings logically

### Step 4: Create structured documentation

Use the appropriate documentation template (see [reference/format-selection-guide.md](reference/format-selection-guide.md)) to structure output:
- Clear title and executive summary
- Well-organized sections with headings
- Citations linking back to source pages
- Actionable conclusions or next steps

## Output Formats

Choose the appropriate format based on request:

**Research Summary**: See [reference/research-summary-format.md](reference/research-summary-format.md)
**Comprehensive Report**: See [reference/comprehensive-report-format.md](reference/comprehensive-report-format.md)
**Quick Brief**: See [reference/quick-brief-format.md](reference/quick-brief-format.md)

## Best Practices

1. **Cast a wide net first**: Start with broad searches, then narrow down
2. **Cite sources**: Always link back to source pages using mentions
3. **Verify recency**: Check page last-edited dates for current information
4. **Cross-reference**: Validate findings across multiple sources
5. **Structure clearly**: Use headings, bullets, and formatting for readability

## Page Placement

By default, create research documents as standalone pages. If the user specifies:
- A parent page → use `page_id` parent
- A database → fetch the database first, then use appropriate `data_source_id`
- A teamspace → create in that context

## Advanced Features

**Search filtering**: See [reference/advanced-search.md](reference/advanced-search.md)
**Citation styles**: See [reference/citations.md](reference/citations.md)

## Common Issues

**"No results found"**: Try broader search terms or different teamspaces
**"Too many results"**: Add filters or search within specific pages
**"Can't access page"**: User may lack permissions, ask them to verify access

## Examples

See [examples/](examples/) for complete workflow demonstrations:
- [examples/market-research.md](examples/market-research.md) - Researching market trends
- [examples/technical-investigation.md](examples/technical-investigation.md) - Technical deep-dive
- [examples/competitor-analysis.md](examples/competitor-analysis.md) - Multi-source synthesis

