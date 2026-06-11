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

```bash
git add <artifact files>
git commit -m "<rendered artifact_commit_message_template>"   # includes {ticket_key} — e.g. "docs: add BMad artifacts for PR #42 [NCC-1234]"
git push
```

Verify the push succeeded (`git status` clean, branch up to date with remote). If it fails, **stop** — do not publish a body whose artifact links would 404. After pushing, spot-check one link target exists:

```bash
gh api repos/{owner}/{repo}/contents/<repo_path>?ref={head_branch} --jq .name
```

If git refuses a file (ignored path), downgrade that row per `{workflow.uncommitted_artifacts}`, adjust the body, and tell the user.

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
> - Artifacts: {n} linked ({m} committed in {sha}), {k} fallback

Offer next steps: mark the PR ready for review (`gh pr ready`), request reviewers, or run `bmad-copilot-review-closure` once Copilot has reviewed.

### On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.
