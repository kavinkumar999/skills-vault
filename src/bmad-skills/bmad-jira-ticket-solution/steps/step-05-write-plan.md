---
---

# Step 5: Write the Plan

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Write exactly the approved plan — no silent post-approval edits
- If `{workflow.apply_mode}` is `"ask"`, confirm once more before writing; `"on_approval"` writes immediately
- Read-only contract still holds: the plan file is the only thing this skill creates — no product-code edits, no fix commits, no PR

## INSTRUCTIONS

### Phase A — Resolve the output location

1. Resolve the plan path: `{plan_path}` = `{planning_artifacts}` + (`{workflow.plan_output_subdir}` if non-empty) + `/` + `{workflow.plan_filename_template}` with `{ticket_key}`/`{date}` substituted.
2. **Resolve the output git repo** (same model as `bmad-pr-describe`): follow `{planning_artifacts}` through any symlink to `{artifacts_repo_root}` (`readlink -f` / `realpath`).
   - If `{artifacts_repo_root}` is a git work tree, set `{artifacts_external_repo}: true` and resolve `{artifacts_remote_url}` (`git -C … remote get-url origin`), `{artifacts_owner}`/`{artifacts_repo}` (parsed from origin), `{artifacts_branch}` (`git -C … branch --show-current`), and `{artifacts_commit_target}` = `{artifacts_repo_root}`.
   - Otherwise set `{artifacts_external_repo}: false` and `{artifacts_commit_target}` = the repo the plan path lives in (if any).

### Phase B — Write the plan file

Write `{plan}` to `{plan_path}` (create parent directories if needed). Confirm the file was written and report its path.

### Phase C — Commit (per `{workflow.commit_plan}`)

Skip this phase entirely when `commit_plan = "never"` or the plan path is not inside a git work tree (tell the user it was written locally only).

When `commit_plan` is `"ask"`, confirm once: *Commit the plan to `{artifacts_branch}` of `{artifacts_remote_url}`?* — **HALT** until answered. `"always"` proceeds without the extra prompt.

**Default-branch guard (external repo):** when `{artifacts_external_repo}` is true and `{artifacts_branch}` is the output repo's default/shared branch (`main`/`master` or protected), confirm before pushing — committing a plan straight to a shared branch is a side effect. **HALT** until confirmed.

Sync, commit, and push in the resolved target:

```bash
git -C "{artifacts_commit_target}" fetch origin "{artifacts_branch}"
git -C "{artifacts_commit_target}" pull --rebase origin "{artifacts_branch}"   # shared repo; skip if nothing to track
git -C "{artifacts_commit_target}" add "<plan path relative to commit target>"
git -C "{artifacts_commit_target}" commit -m "<rendered plan_commit_message_template>"   # includes {ticket_key}
git -C "{artifacts_commit_target}" push origin "{artifacts_branch}"
```

If the push is rejected (non-fast-forward), re-run fetch+rebase and retry once; if it still fails, stop and tell the user the plan is written and committed locally but not pushed. After a successful push, the plan link is `https://github.com/{artifacts_owner}/{artifacts_repo}/blob/{artifacts_branch}/<repo_path>` (external) or the PR-repo equivalent — spot-check it:

```bash
gh api "repos/{artifacts_owner}/{artifacts_repo}/contents/<repo_path>?ref={artifacts_branch}" --jq .name
```

### Phase D — Optional Jira write-back

Only when `{workflow.write_back_jira}` is true: offer to post a short solution summary (problem + approach + a link to the committed plan) as a comment on `{ticket_key}` via the Atlassian MCP (`addCommentToJiraIssue`). **HALT** for approval before posting. Default config is `false` — skip silently.

### Phase E — Completion summary

> **Solution plan ready**
>
> - Ticket: {ticket_key} — {summary}
> - Plan: `{plan_path}` ({committed to {artifacts_branch} / local only})
> - Link: {plan link or "not pushed"}
> - Root cause: {confirmed | ranked — confidence}
> - Open questions: {n}

Offer next steps: implement with **`{workflow.handoff_skill}`** (pass the plan path), or refine the plan further. Do not start implementation from this skill.

### On Complete

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete`

If the resolved `workflow.on_complete` is non-empty, follow it as the final terminal instruction before exiting.
