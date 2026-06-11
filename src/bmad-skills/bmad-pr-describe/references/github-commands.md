# GitHub Commands for PR Describe

All operations via `gh` CLI.

## Prerequisites

```bash
gh auth status
```

## Resolve the PR for the current branch

```bash
gh pr view --json number,url,title,body,baseRefName,headRefName,isDraft,baseRepository,headRepositoryOwner
```

Exit code non-zero with "no pull requests found" → branch has no PR (see `create_if_missing`).

## Read the diff and commits

```bash
gh pr diff {pr_number}                       # full diff of the PR
git diff {base_branch}...HEAD                # when no PR exists yet
gh pr view {pr_number} --json commits
git log {base_branch}..HEAD --oneline
git diff {base_branch}...HEAD --stat         # quick file/areas overview
```

## Test evidence

```bash
gh pr checks {pr_number}                     # CI check results (latest run)
```

Prefer `{workflow.test_command}` output when configured; `gh pr checks` is the fallback. Never report evidence you did not see.

## Apply the description

```bash
gh pr edit {pr_number} --body-file /tmp/pr-body.md
```

Always `--body-file` — inline `--body` mangles quoting and multi-line markdown.

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
