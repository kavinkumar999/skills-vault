---
---

# Step 1: Discover the Jira Ticket

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Do not fetch Jira or search the codebase until `{ticket_key}` is confirmed
- When the ticket is assigned to someone other than the current user, warn once and continue only if the user confirms

## INSTRUCTIONS

1. **Resolve the ticket key:**

   - If the user provided a key or URL, extract `{ticket_key}` by matching `{workflow.ticket_pattern}`.
   - Else search the current git branch name and recent commits for `{workflow.ticket_pattern}`.
   - Else if `{workflow.list_assigned_when_missing}` is `"ask"` and Atlassian MCP is available:
     - Call `getAccessibleAtlassianResources` to get `{cloud_id}`.
     - Call `searchJiraIssuesUsingJql` with JQL like `assignee = currentUser() AND status != Done ORDER BY updated DESC` (limit 10).
     - Present a numbered list: key, summary, status. Ask which ticket to analyze. **HALT** until answered.
   - Else ask once: *Which Jira ticket should I analyze? (pattern: {workflow.ticket_pattern})* — **HALT** until answered.

2. **Set artifact paths:**

   - `{report_path}` = `_bmad_output/{workflow.artifact_subdir}/{ticket_key}-solution-spec.md`
   - `{compact_report_path}` = `_bmad_output/{workflow.artifact_subdir}/{ticket_key}-compact-analysis.md`
   - `{attachment_dir}` = `_bmad_output/{workflow.artifact_subdir}/{ticket_key}/attachments/`
   - `{ticket_url}` = Jira browse URL when known, else placeholder until Step 2 resolves the site.

3. **Confirm with the user** (one line unless ambiguous):

   > Analyzing Jira ticket **{ticket_key}** — pull ticket, attachments, and commands → compact analysis → codebase investigation → solution spec.

   If the user named multiple tickets, analyze one at a time unless they explicitly asked for a batch (batch is out of scope for v1 — pick the first and note the rest).

4. **Load references** — skim before Step 2:

   - `references/jira-commands.md` — MCP, attachments, command extraction
   - `references/compact-analysis-template.md` — Step 3 artifact shape
   - `references/solution-spec-template.md` — Step 5–6 artifact shape

## NEXT

Read fully and follow: `./step-02-fetch-jira.md`
