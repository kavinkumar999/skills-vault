# BMad Artifacts — Commit, Push, Link

## The rule

```text
_bmad_output/   → symlink (BMad reads here only)
<repo_path>/    → git tracks the real files here (discover with git ls-files)
```

**Commit and push `<repo_path>`, then link those URLs in the PR body.** Never `git add _bmad_output/`.

## Steps

1. Read artifacts under `_bmad_output/` (story, sprint status, review reports).
2. Resolve each file to its git-tracked path:

   ```bash
   realpath _bmad_output/stories/foo.md
   git ls-files --full-name --error-unmatch -- "<resolved-path>"
   ```

3. Commit and push the tracked paths only:

   ```bash
   git add <tracked_repo_path>
   git commit -m "docs: add BMad artifacts [{ticket_key}]"
   git push
   ```

4. Link in the PR body using the **tracked** path:

   ```text
   https://github.com/{owner}/{repo}/blob/{head_branch}/<tracked_repo_path>
   ```

5. `gh pr create` or `gh pr edit` — artifacts must be on the remote **before** publish.

## Commit message

- PR exists: `docs: add BMad artifacts for PR #{pr_number} [{ticket_key}]`
- No PR yet: `docs: add BMad artifacts [{ticket_key}]`

## Verify after push

```bash
gh api repos/{owner}/{repo}/contents/<tracked_repo_path>?ref={head_branch} --jq .html_url
```

If `git ls-files` fails, the file is not tracked — use `uncommitted_artifacts` fallback.
