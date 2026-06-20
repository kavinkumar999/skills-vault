---
---

# Step 2: Fetch Feedback

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Fetch only what `{review_scope}` includes
- Paginate GraphQL until `hasNextPage` is false
- Follow `{skill-root}/../_shared/token-budget.md` — fetch once, index in Step 2b, triage from index in Step 3

## INSTRUCTIONS

### A — Copilot (when scope is `copilot` or `both`)

1. Fetch threads per `references/github-pr-commands.md`.

2. Build `{copilot_threads}` — unresolved, first comment author in `{workflow.copilot_author_logins}`:

   `thread_id`, `path`, `line`, `is_outdated`, `body` (truncate to `{workflow.thread_body_max_chars}` for in-memory use — full body goes to report appendix in Step 2b), `suggestion_block` (store full text for execute phase only), `prior_reply`.

3. Move `prior_reply: true` without resolve → `{copilot_resume_threads}` (resolve-only in Step 5, no second reply).

4. Assign sequential `id` prefixed `C1`, `C2`, …

### B — Human (when scope is `human` or `both`)

1. Parse each `{reviewers}` review body into items. Fetch inline threads from human reviewers. Optional: actionable PR conversation comments.

2. Build `{feedback_items}` — `id` prefixed `H1`, `H2`, …:

   `severity`, `source`, `thread_id`, `path`, `line`, `raw_text` (truncate in-memory to `{workflow.thread_body_max_chars}`), `reviewer`, `prior_reply`.

3. Skip items with `prior_reply: true` unless report shows `posted: no` (resume).

### C — Report and halt if empty

```text
Copilot: {X} fresh · {Y} resume-only
Human: {H} items from @alice, @bob · {S} skipped (already answered)
```

If nothing to triage and no resume threads → offer to end. **HALT**.

If only resume threads (no fresh triage) → skip Steps 3–4, go to Step 5.

## NEXT

Read fully and follow: `./step-02b-compact-feedback-index.md`
