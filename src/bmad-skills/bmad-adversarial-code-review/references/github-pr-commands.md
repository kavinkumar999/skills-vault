# GitHub PR Commands — Adversarial Code Review

PR discovery, metadata, diff/commits, and CI all use the shared mechanics in
`../_shared/github-commands.md`. This skill adds only the notes below.

## Fields this skill needs

Request `headRefOid` when resolving/inspecting the PR — the round artifacts and ledger are
keyed to the head commit so a re-review (v2, v3…) can tell whether the PR moved:

```bash
gh pr view {pr_number} --json number,url,title,body,baseRefName,headRefName,headRefOid,isDraft
```

## Read-only

This skill does **not** post comments or reviews to GitHub, and never edits the PR body.
No `gh pr edit`, no `gh pr comment`, no GraphQL mutations.
