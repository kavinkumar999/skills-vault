---
---

# Step 5: Execute — Fix, Reply, Resolve

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}` — but compose everything **posted to the PR** in `{workflow.reply_language}`, regardless of chat language
- Append `{workflow.reply_marker}` to **every** reply body posted (it is an invisible HTML comment — the re-run guard in Step 2 depends on it)
- Process `{execution_plan}` in order
- For **fix**: implement code change → test gate → commit → push → reply → resolve
- For **defer**: **reply with reason** (use `{workflow.defer_reply_template}`) → **resolve** — no code change, but the thread is **closed** on the PR
- For **no_action**: reply explaining why no change → resolve
- For **resolve_only** (resume entries): resolve **without replying** — a reply from a prior run is already on the thread
- **Defer is not "skip"** — deferred threads still get a public reply and are resolved like fixes
- **Never** resolve without a reply on the thread (yours from this run, or a prior-run reply for resolve_only)
- **Never** leave a deferred thread unresolved
- If the test gate or push fails, stop and report — do not resolve threads for unfixed code
- Update `{report_path}` after every thread — it must always reflect true PR state

## INSTRUCTIONS

### Phase A — Apply fixes (batch)

Collect all `action: fix` items.

1. Implement each fix in the codebase. Keep changes minimal and scoped to Copilot's concern.
   - `apply_suggestion: true` → apply the thread's `suggestion_block` **verbatim** at `path:line` (replace the lines the suggestion targets). Do not re-derive the edit from the comment prose.
   - `apply_suggestion: false` (or no block) → implement per `suggested_change`.
   - If a suggestion block no longer applies cleanly (context drifted since triage), fall back to a manual edit and note it.

2. **Test gate** — resolve `{workflow.test_command}`:
   - **Non-empty:** run it. On failure, **HALT**: report the failing output, do not commit/push, do not reply to or resolve any thread. Wait for the user (fix forward, drop an item, or override explicitly).
   - **Empty:** note to the user that no `test_command` is configured (set it in `_bmad/custom/{skill-name}.toml`) and run the project's obvious test/lint if one is evident.

3. Stage and commit using `{workflow.commit_message_template}` — replace `{pr_number}` and `{ticket_key}` (match `{workflow.ticket_pattern}` against branch name / commits / story file; ask the user if nothing matches):

   ```bash
   git add <files>
   git commit -m "<rendered commit_message_template>"
   ```

4. **Push per `{workflow.auto_push}`:**
   - `"ask"` → ask: *Ready to push {N} fix(es) to the PR branch. Push now? (yes/no)* — **HALT** if not pre-approved.
   - `"always"` → push without asking (state that you are doing so).

   ```bash
   git push
   ```

### Phase B — Reply and resolve (per thread)

For **each** entry in `{execution_plan}` (fixes, defers, no_action, resolve_only):

1. **Compose reply body** — in `{workflow.reply_language}`, ending with `{workflow.reply_marker}` on its own line:

   - **fix:** Use `{workflow.fix_reply_template}` with `{summary}` = what changed (file + brief description). Mention commit if pushed.
   - **defer:** Use `{workflow.defer_reply_template}` with `{reason}` = user-confirmed defer reason. Be specific about what blocks the fix and when it might be revisited. Example: `Deferred for now: waiting on platform API schema v2 — will address in follow-up PR #456.` Then **always** call `resolveReviewThread` — defer still closes the thread.
   - **no_action:** Explain clearly why the suggestion is not applied (incorrect, already handled, out of scope, style preference documented elsewhere).
   - **resolve_only:** Skip composition entirely — do not post a second reply.

2. **Post reply** via GraphQL `addPullRequestReviewThreadReply` (see `references/graphql-commands.md`) — skipped for `resolve_only`:

   ```bash
   gh api graphql -f query='...' -f threadId="PRRT_..." -f body="..."
   ```

3. **Resolve thread** via `resolveReviewThread`:

   ```bash
   gh api graphql -f query='...' -f threadId="PRRT_..."
   ```

4. Record result: `replied: yes`, `resolved: yes/no`, `error: ...` — and **immediately update the execution table in `{report_path}`** before moving to the next thread.

If reply succeeds but resolve fails, report the thread ID and continue with remaining threads — the report row (`replied: yes, resolved: no`) is what lets the next run finish it without double-posting.

### Phase C — Verify

Re-fetch unresolved Copilot threads. Report:

| Metric | Count |
| --- | --- |
| Fixed + resolved | |
| Deferred + resolved | |
| No-action + resolved | |
| Resume-only resolved | |
| Remaining unresolved Copilot | |

Mark `{report_path}` status: `complete` if nothing remains, otherwise `in_progress` with the remaining thread IDs listed.

### Phase D — Completion summary

> **Copilot review closure complete**
>
> - PR: #{pr_number} ({pr_url})
> - Fixed: {F} (commit: {sha} if pushed)
> - Deferred: {D}
> - No action: {N}
> - Remaining unresolved Copilot threads: {R}

If `{R} > 0`, list them and offer to re-run the workflow.

### On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.
