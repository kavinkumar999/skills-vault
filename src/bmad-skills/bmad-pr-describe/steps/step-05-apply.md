---
---

# Step 5: Apply — Publish the Description

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Apply the approved draft — only edit allowed: swap in verified artifact URLs after push
- **Order:** commit + push tracked artifacts → link in body → create or update PR
- Update `{report_path}` after publishing

## INSTRUCTIONS

See `references/artifact-commit-flow.md`.

### Phase A0 — Commit and push (tracked paths only)

When `{artifacts_to_commit}` is non-empty:

```bash
git add <tracked_repo_path>   # from git ls-files — NOT _bmad_output/
git commit -m "docs: add BMad artifacts [{ticket_key}]"
git push
```

Never `git add` the symlink folder. Record `{artifact_commit_sha}`.

### Phase A0b — Verify links (spot-check)

```bash
gh api repos/{owner}/{repo}/contents/<repo_path>?ref={head_branch} --jq .html_url
```

Patch the approved body's `bmad_artifacts` links if needed → `{body_to_publish}`.

### Phase A — Create or update PR

**Existing PR:**

```bash
gh pr edit {pr_number} --body-file <{body_to_publish}>
gh pr edit {pr_number} --title "{pr_title}"   # when title changed
```

**New PR (`{create_pr}: true`)** — only after A0 when artifacts were pending:

```bash
gh pr create --draft --base {base_branch} --title "{pr_title}" --body-file <{body_to_publish}>
```

Set `{pr_number}`, `{pr_url}` from output; rename `{report_path}` to use the PR number.

### Phase B — Verify

```bash
gh pr view {pr_number} --json body
```

Confirm body matches `{body_to_publish}` and artifact links resolve.

### Phase C — Report

Write `{report_path}` with mode (`refresh` | `created_pr`), `{artifact_commit_sha}`, artifact paths, and published body verbatim.

### Phase D — Summary

> **PR description applied** — #{pr_number} ({pr_url})
> Artifacts: {n} linked ({artifact_commit_sha or "already on branch"})

Offer: `gh pr ready`, request reviewers, or run `bmad-pr-review-closure`.

### On Complete

If `{project-root}/_bmad/scripts/resolve_customization.py` exists, run it for `workflow.on_complete`. In standalone mode, read `on_complete` from `customize.toml`. Follow if non-empty.
