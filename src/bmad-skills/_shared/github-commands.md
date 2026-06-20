# Shared GitHub (`gh`) mechanics

Common `gh` CLI invocations used by more than one PR skill. Each skill's own
`references/github*-commands.md` keeps its skill-specific operations (GraphQL review
threads, marker contracts, draft-PR creation) and the exact `--json` field sets it needs;
this file holds the mechanics they share so the contract lives in one place.

## Prerequisite

```bash
gh auth status
```

Non-zero exit → not authenticated. HALT and tell the user to run `gh auth login`.

## Resolve / inspect the PR

```bash
# Find the open PR for the current branch (when the number isn't given)
gh pr list --head "$(git branch --show-current)" --state open \
  --json number,url,title,headRefOid,baseRefName

# Inspect a known PR — each skill requests the fields it actually uses
gh pr view {pr_number} --json number,url,title,body,baseRefName,headRefName,isDraft
```

`gh pr view` with no PR and a non-zero exit + "no pull requests found" → the branch has no
PR yet (skills that create one handle this via their own `create_if_missing` path).

## Diff, commits, and CI

```bash
gh pr diff {pr_number} --stat            # file list and churn — always cheap to run first
gh pr diff {pr_number}                   # full hunks
git diff {base_branch}...HEAD            # when no PR exists yet
gh pr view {pr_number} --json commits
git log {base_branch}..HEAD --oneline
gh pr checks {pr_number}                 # CI check results (latest run)
```

Read hunks, not whole files, on large diffs (see `_shared/token-budget.md`). Use only
**conclusive** `gh pr checks` results as evidence — never snapshot pending CI.

## Edit the PR body

```bash
gh pr edit {pr_number} --body-file /tmp/pr-body.md
```

Always `--body-file` — inline `--body` mangles quoting and multi-line markdown.
