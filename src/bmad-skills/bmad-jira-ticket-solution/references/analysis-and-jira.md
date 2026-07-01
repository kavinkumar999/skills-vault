# Reference — Jira fetch & code analysis

## Fetch the ticket (Atlassian MCP)

```text
getAccessibleAtlassianResources          # → cloudId (first run / if unknown)
getJiraIssue(cloudId, issueIdOrKey=NCC-1234)   # summary, description, status, components, ...
# comments are returned with the issue or via the issue's comment expansion
```

Fallbacks when MCP is unavailable:

- `acli jira issue view NCC-1234` (if the Atlassian CLI is installed and authed), or
- ask the user to paste the ticket body (the `"manual"` path).

Never fetch linked external systems (logs, dashboards, attachments) without asking — record their URLs in the plan instead.

## Code analysis (read-only)

```bash
# locate entry points
grep -rn "<symbol or log string>" --include=*.<ext>
# trace history of the suspect lines
git log -p -L <start>,<end>:<file>
git blame -L <start>,<end> <file>
# tests covering the area
grep -rln "<ClassUnderTest>" --include=*Test.*
```

Prefer the dedicated search tools (`Grep`/`Glob`) and read the decisive lines yourself. Use `Explore` / `feature-dev:code-explorer` sub-agents for breadth when the trace spans modules — have them return `file:line` findings, not file contents.

## Evidence discipline

- A fact enters the plan only with a `file:line` you read.
- Inferences are labeled "assumption" and land in *Open questions*.
- When the code contradicts the ticket or a comment, that goes in *Ticket corrections* with the disproving evidence.

## Output

- Plan path: `{planning_artifacts}/{ticket_key}-solution-plan.md`.
- `{planning_artifacts}` is commonly a symlink to a separate BMad-output git repo — commit the plan there and link via its origin (see Step 5; same resolution as `bmad-pr-describe`).
- This skill never edits product code, commits a fix, or opens a PR. Hand off implementation to `bmad-dev-story` / `bmad-quick-dev`.
