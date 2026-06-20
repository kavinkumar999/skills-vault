---
---

# Step 5: Draft the Solution Spec

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}` — but compose the **artifact** in `{workflow.document_language}`
- Render only the sections listed in `{workflow.sections}`, in that order
- **Embed the compact analysis** — full solution spec builds on `{compact_report_path}`, not a duplicate ticket dump
- No implementation step without a code citation from Step 4
- The handoff section is mandatory

## INSTRUCTIONS

Draft `{solution_spec_draft}` following `references/solution-spec-template.md`.

1. **compact_analysis** — include the approved compact report verbatim, or link to `{compact_report_path}` plus a 3-line executive summary if the team prefers a slimmer spec (`{workflow.embed_compact_analysis}` = `"full"` | `"link"`).

2. **ticket_summary** — key, URL, type, status, assignee, story file link.

3. **attachments_and_commands** — condensed tables from Step 2–3: attachments ingested (path under `{attachment_dir}`), commands with validation status from `{command_validation}`.

4. **problem_statement** — refined after investigation; reference attachment/command evidence.

5. **acceptance_criteria** — AC table with validation status from Step 4.

6. **code_validation** — full `{validation}` table + key files list.

7. **root_cause** — ranked hypotheses with file:line refs and evidence chain (attachment → command → code).

8. **proposed_solution** — recommended approach aligned with codebase patterns.

9. **implementation_plan** — ordered tasks with files; reference repro commands in test_plan where applicable.

10. **risks** — when `{risk_signals}` non-empty.

11. **test_plan** — extend existing tests; include ticket repro commands as manual/automated checks.

12. **open_questions** — Blocking / Non-blocking.

13. **agent_handoff** — recommended agent, prompt hint, paths to **both** `{compact_report_path}` and `{report_path}`.

## NEXT

Read fully and follow: `./step-06-present-and-handoff.md`
