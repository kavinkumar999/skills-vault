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

10. **BMad artifacts (commit-and-link):**

   - Collect candidate files: `{story_file}` (always, when found) plus every match of `{workflow.artifact_sources}` resolved under `{implementation_artifacts}` (substitute `{pr_number}` and `{story_id}` in the globs; skip patterns that match nothing).
   - Resolve each path **through symlinks to its in-repo location** (`git ls-files` / the symlink target inside the repo) — the artifacts folder is typically reachable via a tracked symlink, and links must use the path git actually tracks.
   - When `{workflow.commit_artifacts}` is true, classify each artifact:
     - **Already committed and unchanged** → nothing to do; link directly.
     - **New or modified** → add to `{artifacts_to_commit}` (dry-check with `git add --dry-run`; do **not** commit or push yet — that happens in Step 5 after the user approves).
     - **Untrackable** (gitignored, outside the repo) → fall back per `{workflow.uncommitted_artifacts}` (`embed` truncated to `{workflow.embed_max_chars}`, `mention`, or `skip`) and tell the user which file and why.
   - Build `{bmad_artifacts}`: `name`, `repo_path`, `attach_as: link | embed | mention`, `pending_commit: true/false`. Link URLs are deterministic before the push: `https://github.com/{owner}/{repo}/blob/{head_branch}/<repo_path>` per file, plus one **tree URL** to the artifacts directory itself as the "all BMad output for this PR" reference.

11. **Existing hand-written content:**

    - Split `{existing_body}` on the markers: `{preserved_before}` (above `body_marker_begin`) and `{preserved_after}` (below `body_marker_end`). Both are reproduced verbatim in Step 5.

12. **Report what was gathered** (counts, ticket key, template found or not, secrets scan result, risk signals, story found or not, evidence source, artifacts found and how each attaches). If the diff is empty, **HALT** — there is nothing to describe.

## NEXT

Read fully and follow: `./step-03-draft-description.md`
