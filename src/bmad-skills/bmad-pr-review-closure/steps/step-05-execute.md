---
---

# Step 5: Execute — Fix, Reply, Close

## RULES

- Chat in `{communication_language}`; PR posts in `{workflow.reply_language}` + `{workflow.reply_marker}`
- Process `{execution_plan}` in order
- Test gate before push when code/docs fixes exist
- Update `{report_path}` after every item

## INSTRUCTIONS

### Phase A — Apply fixes (batch)

All `action: fix` items:

**Copilot:** minimal code change; `apply_suggestion: true` → apply `suggestion_block` verbatim.

**Human by `fix_kind`:**

| fix_kind | Action |
| --- | --- |
| `code_change` | Edit source/tests, commit |
| `pr_description` | Draft body diff → user approves → `gh pr edit` |
| `evidence` | Add to PR body or comment |
| `docs` | Edit docs, commit |
| `reply_only` | No repo change |

Run `{workflow.test_command}` when non-empty; **HALT** on failure.

Before committing, set `{ticket_key}` by matching `{workflow.ticket_pattern}` against the branch name, then commit messages, then the PR title/body — use the first match. Commit with `{workflow.commit_message_template}` (substitute `{pr_number}` and `{ticket_key}`); if no ticket key is found, drop the trailing `[{ticket_key}]` segment rather than committing an empty `[]`. Push per `{workflow.auto_push}`.

### Phase B — Reply (per plan entry)

**Copilot** (`source: copilot`):

- **fix:** `{workflow.copilot_fix_reply_template}` + `{summary}`
- **defer:** `{workflow.copilot_defer_reply_template}` + `{reason}`
- **no_action:** explain why
- **resolve_only:** skip reply
- GraphQL reply → **always** `resolveReviewThread`

**Human** (`source: human`):

- **fix/defer/no_action:** `{workflow.human_response_template}` or `{workflow.human_defer_reply_template}`
- Post via `addPullRequestReviewThreadReply` when `thread_id` set; else include in Phase C summary
- Resolve thread only if user chose yes in Step 4 or `{workflow.human_resolve_threads}` is `always`

See `references/github-pr-commands.md`.

### Phase C — Human summary comment (when scope includes human and items were addressed)

Draft table grouped by reviewer; @-mention reviewers. **HALT** for approval unless user said post immediately.

```bash
gh pr comment {pr_number} --body "..."
```

### Phase D — Verify and complete

Re-count unresolved Copilot threads (if copilot scope). Mark `{report_path}` `complete` or `in_progress`.

> **PR review closure complete**
> - PR #{pr_number} · Scope: {review_scope}
> - Copilot: fixed {F} · deferred {D} · remaining {R}
> - Human: fixed {HF} · summary comment {url}

Offer: `gh pr ready`, re-request review, or `bmad-pr-describe` to refresh PR body.

### On Complete

Run `resolve_customization.py` for `workflow.on_complete` when BMad present; else read from `customize.toml`.
