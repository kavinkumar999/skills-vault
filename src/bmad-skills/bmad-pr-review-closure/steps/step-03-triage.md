---
---

# Step 3: Triage

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Read code at cited lines before classifying
- **Use `{feedback_index}` and `{files_to_read}`** — read each file once per path group; do not re-fetch GraphQL
- Copilot and human items use different fields — do not conflate

## INSTRUCTIONS

### Load index

Read `{index_path}` (or in-memory `{feedback_index}`). Full thread bodies: `{report_path}` appendix only when excerpt is insufficient.

### Copilot items (`{copilot_threads}`)

For each thread in the index (skip `{copilot_resume_threads}`):

1. Read `path:line` **once per file** using `{files_to_read}` grouping. If `is_outdated` and concern no longer applies → recommend `no_action`.
2. Valid suggestion → `fix`; wrong/out of scope → `no_action`; valid but later → `defer`; unsure → `decision_needed`.
3. If `suggestion_block` applies cleanly → `apply_suggestion: true`.
4. Record: `id`, `source: copilot`, `thread_id`, `recommendation`, `title`, `rationale`, `suggested_change`, `apply_suggestion`, `draft_defer_reason`.

### Human items (`{feedback_items}`)

For each item:

1. Read code, PR body, tests as needed.
2. Set `validity`: valid | partially_valid | invalid | needs_clarification.
3. Set `fix_kind`: code_change | pr_description | evidence | docs | reply_only | decision_needed.
4. Recommend: fix | defer | no_action | decision_needed.
5. Record: `id`, `source: human`, `reviewer`, `severity`, `fix_kind`, `recommendation`, `title`, `rationale`, `draft_response_issue`, `draft_response_resolution`.

### Deduplicate

Merge duplicate Copilot threads or human items covering the same issue; note merged IDs.

## NEXT

Read fully and follow: `./step-04-present.md`
