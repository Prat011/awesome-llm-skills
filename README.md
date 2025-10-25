<h1 align="center">Awesome LLM Skills</h1>

<p align="center">
  <a href="url">
    <img
      src="https://github.com/user-attachments/assets/16652783-7675-4e63-a699-6b2f849587fc"
      width="50%"
      alt="Awesome LLM Skills">
  </a>
</p>

<p align="center">
  A curated list of awesome LLM Skills, resources, and tools for customizing AI workflows on tools like Claude Code, Codex, Gemini CLI, Qwen Code, OpenCode etc.
</p>


## Contents

- [What Are LLM Skills?](#what-are-llm-skills)
- [Quick Start](#quick-start)
- [Platforms](#platforms)
  - [Claude Code (Anthropic)](#claude-code-anthropic)
  - [Claude Desktop (Anthropic)](#claude-desktop-anthropic)
  - [Codex CLI (OpenAI)](#codex-cli-openai)
  - [Gemini CLI (Google)](#gemini-cli-google)
  - [OpenCode (Open-source CLI)](#opencode)
  - [Qwen Code (Alibaba)](#qwen-code)
- [Skills](#skills)
  - [Official](#official)
  - [Community](#community)
- [Contributing](#contributing)
  - [Quick Contribution Steps](#quick-contribution-steps)
- [Resources](#resources)
  - [Official Documentation](#official-documentation)
  - [Community Resources](#community-resources)
- [License](#license)


## What Are LLM Skills?

LLM Skills are customizable workflows that teach LLM how to perform specific tasks according to your unique requirements. Skills enable LLM to execute tasks in a repeatable, standardized manner across all LLM platforms.

## Quick Start

1. **Create a project-local or user-level skill folder**
   Use one of these discovery paths so Claude Code finds it automatically:

   * Project: `.claude/skills/webapp-testing/`
   * User: `~/.claude/skills/webapp-testing/`

2. **Add `SKILL.md`** (required)

  Basic Skill Template:
  
  ```markdown
  ---
  name: my-skill-name
  description: A clear description of what this skill does and when to use it.
  ---
  
  # My Skill Name
  
  Detailed description of the skill's purpose and capabilities.
  
  ## When to Use This Skill
  
  - Use case 1
  - Use case 2
  - Use case 3
  
  ## Instructions
  
  [Detailed instructions for LLMs on how to execute this skill]
  
  ## Examples
  
  [Real-world examples showing the skill in action]
  ```

  - Focus on specific, repeatable tasks
  - Include clear examples and edge cases
  - Write instructions for LLM, not end users
  - Document prerequisites and dependencies
  - Include error handling guidance

3. **Keep supporting files small**
   Add only what’s needed (e.g., small fixtures in `resources/`, helper scripts). This keeps skills snappy to load and easier for Claude to apply.

4. **Load the skill**

   * **Claude (web or Desktop):** Upload a ZIP via **Settings → Capabilities → Skills** → **Upload skill**. 
   * **Claude Code (terminal):** Place the folder under `.claude/skills/` (project) or `~/.claude/skills/` (user). Claude Code discovers skills from these locations.
   * **Other CLIs (Codex, Gemini, OpenCode, Qwen Code):** They don’t use Anthropic’s Skills format natively—reference your `SKILL.md` in prompts (Gemini CLI supports `@` file/context attachments).
  
5. **Use it**
   Just ask in natural language, optionally mentioning the skill by name—for example:
   “Use the **Webapp Testing** skill to validate the checkout flow and generate `report.md`.” Claude can auto-invoke relevant skills based on your request. 

6. **(Optional) Kickstart a repo session in Claude Code**
   Slash-commands are supported; many users run `/init` to generate a `CLAUDE.md` and bootstrap context before working.

## Platforms

### Claude Code (Anthropic)

**Set‑up and enable skills**

* Install the CLI with `npm install -g @anthropic-ai/claude-code` (requires Node 18+) and run `claude` inside your project folder to start a session. The first run opens a browser window to log in with your Anthropic account.
* To use skills, place your skill folder in the project (e.g., `./skills/webapp-testing/`) and initialize context with `/init`. Claude Code automatically discovers skills using the progressive scanning mechanism described above.
* You can also upload skills to your account via the web app; Claude Code will load them when relevant.

### Claude Desktop (Anthropic)

**Set‑up and enable skills**

* Download Claude Desktop from the official site and sign in with your account. Enable code execution and file‑creation capabilities under **Settings → Capabilities** and toggle skills on or off.
* To add a custom skill, upload a ZIP file containing your skill folder in the Skills section.


### Codex CLI (OpenAI)

**Set‑up and enable skills**

* Install the CLI via `npm install -g @openai/codex` or `brew install codex`. Run `codex` in your project directory; on first launch you’ll authenticate with your ChatGPT or API account.
* Codex doesn’t yet support Anthropic‑style skills, but you can replicate a skill’s workflow by writing a `SKILL.md` in your repository and prompting Codex to follow the instructions. For portability, keep the same folder structure as other skills (e.g., `skills/my-feature/` with `SKILL.md`). Codex can read files and follow step‑by‑step instructions, enabling you to reuse skill instructions across agents.

### Gemini CLI (Google)

**Set‑up and enable skills**

* Install Node 20+ and then install Gemini CLI via `npm install -g @google/gemini-cli` or run it on‑demand with `npx @google/gemini-cli`.
* Run `gemini` and sign in with your Google account; a browser window will open for authentication. Gemini CLI currently doesn’t have built‑in support for Anthropic skills, but you can follow skill instructions by loading your own `SKILL.md` file and referencing it in prompts. Use the `@` symbol to upload files containing your skill instructions.

### OpenCode

**Set‑up and enable skills**

* Install OpenCode with a one‑line script: `curl -fsSL https://opencode.ai/install | bash`.
* Run `opencode auth login` and choose your provider (e.g., Cerebras) to configure your API key.
* Start the interface with `opencode` and initialize your project context using `/init`.
* OpenCode doesn’t natively load Anthropic skills, but you can place a `skills/` folder in your project and ask OpenCode to read the `SKILL.md` file; this approximates skills functionality and lets you reuse instructions across tools.

### Qwen Code

**Set‑up and enable skills**

* Ensure Node 20+ is installed, then install Qwen Code with `npm install -g @qwen-code/qwen-code@latest` and verify with `qwen --version`. Alternatively, clone the repository and install locally.
* Start a session by running `qwen`. Qwen Code currently doesn’t support Anthropic skills directly, but you can still adopt the skill pattern by creating a `skills/` directory and prompting Qwen Code to follow the instructions in your `SKILL.md` files.

## Skills

### Official

| Skill                     | Category                    | Link                           | Description                                                                                                                                                 |
| ------------------------- | --------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Brand Guidelines          | Business & Marketing        | `./brand-guidelines/`          | Applies Anthropic's official brand colors and typography to artifacts for consistent visual identity and professional design standards.                     |
| Competitive Ads Extractor | Business & Marketing        | `./competitive-ads-extractor/` | Extracts and analyzes competitors' ads from ad libraries to understand messaging and creative approaches that resonate.                                     |
| Domain Name Brainstormer  | Business & Marketing        | `./domain-name-brainstormer/`  | Generates creative domain name ideas and checks availability across multiple TLDs including .com, .io, .dev, and .ai extensions.                            |
| Internal Comms            | Business & Marketing        | `./internal-comms/`            | Helps write internal communications including 3P updates, company newsletters, FAQs, status reports, and project updates using company-specific formats.    |
| Lead Research Assistant   | Business & Marketing        | `./lead-research-assistant/`   | Identifies and qualifies high-quality leads by analyzing your product, searching for target companies, and providing actionable outreach strategies.        |
| Content Research Writer   | Communication & Writing     | `./content-research-writer/`   | Assists in writing high-quality content by conducting research, adding citations, improving hooks, and providing section-by-section feedback.               |
| Meeting Insights Analyzer | Communication & Writing     | `./meeting-insights-analyzer/` | Analyzes meeting transcripts to uncover behavioral patterns including conflict avoidance, speaking ratios, filler words, and leadership style.              |
| Canvas Design             | Creative & Media            | `./canvas-design/`             | Creates beautiful visual art in PNG and PDF documents using design philosophy and aesthetic principles for posters, designs, and static pieces.             |
| Image Enhancer            | Creative & Media            | `./image-enhancer/`            | Improves image and screenshot quality by enhancing resolution, sharpness, and clarity for professional presentations and documentation.                     |
| Slack GIF Creator         | Creative & Media            | `./slack-gif-creator/`         | Creates animated GIFs optimized for Slack with validators for size constraints and composable animation primitives.                                         |
| Theme Factory             | Creative & Media            | `./theme-factory/`             | Applies professional font and color themes to artifacts including slides, docs, reports, and HTML landing pages with 10 pre-set themes.                     |
| Video Downloader          | Creative & Media            | `./video-downloader/`          | Downloads videos from YouTube and other platforms for offline viewing, editing, or archival with support for various formats and quality options.           |
| Artifacts Builder         | Development                 | `./artifacts-builder/`         | Builds elaborate, multi-component Claude.ai HTML artifacts using modern frontend technologies including React, Tailwind CSS, and shadcn/ui.                 |
| Changelog Generator       | Development                 | `./changelog-generator/`       | Automatically creates user-facing changelogs from git commits by analyzing history and transforming technical commits into customer-friendly release notes. |
| MCP Builder               | Development                 | `./mcp-builder/`               | Guides creation of high-quality MCP (Model Context Protocol) servers for integrating external APIs and services with LLMs using Python or TypeScript.       |
| Skill Creator             | Development                 | `./skill-creator/`             | Provides guidance for creating effective LLM skills that extend capabilities with specialized knowledge, workflows, and tool integrations.                  |
| Webapp Testing            | Development                 | `./webapp-testing/`            | Tests local web applications using Playwright for verifying frontend functionality, debugging UI behavior, and capturing screenshots.                       |
| File Organizer            | Productivity & Organization | `./file-organizer/`            | Intelligently organizes files and folders by understanding context, finding duplicates, and suggesting better organizational structures.                    |
| Invoice Organizer         | Productivity & Organization | `./invoice-organizer/`         | Automatically organizes invoices and receipts for tax preparation by reading files, extracting information, and renaming consistently.                      |
| Raffle Winner Picker      | Productivity & Organization | `./raffle-winner-picker/`      | Randomly selects winners from lists, spreadsheets, or Google Sheets for giveaways and contests with cryptographically secure randomness.                    |


### Community
| Skill                         | Category                    | Link                                                                                                                                     | Description                                                                                                               | Author             |
| ----------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| D3.js Visualization           | Development                 | [https://github.com/chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill)                         | Teaches Claude to produce D3 charts and interactive data visualizations.                                                  | @chrisvoncsefalvay |
| FFUF Web Fuzzing              | Development                 | [https://github.com/jthack/ffuf_claude_skill](https://github.com/jthack/ffuf_claude_skill)                                               | Integrates the ffuf web fuzzer so Claude can run fuzzing tasks and analyze results for vulnerabilities.                   | @jthack            |
| iOS Simulator                 | Development                 | [https://github.com/conorluddy/ios-simulator-skill](https://github.com/conorluddy/ios-simulator-skill)                                   | Enables Claude to interact with iOS Simulator for testing and debugging iOS applications.                                 | @conorluddy        |
| Playwright Browser Automation | Development                 | [https://github.com/lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill)                                             | Model-invoked Playwright automation for testing and validating web applications.                                          | @lackeyjb          |
| Skill Seekers                 | Development                 | [https://github.com/yusufkaraaslan/Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers)                                       | Automatically converts any documentation website into a Claude AI skill in minutes.                                       | @yusufkaraaslan    |
| CSV Data Summarizer           | Productivity & Organization | [https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) | Automatically analyzes CSV files and generates comprehensive insights with visualizations without requiring user prompts. | @coffeefuelbump    |
| Markdown to EPUB Converter    | Productivity & Organization | [https://github.com/smerchek/claude-epub-skill](https://github.com/smerchek/claude-epub-skill)                                           | Converts markdown documents and chat summaries into professional EPUB ebook files.                                        | @smerchek          |
| NotebookLM Integration        | Productivity & Organization | [https://github.com/PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill)                                   | Lets Claude Code chat directly with NotebookLM for source-grounded answers based exclusively on uploaded documents.       | @PleasePrompto     |


## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- How to submit new skills
- Skill quality standards
- Pull request process
- Code of conduct

### Quick Contribution Steps

1. Ensure your skill is based on a real use case
2. Check for duplicates in existing skills
3. Follow the skill structure template
4. Test your skill across platforms
5. Submit a pull request with clear documentation

## Resources

### Official Documentation

- [LLM Skills Overview](https://www.anthropic.com/news/skills) - Official announcement and features
- [Skills User Guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude) - How to use skills in LLMs
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills) - Skill development guide
- [Skills API Documentation](https://docs.claude.com/en/api/skills-guide) - API integration guide
- [Agent Skills Blog Post](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Engineering deep dive

### Community Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills) - Official example skills
- [Claude Community](https://community.anthropic.com) - Discuss skills with other users
- [Skills Marketplace](https://claude.ai/marketplace) - Discover and share skills
- [Notion Skills](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) - Notion integration skills

## License

This repository is licensed under the Apache License 2.0.

Individual skills may have different licenses - please check each skill's folder for specific licensing information.

---
