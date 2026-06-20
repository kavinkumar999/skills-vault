---
---

# Step 2: Fetch Jira Context, Attachments, and Commands

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Every ticket claim you use later must be traceable to something fetched here
- **Download and read attachments** — do not list filenames only
- If Jira is unreachable, **HALT** and ask the user to paste summary, description, AC, commands, and attachment contents — do not proceed on guesses

## INSTRUCTIONS

1. **Authenticate Atlassian MCP when needed:**

   - If MCP tools fail with auth errors, call `mcp_auth` for the Atlassian server once, then retry.
   - If MCP is unavailable, ask the user to paste: summary, description, issue type, labels, acceptance criteria, relevant comments, **repro/diagnostic commands**, and **attachment contents or files**. Record `{jira_source}: manual`.

2. **Fetch the issue:**

   ```
   getAccessibleAtlassianResources → cloudId, site URL
   getJiraIssue(cloudId, issueIdOrKey={ticket_key}, fields={workflow.jira_fields})
   ```

   Build structured `{ticket_context}`:

   | Field | Value |
   | --- | --- |
   | Key | {ticket_key} |
   | Summary | … |
   | Type | … |
   | Status | … |
   | Priority | … |
   | Assignee | … |
   | Reporter | … |
   | Labels / components | … |
   | Parent / epic | … |
   | Linked issues | … |

3. **Parse description and comments:**

   - Extract `{problem_narrative}` — what the reporter says is wrong or needed.
   - Extract `{acceptance_criteria}` — numbered AC lines, checklist items, or "Definition of Done" bullets. If none exist, note `{ac_missing}: true`.
   - Include up to `{workflow.jira_comment_limit}` newest comments that add technical context (repro steps, logs, prior attempts). Skip noise ("bump", "+1").

4. **Extract commands `{ticket_commands}`:**

   Scan description, comments, and (after ingest) attachment text for executable instructions. See `references/jira-commands.md` for patterns.

   For each command, record:

   | ID | Source | Type | Command | Safe to run? |
   | --- | --- | --- | --- | --- |
   | C1 | description | repro | `curl -s …` | yes / ask / no |
   | C2 | comment #3 | diagnostic | `kubectl logs …` | ask |

   **Types:** `repro`, `diagnostic`, `test`, `build`, `deploy`, `data`, `other`.

   **Safe to run** rules:
   - `yes` — read-only GET/curl, local grep, `git log`, test runners with no side effects
   - `ask` — needs env/credentials, writes data, hits shared staging/prod
   - `no` — destructive (delete, drop, force push, prod writes) — never run; cite only

   Deduplicate identical commands. Preserve exact syntax (flags, URLs, headers).

5. **Fetch and ingest attachments `{attachments}`:**

   From the issue `attachment` field (up to `{workflow.attachment_max_count}` files, skip larger than `{workflow.attachment_max_bytes}`):

   1. List: filename, mime type, size, author, created.
   2. Download each file to `{attachment_dir}` =
      `_bmad_output/{workflow.artifact_subdir}/{ticket_key}/attachments/`
      - Prefer Atlassian MCP attachment download when available.
      - Else use the attachment `content` URL from the Jira API response with authenticated fetch.
      - If download fails, ask the user to drop the file into `{attachment_dir}` or paste contents. **HALT** only when `{workflow.require_attachments}` is true and zero files were ingested.
   3. **Read and summarize** each ingested file into `{attachment_summaries}`:

      | File | Type | Key extracts |
      | --- | --- | --- |
      | `error.log` | log | stack trace line 42: `NullPointerException` in `SessionService.refresh` |
      | `repro.sh` | script | adds to `{ticket_commands}` as C3 |
      | `screenshot.png` | image | UI shows timeout modal on login |

      Handle by type: `.log`/`.txt`/`.json`/`.xml`/`.har`/`.sql`/`.sh`/`.md` → read text; extract errors, IDs, timestamps, endpoints; pull embedded commands into `{ticket_commands}`. Images → brief visual description. Binaries → note type/size; extract text only if tooling allows.

6. **Assignee check:**

   - If assignee is set and is not the current user (compare login/email when known), say:
     > This ticket is assigned to **{assignee}**, not you. Continue anyway?
   - **HALT** until confirmed when mismatched.

7. **Set URLs and paths:**

   - `{ticket_url}` from Jira response.
   - `{compact_report_path}` = `_bmad_output/{workflow.artifact_subdir}/{ticket_key}-compact-analysis.md`

8. **Linked context (optional, when links exist):**

   - For "blocks / is blocked by / relates to" links, fetch linked issue summaries only.
   - For a parent Epic, pull epic summary + key only.

9. **Story file cross-check (BMad integration):**

   - Search `_bmad_output/` and `{implementation_artifacts}` for a story file matching `{ticket_key}`.
   - If found, set `{story_file}` and merge AC/tasks into `{acceptance_criteria}`.

10. **Summarize what was fetched** — type, status, AC count, comment count, **attachment count (ingested)**, **command count**, story file y/n. Flag **spec gaps** when description/AC/commands/attachments are all thin.

## NEXT

Read fully and follow: `./step-03-compact-analysis.md`
