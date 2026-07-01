---
---

# Step 5: Apply — Publish the Description

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Apply exactly the approved draft — no silent post-approval edits
- If `{workflow.apply_mode}` is `"ask"`, confirm once more before touching GitHub; `"on_approval"` applies immediately
- Update `{report_path}` after publishing — it records what went live

## INSTRUCTIONS

### Phase A0 — Commit and push artifacts

When `{artifacts_to_commit}` is non-empty (approved in Step 4):

**Default-branch guard (external repo only):** when `{artifacts_external_repo}` is true and `{artifacts_branch}` is the output repo's default/shared branch (`main`/`master`, or it has branch protection), pushing BMad artifacts straight to it is a surprising side effect. Confirm with the user once before pushing — *BMad artifacts will be committed and pushed to `{artifacts_branch}` of `{artifacts_remote_url}`. Proceed?* — unless the user already approved this target explicitly in Step 4. **HALT** until confirmed.

Commit and push in **`{artifacts_commit_target}`** — the symlinked BMad output repo when `{artifacts_external_repo}` is true, otherwise the PR repo. Sync with origin first so a shared branch doesn't reject the push:

```bash
git -C "{artifacts_commit_target}" fetch origin "{artifacts_branch}"
git -C "{artifacts_commit_target}" pull --rebase origin "{artifacts_branch}"   # external/shared repo; skip if nothing to track
git -C "{artifacts_commit_target}" add <files ...>
git -C "{artifacts_commit_target}" commit -m "<rendered artifact_commit_message_template>"
git -C "{artifacts_commit_target}" push origin "{artifacts_branch}"
```

If the push is rejected (non-fast-forward), re-run the fetch+rebase and retry once; if it still fails, **stop** and tell the user — do not publish links that would 404. When `{artifacts_external_repo}` is true, verify `{artifacts_remote_url}` is set. Re-read `{artifacts_owner}`, `{artifacts_repo}`, and `{artifacts_branch}` after push if the branch was newly created.

Verify the push succeeded (`git -C "{artifacts_commit_target}" status` clean, branch up to date with remote — **not** merely committed locally). If it fails, **stop** — do not publish a body whose artifact links would 404. Spot-check one link target exists:

```bash
gh api "repos/{artifacts_owner}/{artifacts_repo}/contents/<repo_path>?ref={artifacts_branch}" --jq .name
```

(Use `{owner}/{repo}` and `{head_branch}` when `{artifacts_external_repo}` is false.)

If git refuses to track a file in `{artifacts_commit_target}`, downgrade that row per `{workflow.uncommitted_artifacts}` (`embed`/`mention`/`skip`), adjust the body, and tell the user.

### Phase A — Publish

**Existing PR:**

```bash
gh pr edit {pr_number} --body-file <tempfile with approved body>
gh pr edit {pr_number} --title "{pr_title}"        # when the title changed (approved in Step 4)
```

Use `--body-file` (not `--body`) so markdown, markers, and quoting survive intact.

**New PR (`{create_pr}: true`):**

```bash
gh pr create --draft --base {base_branch} --title "{pr_title}" --body-file <tempfile>
```

`{pr_title}` is the Step 4-approved title — it always contains `{ticket_key}`. Set `{pr_number}` and `{pr_url}` from the output and rename `{report_path}` to use the real PR number.

### Phase B — Verify

```bash
gh pr view {pr_number} --json body
```

Confirm the published body matches the approved draft (markers present, preserved content intact). On mismatch, report and retry once before asking the user.

### Phase C — Write the report

Create or update `{report_path}` (make the `pr-reviews/` directory if needed):

```markdown
# PR Describe — PR #{pr_number}

- PR: {pr_url}
- Title: {pr_title}
- Ticket: {ticket_key}
- Run: {date}
- Mode: first_run | refresh | created_pr
- Story: {story_file or "none"}
- Evidence source: test_command | gh pr checks | pending
- Secrets scan: clean | confirmed false positives: <list> | skipped
- Status: applied

## Published body

<the approved body, verbatim>
```

### Phase D — Completion summary

> **PR description applied**
>
> - PR: #{pr_number} ({pr_url})
> - Sections: {list rendered}
> - ACs mapped: {n}/{total} (story: {story_file or "none"})
> - Evidence: {source}
> - Artifacts: {n} linked ({m} committed in {sha} to {artifacts_remote_url or PR origin}), {k} fallback

Offer next steps: mark the PR ready for review (`gh pr ready`), request reviewers, or run `bmad-copilot-review-closure` once Copilot has reviewed.

### On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.
