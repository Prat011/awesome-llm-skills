---
name: notion-meeting-intelligence
description: Prepares meeting materials by gathering context from Notion, enriching with Claude research, and creating both an internal pre-read and external agenda saved to Notion. Helps you arrive prepared with comprehensive background and structured meeting docs.
---

# Meeting Intelligence

Prepares you for meetings by gathering context from Notion, enriching it with Claude research, and creating comprehensive meeting materials. Generates both an internal pre-read for attendees and an external-facing agenda for the meeting itself.

## Quick Start

When asked to prep for a meeting:

1. **Gather Notion context**: Use `Notion:notion-search` to find related pages
2. **Fetch details**: Use `Notion:notion-fetch` to read relevant content
3. **Enrich with research**: Use Claude's knowledge to add context, industry insights, or best practices
4. **Create internal pre-read**: Use `Notion:notion-create-pages` for background context document (for attendees)
5. **Create external agenda**: Use `Notion:notion-create-pages` for meeting agenda (shared with all participants)
6. **Link resources**: Connect both docs to related projects and each other

## Meeting Prep Workflow

### Step 1: Understand meeting context

```
Collect meeting details:
- Meeting topic/title
- Attendees (internal team + external participants)
- Meeting purpose (decision, brainstorm, status update, customer demo, etc.)
- Meeting type (internal only vs. external participants)
- Related project/initiative
- Specific topics to cover
```

### Step 2: Search for Notion context

```
Use Notion:notion-search to find:
- Project pages related to meeting topic
- Previous meeting notes
- Specifications or design docs
- Related tasks or issues
- Recent updates or reports
- Customer/partner information (if applicable)

Search strategies:
- Topic-based: "mobile app redesign"
- Project-scoped: search within project teamspace
- Attendee-created: filter by created_by_user_ids
- Recent updates: use created_date_range filters
```

### Step 3: Fetch and analyze Notion content

```
For each relevant page:
1. Fetch with Notion:notion-fetch
2. Extract key information:
   - Project status and timeline
   - Recent decisions and updates
   - Open questions or blockers
   - Relevant metrics or data
   - Action items from previous meetings
3. Note gaps in information
```

### Step 4: Enrich with Claude research

```
Beyond Notion context, add value through:

For technical meetings:
- Explain complex concepts for broader audience
- Summarize industry best practices
- Provide competitive context
- Suggest discussion frameworks

For customer meetings:
- Research company background (if public info)
- Industry trends relevant to discussion
- Common pain points in their sector
- Best practices for similar customers

For decision meetings:
- Decision-making frameworks
- Risk analysis patterns
- Trade-off considerations
- Implementation best practices

Note: Use general knowledge only - don't fabricate specific facts
```

### Step 5: Create internal pre-read

```
Use Notion:notion-create-pages for internal doc:

Title: "[Meeting Topic] - Pre-Read (Internal)"

Content structure:
- **Meeting Overview**: Date, time, attendees, purpose
- **Background Context**: 
  - What this meeting is about (2-3 sentences)
  - Why it matters (business context)
  - Links to related Notion pages
- **Current Status**: 
  - Where we are now (from Notion content)
  - Recent updates and progress
  - Key metrics or data
- **Context & Insights** (from Claude research):
  - Industry context or best practices
  - Relevant considerations
  - Potential approaches to discuss
- **Key Discussion Points**:
  - Topics that need airtime
  - Open questions to resolve
  - Decisions required
- **What We Need from This Meeting**:
  - Expected outcomes
  - Decisions to make
  - Next steps to define

Audience: Internal attendees only
Purpose: Give team full context and alignment before meeting
```

### Step 6: Create external agenda

```
Use Notion:notion-create-pages for meeting doc:

Title: "[Meeting Topic] - Agenda"

Content structure:
- **Meeting Details**: Date, time, attendees
- **Objective**: Clear meeting goal (1-2 sentences)
- **Agenda Items** (with time allocations):
  1. Topic 1 (10 min)
  2. Topic 2 (20 min)
  3. Topic 3 (15 min)
- **Discussion Topics**: 
  - Key items to cover
  - Questions to answer
- **Decisions Needed**: 
  - Clear decision points
- **Action Items**: 
  - (To be filled during meeting)
- **Related Resources**:
  - Links to relevant pages
  - Link to pre-read document

Audience: All participants (internal + external)
Purpose: Structure the meeting, keep it on track
Tone: Professional, focused, clear
```

See [reference/template-selection-guide.md](reference/template-selection-guide.md) for full templates.

### Step 7: Link documents

```
1. Link pre-read to agenda:
   - Add mention in agenda: "See <mention-page>Pre-Read</mention-page> for background"

2. Link both to project:
   - Update project page with meeting links
   - Add to "Meetings" section

3. Cross-reference:
   - Agenda mentions pre-read for internal attendees
   - Pre-read mentions agenda for meeting structure
```

## Document Types

### Internal Pre-Read (for team)

More comprehensive, internal context:
- Full background and history
- Internal metrics and data
- Honest assessment of challenges
- Strategic considerations
- What we need to achieve
- Internal discussion points

**When to create**: Always for important meetings with internal team

### External Agenda (for all participants)

Clean, professional, focused:
- Clear objectives
- Structured agenda with times
- Discussion topics
- Decision items
- Professional tone

**When to create**: Every meeting

### Agenda Types by Meeting Purpose

**Decision Meeting**: Meeting Details → Objective → Options (Pros/Cons) → Recommendation → Discussion → Decision → Action Items

**Status Update**: Meeting Details → Project Status → Progress → Upcoming Work → Blockers → Discussion → Action Items

**Customer/External**: Meeting Details → Objective → Agenda Items (timed) → Discussion Topics → Next Steps

**Brainstorming**: Meeting Details → Objective → Constraints → Ideas → Discussion → Next Steps

See [reference/template-selection-guide.md](reference/template-selection-guide.md) for complete templates.

## Research Enrichment Patterns

Beyond Notion content, add value through Claude's capabilities:

**Technical Context**: Explain technologies, architectures, or approaches. Provide industry standard practices. Compare common solutions. Suggest evaluation criteria.

**Business Context**: Industry trends affecting topic. Competitive landscape insights. Common challenges in space. ROI considerations.

**Decision Support**: Decision-making frameworks (e.g., RICE, cost-benefit). Risk assessment patterns. Trade-off analysis approaches. Success criteria suggestions.

**Customer Context** (for external meetings): Industry-specific challenges. Common pain points. Best practices from similar companies. Value proposition framing.

**Process Guidance**: Meeting facilitation techniques. Discussion frameworks. Retrospective patterns. Brainstorming structures.

Note: Use general knowledge and analytical capabilities. Don't fabricate specific facts. Clearly distinguish Notion facts from Claude insights.

## Meeting Context Sources

**Project Pages**: Status, goals, team, timelines (most important)
**Previous Meeting Notes**: Historical discussions, action items, decisions (recurring meetings)
**Task/Issue Database**: Current status, blockers, completed/upcoming work (project meetings)
**Specifications/Designs**: Requirements, decisions, approach, open questions (technical meetings)
**Reports/Dashboards**: Metrics, KPIs, performance data, trends (executive meetings)

## Linking Meetings to Projects

**Forward Link**: Add meeting to project page's "Meetings" section
**Backward Link**: Include "Related Project" section in agenda with project mention
**Maintain bidirectional** links for easy navigation

## Meeting Series Management

**Recurring Meetings**: Create series parent page with schedule, meeting notes list, standing agenda, and action items tracker. Link individual meetings to parent.

**Meeting Database**: For organizations, use database with properties: Meeting Title, Date, Type (Decision/Status/Brainstorm), Project, Attendees, Status (Scheduled/Completed)

## Post-Meeting Actions

Update agenda with:

**Decisions**: List each decision with rationale and owner
**Action Items**: Checkbox list with owner and due date (consider creating tasks in database)
**Key Outcomes**: Bullet list of main outcomes

## Meeting Prep Timing

**Day-Before** (next-day meetings): Gather context → create agenda → share with attendees → allow review time
**Hour-Before** (last-minute): Quick context → brief pre-read → basic agenda → essentials only
**Week-Before** (major meetings): Comprehensive research → detailed pre-read → structured agenda → pre-meeting reviews

## Best Practices

1. **Create both documents**: Internal pre-read + external agenda for important meetings
2. **Distinguish sources**: Label what's from Notion vs. Claude research
3. **Start with search**: Cast wide net in Notion, then narrow
4. **Keep pre-read concise**: 2-3 pages maximum, even with research
5. **Professional external docs**: Agenda should be polished and focused
6. **Enrich thoughtfully**: Claude research should add real value, not fluff
7. **Link documents**: Pre-read mentions agenda, agenda mentions pre-read
8. **Include metrics**: Data from Notion helps ground discussions
9. **Share appropriately**: Pre-read to internal team, agenda to all participants
10. **Share early**: Give attendees time to review (24hr+ for important meetings)
11. **Update post-meeting**: Capture decisions and actions in agenda

## Advanced Features

**Meeting templates**: See [reference/template-selection-guide.md](reference/template-selection-guide.md) for comprehensive template library

## Common Issues

**"Too much context"**: Split into pre-read (internal, comprehensive) and agenda (external, focused)
**"Can't find relevant pages"**: Broaden search, try different terms, ask user for page URLs
**"Meeting purpose unclear"**: Ask user to clarify before proceeding
**"No recent updates"**: Note that in pre-read, focus on historical context and strategic considerations
**"External meeting - no internal context"**: Create simpler structure with just agenda, skip internal pre-read or keep it minimal
**"Claude research too generic"**: Focus on specific insights relevant to the actual meeting topic, not general platitudes

## Examples

See [examples/](examples/) for complete workflows:
- [examples/project-decision.md](examples/project-decision.md) - Decision meeting prep with pre-read
- [examples/sprint-planning.md](examples/sprint-planning.md) - Sprint planning meeting
- [examples/executive-review.md](examples/executive-review.md) - Executive review prep
- [examples/customer-meeting.md](examples/customer-meeting.md) - External meeting with customer (pre-read + agenda)

