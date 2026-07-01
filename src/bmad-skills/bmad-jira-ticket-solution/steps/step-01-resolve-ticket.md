---
---

# Step 1: Resolve & Read the Ticket

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Do not start code analysis until `{ticket_key}` is confirmed and the ticket body is loaded
- Read the ticket as evidence, not as ground truth — its claims get verified against code in Step 2

## INSTRUCTIONS

1. **Extract the ticket key:**

   - Match `{workflow.ticket_pattern}` against the user's prompt / arguments.
   - If none is found, ask once: *Which Jira ticket should I analyze? (e.g. NCC-1234)* — **HALT** until answered.
   - Set `{ticket_key}`.

2. **Fetch the ticket** per `{workflow.jira_fetch}`:

   - **`"mcp"`** — use the Atlassian MCP. First resolve the cloud id if needed (`getAccessibleAtlassianResources`), then `getJiraIssue` for `{ticket_key}`. If `{workflow.include_comments}` is true, pull comments as well (they often carry the real root-cause discussion and prior attempts). If the Atlassian tools are unreachable or unauthorized, tell the user and fall back to `"manual"`.
   - **`"manual"`** — ask the user to paste the ticket summary + description (+ comments). **HALT** until provided.

3. **Extract into `{ticket}`** (structured, not prose):

   - `summary`, `type` (bug / story / task), `status`, `priority`, `components`, `labels`
   - `description` — the body, preserved
   - `acceptance_criteria` — explicit ACs if present; else note "none stated"
   - `repro_steps` / `expected vs actual` (for bugs)
   - `comments` — a short digest of each substantive comment (author + the technical claim/decision), flagged where comments disagree with each other
   - `links` — linked issues, PRs, logs, dashboards, attachments (record URLs; do not fetch external systems without asking)

4. **Identify the target codebase:**

   - Default to the current `{project-root}` repo. Confirm it is the right repo for this ticket (the ticket's component/service should map to code here). If the ticket clearly targets a different repo than the working directory, say so and ask which repo to analyze. Set `{repo_root}`.

5. **Confirm with the user** (one line unless ambiguous):

   > Analyzing **{ticket_key}** — *{summary}* ({type}, components: {components}) against `{repo_root}`. Proceed?

   Surface anything that changes scope now: multiple components, "spike"/research tickets, missing ACs, or comments that contradict the description. **HALT** until confirmed.

6. **Frame the analysis question** — from the ticket type, state in one line what Step 2 must establish:

   - **Bug** → "Where and why does {observed behavior} happen?" (find the root cause)
   - **Feature/story** → "Where does {capability} integrate, and what must change?" (find the seams)
   - **Refactor/tech-debt** → "What is the current shape and what constrains the change?"

## NEXT

Read fully and follow: `./step-02-analyze-code.md`
