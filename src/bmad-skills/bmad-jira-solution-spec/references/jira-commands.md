# Jira MCP, Attachments, Commands, and Fallbacks

## Atlassian MCP (preferred)

1. **Authenticate** — if tools fail, call `mcp_auth` for the Atlassian server once.
2. **Resolve cloud** — `getAccessibleAtlassianResources` → `cloudId`, site URL.
3. **Fetch issue** — `getJiraIssue(cloudId, issueIdOrKey, fields)` using `{workflow.jira_fields}` (must include `attachment`).
4. **List assigned** — when the user has no key:

   ```text
   searchJiraIssuesUsingJql(
     cloudId,
     jql = "assignee = currentUser() AND status != Done ORDER BY updated DESC",
     fields = ["summary", "status", "issuetype", "priority"],
     maxResults = 10
   )
   ```

5. **Linked issues** — `getJiraIssue` on link keys, or expand `issuelinks` from the parent fetch.

## Attachments

For each item in the issue `attachment` array (respect `{workflow.attachment_max_count}` and `{workflow.attachment_max_bytes}`):

1. Record metadata: `id`, `filename`, `mimeType`, `size`, `author`, `created`.
2. Download to `_bmad_output/{artifact_subdir}/{ticket_key}/attachments/{filename}`:
   - Use Atlassian MCP attachment/content download when the server exposes it.
   - Else `GET` the attachment `content` URL from the Jira REST response (same auth as MCP).
   - On failure: ask the user to save the file into that folder or paste text contents.
3. Read and summarize — never cite attachment claims without reading the file.

**High-value attachment types:** `.log`, `.txt`, `.json`, `.xml`, `.har`, `.sql`, `.sh`, `.bash`, `.md`, `.csv`, stack traces in `.pdf` (extract if possible). Images: describe UI/error state briefly.

## Command extraction

Scan description, comments, and attachment text for:

| Pattern | Type |
| --- | --- |
| Fenced ` ```bash ` / ` ```shell ` blocks | repro / diagnostic |
| Lines starting with `$`, `curl`, `wget`, `http `, `kubectl`, `docker` | repro / diagnostic |
| `npm `, `yarn`, `pnpm`, `gradle`, `mvn`, `./mvnw`, `make`, `pytest`, `go test` | test / build |
| `INSERT`/`UPDATE`/`DELETE`/`SELECT` SQL | data |
| API paths with method (`POST /api/...`) | repro (convert to curl when possible) |

Assign each command an ID (`C1`, `C2`, …), source (description / comment / `error.log`), and **safe to run** (`yes` | `ask` | `no`). See Step 2 rules.

## Running commands (Step 3 only)

Controlled by `{workflow.run_diagnostic_commands}`:

- `"never"` — extract and list only; no execution
- `"safe_only"` — auto-run `yes` read-only commands
- `"ask"` — prompt before any execution

Truncate captured output to `{workflow.command_output_max_lines}` lines in the compact analysis.

## Manual fallback

When MCP is unavailable, ask the user to paste:

- Summary, description, AC / DoD
- Issue type, status, labels, assignee
- Repro and diagnostic commands (exact syntax)
- Attachment files or pasted log/stack trace contents

Record `{jira_source}: manual`.

## Story file lookup

1. `_bmad_output/**/*{ticket_key}*`
2. `{implementation_artifacts}/**/*{ticket_key}*`
3. Sprint/status files referencing `{ticket_key}`

## Ticket URL

`https://{site}.atlassian.net/browse/{ticket_key}`
