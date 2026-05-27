# AI Pieces Collections

A curated collection of reusable AI skills, instructions, and tool playbooks for engineering workflows.

This repository focuses on practical, execution-oriented assets you can plug into Copilot/agent workflows for architecture planning, implementation breakdown, testing, browser automation, documentation, frontend design, and diagram generation.

## What is included

- 19 reusable skills under `skills/`
- 11 reusable instructions under `instructions/`
- 1 tool playbook under `tools/`
- 1 MCP integration reference under `mcp/`
- 1 workspace MCP server config under `.vscode/mcp.json`
- Supporting reference docs and helper scripts for specific skills

## Repository structure

```text
.
|-- .vscode/
|   `-- mcp.json
|-- instructions/
|   |-- agent-skills.instructions.md
|   |-- agents.instructions.md
|   |-- code-review-generic.instructions.md
|   |-- commit-message.instructions.md
|   |-- go.instructions.md
|   |-- kubernetes-deployment-best-practices.instructions.md
|   |-- kubernetes-manifests.instructions.md
|   |-- markdown.instructions.md
|   |-- playwright-python.instructions.md
|   |-- shell.instructions.md
|   `-- sql-sp-generation.instructions.md
|-- mcp/
|   `-- drawio-mcp/
|       `-- README.md
|-- skills/
|   |-- agent-browser/
|   |-- ai-fomo/
|   |-- breakdown-epic-arch/
|   |-- breakdown-feature-implementation/
|   |-- breakdown-test/
|   |-- chrome-devtools/
|   |-- create-architectural-decision-record/
|   |-- create-readme/
|   |-- create-technical-spike/
|   |-- curl-api-testing/
|   |-- documentation-writer/
|   |-- drawio/
|   |-- frontend-design/
|   |-- generate-import-export-import-files/
|   |-- meeting-minutes/
|   |-- playwright-generate-test/
|   |-- playwright-recording/
|   |-- skill-creator/
|   `-- robot-framework-py/
|-- tools/
|   `-- markitdown/
|       `-- README.md
`-- LICENSE
```

## Skill catalog

| Skill | Purpose |
|---|---|
| `agent-browser` | Install and use the Agent Browser skill for browser-driven automation flows. |
| `ai-fomo` | Turn AI information overload into reusable knowledge, signals, and digest workflows. |
| `breakdown-epic-arch` | Create high-level technical architecture from an Epic PRD. |
| `breakdown-feature-implementation` | Generate detailed feature implementation plans (monorepo-oriented). |
| `breakdown-test` | Build test strategy and QA planning artifacts. |
| `chrome-devtools` | Browser automation and debugging via Chrome DevTools MCP. |
| `create-architectural-decision-record` | Generate structured ADR documents. |
| `create-readme` | Create concise, high-quality project README files. |
| `create-technical-spike` | Create time-boxed technical spike documents before implementation. |
| `curl-api-testing` | Test and debug REST APIs with reproducible `curl` workflows and compact result reports. |
| `documentation-writer` | Produce docs using the Diataxis framework. |
| `drawio` | Generate native `.drawio` diagrams and optional exports. |
| `frontend-design` | Build distinctive, production-grade frontend UI and pages. |
| `generate-import-export-import-files` | Generate valid/invalid import JSON datasets for import-export testing scenarios. |
| `meeting-minutes` | Generate concise meeting minutes with actions and decisions. |
| `playwright-generate-test` | Generate Playwright tests from scenario-driven flows. |
| `playwright-recording` | Record and refine Playwright tests with codegen workflow. |
| `robot-framework-py` | Build/refactor Python-centric Robot Framework test suites. |
| `skill-creator` | Create, optimize, and evaluate skills for trigger quality and performance. |

## Instruction catalog

| Instruction | Purpose |
|---|---|
| `agent-skills.instructions.md` | Best practices for designing high-quality SKILL files. |
| `agents.instructions.md` | Guidelines for creating custom agent files and tool/model settings. |
| `code-review-generic.instructions.md` | Reusable code review framework and severity model. |
| `commit-message.instructions.md` | Conventional commit format and message quality guidance. |
| `go.instructions.md` | Idiomatic Go coding rules and project conventions. |
| `kubernetes-deployment-best-practices.instructions.md` | Kubernetes deployment quality and operational best practices. |
| `kubernetes-manifests.instructions.md` | Conventions for authoring Kubernetes manifests. |
| `markdown.instructions.md` | CommonMark-aligned markdown writing and validation rules. |
| `playwright-python.instructions.md` | Playwright + Python test authoring and execution guidance. |
| `shell.instructions.md` | Safe, maintainable shell scripting conventions. |
| `sql-sp-generation.instructions.md` | SQL stored procedure generation and quality guidance. |

## Tools catalog

| Tool | Purpose |
|---|---|
| `tools/markitdown` | Document conversion playbook focused on markdown conversion workflows. |

## Quick start

1. Clone this repository.
2. Pick an asset type:
   - Skill: `skills/<skill-name>/SKILL.md`
   - Instruction: `instructions/*.instructions.md`
   - Tool playbook: `tools/<tool-name>/README.md`
3. Use the content as your agent instruction/prompt basis.
4. Follow each file's required folder conventions, constraints, and output paths.

> [!TIP]
> Most skills are designed as opinionated playbooks. Read the full `SKILL.md` before execution to avoid missing required steps, output format constraints, or expected file locations.

## How to use skills effectively

- Keep skills task-specific: one skill per clear outcome.
- Keep instructions language/task specific and scoped by file patterns when possible.
- Preserve each skill's required output format and target path.
- Reuse references/scripts shipped with a skill (for example in `skills/robot-framework-py/references/` and `skills/robot-framework-py/scripts/`).
- For diagram tasks, use the `drawio` skill and pair it with the MCP reference in `mcp/drawio-mcp/` when needed.

## MCP server configuration

This repository includes a workspace-level MCP config at `.vscode/mcp.json`.

Current configured server:

- `drawio-mcp-app-server` (`http`)
- URL: `http://192.168.137.100:3001/mcp`

Example configuration:

```json
{
   "servers": {
      "drawio-mcp-app-server": {
         "url": "http://192.168.137.100:3001/mcp",
         "type": "http"
      }
   },
   "inputs": []
}
```

> [!IMPORTANT]
> If you run this repository in a different environment, update the server URL in `.vscode/mcp.json` to your reachable MCP endpoint.

Quick check:

1. Ensure the MCP endpoint is running and reachable.
2. Open VS Code in this workspace so `.vscode/mcp.json` is applied.
3. Use `drawio` skill flows that depend on MCP connectivity.

## Add a new skill

1. Create a new folder under `skills/<new-skill-name>/`.
2. Add a `SKILL.md` with:
   - YAML front matter (`name`, `description`)
   - clear usage scope
   - strict output requirements
   - examples and constraints
3. Add `references/` or `scripts/` only when they are truly reusable.
4. Keep instructions deterministic and concise.

## Suggested workflow

1. Start from planning skills:
   - `breakdown-epic-arch`
   - `breakdown-feature-implementation`
2. Move to quality and delivery:
   - `breakdown-test`
   - `playwright-generate-test` or `robot-framework-py`
3. Document decisions and outcomes:
   - `create-architectural-decision-record`
   - `documentation-writer`
   - `meeting-minutes`

## Notes

- License is MIT (see `LICENSE`).
- MCP reference currently included: `drawio-mcp`.