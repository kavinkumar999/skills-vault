---
---

# Step 2: Gather Context — Diff, Commits, Story, Evidence

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Every claim in the description must trace back to something gathered here
- Large diffs: read changed hunks, not whole files — subagents may parallel-read when many files changed

## INSTRUCTIONS

1. **Diff and commits:**

   ```bash
   gh pr diff {pr_number}            # or: git diff {base_branch}...HEAD when creating
   gh pr view {pr_number} --json commits
   git log {base_branch}..HEAD --oneline
   ```

   Build `{change_summary}`: changed files with per-file one-liners (what changed and why it matters), grouped by area (src, tests, config, docs). Note adds/deletes/renames and any migration or breaking change.

2. **Story context (BMad integration):**

   - Search `{implementation_artifacts}` for the story file matching this branch/PR — match on branch name, story ID in branch or commits, or most recent `in progress` story in sprint status.
   - If found, set `{story_file}` and extract: story title, acceptance criteria (with IDs), tasks, and any dev notes.
   - If none found, note it — the AC mapping section will be omitted and `{story_file}` left empty. Do not guess ACs.

3. **Ticket linkage (required):**

   - Extract `{ticket_key}` by matching `{workflow.ticket_pattern}` (e.g. `NCC-1234`) against the branch name, then commit messages, then the story file.
   - If nothing matches, ask the user once: *Which Jira ticket does this PR belong to? (pattern: {workflow.ticket_pattern})* — **HALT** until answered. The key is mandatory: it goes in the PR title and every commit this run creates.

4. **Repo PR template:**

   - Look for the repo's own template: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/pull_request_template.md`, `PULL_REQUEST_TEMPLATE.md`, or `docs/PULL_REQUEST_TEMPLATE.md` (also the `.github/PULL_REQUEST_TEMPLATE/` directory — if it holds multiple templates, ask which applies).
   - If found and `{workflow.respect_repo_template}` is true, set `{repo_template}` — Step 3 maps generated content into **its** headings and checkboxes instead of imposing `{workflow.sections}` order.

5. **Secrets pre-flight** (when `{workflow.secrets_scan}` is true):

   - Scan the **diff** (added lines only) for credential patterns: private key blocks (`-----BEGIN ... PRIVATE KEY`), AWS-style keys (`AKIA[0-9A-Z]{16}`), generic tokens/secrets (`(api[_-]?key|secret|token|password)\s*[:=]\s*['"][^'"]{8,}`), bearer/JWT-looking strings, `.env`-style assignments in newly added files — plus every regex in `{workflow.secrets_patterns}`.
   - **Any hit → HALT.** Show file:line and the matched pattern (mask the value itself). Do not draft or publish until the user removes the secret or explicitly confirms a false positive (record which in the report). A removed-but-pushed secret must be rotated — say so.
   - Clean scan → the checklist item "No secrets…" may be pre-checked as **verified**.

6. **Risk signals** (feeds the conditional `risk_rollback` section):

   - Flag: schema/data migrations, config or environment changes, feature-flag changes, dependency major bumps, public API signature changes, auth/permission logic, anything touching deploy scripts.
   - Record `{risk_signals}` with file references. Empty list → the section is omitted.

7. **Structural-change detection** (feeds the conditional `diagram` section):

   - If the change introduces or alters a flow across components — new service/API call, event producer/consumer, queue, schema relationship, multi-module call chain — record `{diagram_worthy}: true` with the participants. A localized change (few files, one module) → `false`, no diagram.

8. **Test evidence** — build structured `{test_gates}`, not prose:

   - Each gate is `{name, command, result: pass|fail, detail}` — `name` is a short label (task or check name, not the full command line), `detail` carries counts ("13 tests, 0 failed", "0 matches", "clean").
   - If `{workflow.test_command}` is non-empty: run it and parse per-suite counts from the runner's output or result files (e.g. Gradle/Surefire XML `tests=/failures=/errors=`). On failure, tell the user — a failing gate goes into the description only as an honest ❌ row if the user insists on proceeding.
   - If empty: run the project's obvious targeted tests for the changed modules when the build tool makes that evident (e.g. `:module:test`); otherwise fall back to CI:

     ```bash
     gh pr checks {pr_number}
     ```

     Use only **conclusive** check results (pass/fail) as gates. **Never snapshot pending CI as evidence** — pending states go stale the moment CI finishes; the rendered section links to the PR's Checks tab instead.
   - Capture `{evidence_raw}`: a short tail (≤ ~30 lines) of the actual runner output — per-suite count lines and the final BUILD/summary line — with the run date. This becomes the collapsible proof block; never fabricate it.

9. **Screenshots / artifacts:**

   - If the change is UI-facing, ask the user for screenshot paths or URLs to embed (one short question). Otherwise plan to omit the screenshots section.

10. **BMad artifacts (commit in output repo, link via origin):**

   - Collect candidate files: `{story_file}` (always, when found) plus every match of `{workflow.artifact_sources}` resolved under `{implementation_artifacts}` (substitute `{pr_number}` and `{story_id}` in the globs; skip patterns that match nothing). **Exclude this skill's own describe report** (`pr-{pr_number}-describe.md`) from the candidates — it is written in Step 5 *after* this classification, so linking it is circular (it is just a copy of the PR body).
   - **Resolve the artifacts git repo** (do this before classifying files):
     - Follow `{implementation_artifacts}` through any symlink to `{artifacts_repo_root}` (`readlink` / `realpath`).
     - Resolve both git toplevels and compare them — a folder inside the PR repo is *also* a git work tree, so "is it a git repo" is **not** the test; "is it a **different** repo" is:
       - `{artifacts_toplevel}` = `git -C {artifacts_repo_root} rev-parse --show-toplevel` (empty/error → the artifacts path is not under git at all; treat as untrackable and fall through to the `false` branch)
       - `{pr_toplevel}` = `git -C {project-root} rev-parse --show-toplevel`
     - **External** — `{artifacts_toplevel}` is non-empty and **differs from** `{pr_toplevel}`. Set `{artifacts_external_repo}: true` and resolve:
       - `{artifacts_remote_url}` = `git -C {artifacts_toplevel} remote get-url origin` (HALT and ask if missing — artifacts cannot be linked without a remote)
       - `{artifacts_owner}`, `{artifacts_repo}` — parse from the GitHub SSH/HTTPS origin
       - `{artifacts_branch}` = current branch in that repo (`git -C {artifacts_toplevel} branch --show-current`)
       - `{artifacts_commit_target}` = `{artifacts_toplevel}` — all commits and pushes for BMad artifacts happen **here**, not on the PR branch
     - **Not external** — `{artifacts_toplevel}` is empty or **equals** `{pr_toplevel}` (plain folder inside the PR repo). Set `{artifacts_external_repo}: false` and `{artifacts_commit_target}` = the PR repo root — links use `{owner}/{repo}` and `{head_branch}` as before.
   - When `{workflow.commit_artifacts}` is true, classify each artifact path (always relative to `{artifacts_repo_root}` when external, else relative to the PR repo):
     - **Already committed and pushed** — clean `git status` in `{artifacts_commit_target}` **and** the commit is on origin (`git -C {artifacts_commit_target} status -sb` shows no "ahead" count for the branch). A clean tree with un-pushed local commits is **not** linkable yet → treat as "new or modified". When confirmed pushed → nothing to do; link directly.
     - **New or modified** → add to `{artifacts_to_commit}` with `repo_path` = path relative to `{artifacts_commit_target}` (dry-check with `git -C {artifacts_commit_target} add --dry-run`; do **not** commit or push yet — Step 5 after approval).
     - **Untrackable** in `{artifacts_commit_target}` (`git check-ignore -v`, or outside that work tree) → resolve per `{workflow.uncommitted_artifacts}` (`embed` / `mention` / `skip`). Tell the user which file failed and why.
   - **Secrets scan the artifact contents** (when `{workflow.secrets_scan}` is true): before finalizing `{artifacts_to_commit}`, scan the **full contents** of each file to be committed (not just a diff) with the same patterns as item 5, plus `{workflow.secrets_patterns}`. Artifacts are pushed verbatim to the output repo — which is frequently more visible than the PR branch — so a secret pasted into a story file or review note leaks on push. **Any hit → HALT** with `file:line` and the masked match; do not draft or push until the user removes it or confirms a false positive (record which in the report). This gate is independent of the diff scan — a clean diff does not clear the artifacts.
   - Build `{bmad_artifacts}`: `name`, `repo_path`, `attach_as: link | embed | mention`, `pending_commit: true/false`.
   - **Link URLs** (deterministic once `{artifacts_branch}` / `{head_branch}` is known):
     - External repo: `https://github.com/{artifacts_owner}/{artifacts_repo}/blob/{artifacts_branch}/<repo_path>` per file
     - PR repo: `https://github.com/{owner}/{repo}/blob/{head_branch}/<repo_path>` per file
     - Tree link for "all BMad output": the `{implementation_artifacts}` folder in the output repo — `https://github.com/{artifacts_owner}/{artifacts_repo}/tree/{artifacts_branch}/<relative_tree_path>` when external; PR-repo equivalent otherwise. Use the path as it appears from the output repo root (follow the symlink name only when documenting for the user; URLs always target the repo that was committed).

11. **Existing hand-written content:**

    - Split `{existing_body}` on the markers: `{preserved_before}` (above `body_marker_begin`) and `{preserved_after}` (below `body_marker_end`). Both are reproduced verbatim in Step 5.

12. **Report what was gathered** (counts, ticket key, template found or not, secrets scan result, risk signals, story found or not, evidence source, artifacts found and how each attaches). If the diff is empty, **HALT** — there is nothing to describe.

## NEXT

Read fully and follow: `./step-03-draft-description.md`
