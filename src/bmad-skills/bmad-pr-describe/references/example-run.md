# Example Run — PR Describe

## Create PR

`_bmad_output/` → symlink (BMad reads here only). Git tracks files elsewhere.

```text
User: Create PR

Agent: I'll read artifacts from _bmad_output/, commit the git-tracked paths,
       push, link them, then open a draft PR.
```

```bash
realpath _bmad_output/stories/NCC-1234-foo.md
git ls-files --full-name --error-unmatch -- <resolved-path>
# → <tracked_repo_path>

git add <tracked_repo_path>
git commit -m "docs: add BMad artifacts [NCC-1234]"
git push

gh pr create --draft --base main --title "feat(...): ... [NCC-1234]" --body-file /tmp/pr-body.md
```

PR body links use `<tracked_repo_path>`, never `_bmad_output/`.

## Refresh existing PR

If artifacts under `_bmad_output/` changed: push tracked paths first, then `gh pr edit`.
