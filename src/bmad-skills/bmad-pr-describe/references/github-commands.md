# GitHub Commands for PR Describe

All operations via `gh` CLI. Shared mechanics — auth, PR resolution, diff/commits/CI, and
the `gh pr edit --body-file` contract — live in `../_shared/github-commands.md`. This file
covers only what PR Describe adds on top.

## Resolve the PR (extra fields PR Describe needs)

```bash
gh pr view --json number,url,title,body,baseRefName,headRefName,isDraft,baseRepository,headRepositoryOwner
```

`baseRepository` / `headRepositoryOwner` are needed for cross-fork blob links in the body.
Non-zero exit + "no pull requests found" → branch has no PR (see `create_if_missing`).

## Test evidence

Prefer `{workflow.test_command}` output when configured; `gh pr checks {pr_number}` is the
fallback (shared file). Never report evidence you did not see.

## Create a draft PR (when none exists)

```bash
gh pr create --draft --base {base_branch} --title "..." --body-file /tmp/pr-body.md
```

## Verify

```bash
gh pr view {pr_number} --json body
```

Check that `{workflow.body_marker_begin}` and `{workflow.body_marker_end}` are present and hand-written content outside them is intact.

## Marker contract

The generated block always sits between the markers:

```markdown
<!-- bmad-pr-describe:begin -->
... generated sections ...
<!-- bmad-pr-describe:end -->
```

- Refresh runs replace **only** what is between the markers.
- Content above/below the markers is hand-written — reproduce verbatim.
- Markers are invisible on GitHub; do not remove them.

## Optional follow-ups

```bash
gh pr ready {pr_number}                      # flip draft → ready for review
gh pr edit {pr_number} --add-reviewer LOGIN  # request reviewers
```
