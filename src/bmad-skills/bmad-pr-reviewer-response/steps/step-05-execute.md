---
---

# Step 5: Execute — Fix, Post Responses, Ready for Re-Review

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}` — but compose everything **posted to the PR** in `{workflow.reply_language}`, regardless of chat language
- Append `{workflow.reply_marker}` to **every** reply and summary body posted (invisible HTML comment — the re-run guard in Step 2 depends on it)
- Execute `{execution_plan}` in order
- **fix** work varies by `fix_kind` — see Phase A
- **Every item** gets a PR reply using `{workflow.response_template}` or `{workflow.defer_reply_template}`
- **Never** post without user approval to push (for code) or publish (for PR edits)
- Default: **reply only** on threads; resolve threads only if user explicitly requests
- If the test gate or push fails, stop and report — do not post responses for unfixed code
- Update `{report_path}` after every item — it must always reflect true PR state

## INSTRUCTIONS

### Phase A — Apply fixes (by fix_kind)

Group all `action: fix` items.

| fix_kind | Action |
| --- | --- |
| `code_change` | Edit files, run tests/lint, commit |
| `pr_description` | Draft updated body (`gh pr edit`), show diff to user before applying |
| `evidence` | Add to PR body or post as comment (CI link, test output, screenshot path) |
| `docs` | Update docs/comments, commit |
| `reply_only` | Skip repo change — response only in Phase B |

1. Implement each fix. Keep scope minimal to reviewer's concern.
2. **Test gate** (when any `code_change`/`docs`/`tests` fix was made) — resolve `{workflow.test_command}`:
   - **Non-empty:** run it. On failure, **HALT**: report the failing output, do not commit/push, do not post any response. Wait for the user.
   - **Empty:** note that no `test_command` is configured (set it in `_bmad/custom/{skill-name}.toml`) and run the project's obvious test/lint if one is evident.
3. For code/docs: commit using `{workflow.commit_message_template}` — replace `{pr_number}` and `{ticket_key}` (match `{workflow.ticket_pattern}` against branch name / commits / story file; ask the user if nothing matches); reference item ids in the body if useful.
4. **Push per `{workflow.auto_push}`:**
   - `"ask"` → ask: *Push {N} commit(s) and apply PR description update? (yes/no)* — **HALT** if not pre-approved.
   - `"always"` → push without asking (state that you are doing so). PR body edits still require explicit approval of the shown diff.
5. `git push` when approved.
6. `gh pr edit` when PR body changes are approved.

### Phase B — Post per-item responses

For **each** entry in `{execution_plan}`:

1. **Compose body** using templates — in `{workflow.reply_language}`, ending with `{workflow.reply_marker}` on its own line:

   - **fix:** `{workflow.response_template}` with `{issue}` = reviewer's concern (concise), `{resolution}` = exactly what changed (file, PR section, evidence link).
   - **defer:** `{workflow.defer_reply_template}`
   - **no_action:** `{workflow.response_template}` with resolution explaining why no change.

   Example:

   ```markdown
   **Issue:** Reviewer asked for null guard on `user.id` in `handler.ts:42`.

   **Resolution:** Added early return when `user?.id` is falsy and test `handler.test.ts` covers the branch. Pushed in abc1234.

   Ready for re-review.
   ```

2. **Post reply:**
   - `thread_id` present → `addPullRequestReviewThreadReply` (see `references/github-commands.md`)
   - No thread (review-body item) → include in Phase C summary **and** optional direct `gh pr comment` if item needs standalone visibility

3. Record: `item_id`, `posted: yes/no`, `url` if available — and **immediately update the execution table in `{report_path}`** before the next item. A crash after this point must not cause a duplicate reply on re-run.

### Phase C — Post summary comment

After all items, post one **summary** on the PR:

```bash
gh pr comment {pr_number} --body "..."
```

Table format — grouped by reviewer so each can scan their own items; compose in `{workflow.reply_language}` and end with `{workflow.reply_marker}`:

| # | Reviewer | Issue (short) | Resolution | Status |
| --- | --- | --- | --- | --- |
| 1 | @alice | Null check missing | Added guard + test | ✅ Ready |
| 2 | @alice | No test evidence in PR | Added pytest output to description | ✅ Ready |
| 4 | @bob | Large refactor suggested | Deferred to PROJ-891 | ⏸ Deferred |

Close by @-mentioning **every** reviewer whose items were addressed:

> **@alice @bob** — addressed the above. Ready for re-review when you have a moment.

**HALT** — show draft summary to user before posting unless they said post immediately.

### Phase D — Completion

> **PR reviewer response complete**
>
> - PR: #{pr_number} · Reviewers: @alice, @bob
> - Fixed: {F} (kinds: code {C}, pr_description {P}, evidence {E}, docs {D})
> - Deferred: {Def} · No action: {N}
> - Commits: {sha_list}
> - Summary comment: {comment_url}

Mark `{report_path}` status: `complete` (or `in_progress` listing unposted items if anything failed).

Offer: re-request review from each reviewer (`gh pr ready` / ping) if user wants.

### On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If non-empty, follow as final terminal instruction.
