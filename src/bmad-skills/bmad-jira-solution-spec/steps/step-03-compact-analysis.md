---
---

# Step 3: Compact Analysis Report

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Concise by design** — this report fits on one screen; no codebase citations yet
- Compose the artifact in `{workflow.document_language}`
- **HALT** after presenting — codebase investigation (Step 4) starts only after the user approves or corrects this analysis
- Optional safe commands may run here only when `{workflow.run_diagnostic_commands}` allows and the user approves

## INSTRUCTIONS

1. **Synthesize `{compact_analysis}`** from Step 2 only (`{ticket_context}`, `{ticket_commands}`, `{attachment_summaries}`, `{acceptance_criteria}`, `{story_file}`). Follow `references/compact-analysis-template.md`.

   Required blocks (keep each block ≤ 5 lines unless AC/commands need more):

   - **One-line ask** — what the developer must deliver
   - **Ticket facts** — type, status, priority, assignee, labels (table or single line)
   - **Problem** — reporter view vs your distilled technical reading
   - **Acceptance criteria** — compact numbered list (max 1 line per AC)
   - **Commands** — table of `{ticket_commands}` (ID, type, command, safe?)
   - **Attachment evidence** — 1 bullet per file: filename → single most important extract
   - **Initial hypothesis** — 1–3 sentences; no file paths yet (code not read)
   - **Investigation plan** — ordered list of what Step 4 will search/read, derived from hypothesis + commands + attachments:
     - search terms (errors, classes, routes, config keys)
     - areas to trace (handler → service → store)
     - commands to run locally if approved (C1, C2…)
   - **Gaps / blockers** — missing repro, missing AC, unreadable attachments, commands needing secrets

2. **Optional — run approved diagnostic commands** (when `{workflow.run_diagnostic_commands}` is not `"never"`):

   - Collect commands marked `safe: yes` automatically when setting is `"safe_only"`.
   - When `"ask"`, offer: *Run N read-only diagnostic commands from the ticket before code investigation? (yes/no/list)* — **HALT** until answered.
   - Run only approved commands; capture stdout/stderr (truncate to `{workflow.command_output_max_lines}` lines).
   - Append results to **Command results** in `{compact_analysis}` — link output to command ID.
   - Failed commands → note in gaps; do not retry destructively.

3. **Present in chat** — show `{compact_analysis}` in a fenced markdown block. Lead with:

   > **Compact analysis — {ticket_key}** — review before codebase investigation.

4. **Collect the decision:**

   - `proceed` / `yes` — write compact artifact, continue to Step 4
   - `edit: <correction>` — update analysis, re-present
   - `run C2` — run one listed command, append result, re-present
   - `skip commands` — clear pending command runs, continue
   - `cancel` — stop

   **HALT** until `proceed` (or equivalent).

5. **Write compact artifact:**

   Save `{compact_analysis}` to `{compact_report_path}`.

   Resolve git-tracked path when applicable (same symlink rules as the solution spec).

6. **Hand state to Step 4:**

   Set `{investigation_plan}` = the Investigation plan section from `{compact_analysis}`.
   Set `{search_queries}` = search terms extracted from investigation plan + attachment evidence.

## NEXT

Read fully and follow: `./step-04-validate-codebase.md`
