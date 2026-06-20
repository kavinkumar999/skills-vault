---
name: bmad-pr-describe
description: 'Generate or refresh a pull request description from the diff, commits, story file, and test evidence — summary, AC mapping, checklist, BMad artifact links — then apply it after approval. Creates a draft PR when none exists. Use when the user says "describe this PR", "write the PR description", "update PR body", "create PR", or "prep PR for review"'
---

# PR Describe

**Goal:** Produce a complete, reviewer-ready **PR description** — summary, AC mapping, test evidence, checklist, and **BMad artifact links**. Refresh an existing PR body or **create a draft PR** when none exists.

**BMad artifacts:** `_bmad_output/` is a **symlink** (BMad reads here only). Git tracks the files elsewhere — commit and push those tracked paths, then link them in the PR body.

**Your Role:** PR documentation engineer. Draft from diff + story → user approves → commit/push tracked artifact paths → `gh pr create` or `gh pr edit` with working links.

Use the `gh` CLI for all GitHub operations.

## Conventions

- Bare paths (e.g. `references/github-commands.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

**If `{project-root}/_bmad/bmm/config.yaml` exists**, load it and resolve:

- `project_name`, `user_name`
- `communication_language`, `document_output_language`, `user_skill_level`
- `implementation_artifacts` — story files and the per-run describe report live here
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)

**If BMad is not installed** (config file missing), you are in **standalone mode**. Read `{skill-root}/../_shared/standalone-mode.md` when that path exists; otherwise apply its defaults inline: treat `_bmad_output/` as the artifacts symlink, resolve `{user_name}` via `gh api user`, `{communication_language}` = English unless the user writes in another language, `{project_name}` = repo basename. Tell the user once that standalone mode is active. Skip `on_complete` script invocation at workflow end.

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. State that `_bmad_output/` is the BMad artifacts symlink — commit tracked files (not the symlink), link them in the body, then create or update the PR.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Workflow Architecture

Step-file architecture — same discipline as `bmad-pr-review-closure`:

- **Micro-file design:** One step file at a time
- **Sequential enforcement:** No skipping steps
- **Human gates:** Halt at draft presentation and before applying the body (or creating a PR)
- **State:** Track `{pr_number}`, `{owner}`, `{repo}`, `{base_branch}`, `{story_file}`, `{change_digest}`, `{digest_path}`, `{create_pr}`, `{artifacts_to_commit}`, `{bmad_artifacts}`, and the draft body
- **Artifacts:**
  - Digest: `_bmad_output/pr-reviews/pr-{pr_number}-digest.md` (Step 2b — compact; Step 3 drafts from this)
  - Report: `_bmad_output/pr-reviews/pr-{pr_number}-describe.md` (Step 5 — published body audit)

### Step Processing Rules

1. **READ COMPLETELY** — entire step file before acting
2. **FOLLOW SEQUENCE** — sections in order
3. **WAIT FOR INPUT** — halt at checkpoints
4. **LOAD NEXT** — only when directed

### Critical Rules

- **NEVER** apply a PR body or create a PR without explicit user approval of the shown draft
- **NEVER** `git add _bmad_output/` — only the git-tracked paths from `git ls-files`
- **NEVER** create or update a PR until artifact files are **committed, pushed, and linked** in the body
- **NEVER** state anything in the description the diff does not support — no invented test results, no claimed coverage without evidence
- **NEVER** publish while the secrets scan has unconfirmed findings — a hit halts the workflow until removed or confirmed false positive
- **NEVER** apply a PR title or commit without `{ticket_key}` (any Jira key matching `{workflow.ticket_pattern}`, e.g. NCC-1234 or PLAT-42) — ask for the ticket if it cannot be extracted
- **ALWAYS** respect the repo's `PULL_REQUEST_TEMPLATE.md` when present — its headings and checkboxes win over `{workflow.sections}`
- **NEVER** delete hand-written content outside the `{workflow.body_marker_begin}` / `{workflow.body_marker_end}` markers — generated content lives between them; everything outside is the user's
- **ALWAYS** compose the PR body in `{workflow.reply_language}` — chat uses `{communication_language}`, the PR body does not
- **ALWAYS** map acceptance criteria to concrete changes when a story file exists — AC IDs are the vocabulary of review
- **ALWAYS** distill Step 2 into `pr-{n}-digest.md` before drafting — Step 3 uses the digest, not the raw diff (see `_shared/token-budget.md`)
- **ALWAYS** when artifacts exist: commit + push tracked paths → link in `bmad_artifacts` section → then `gh pr create` or `gh pr edit`
- **ALWAYS** update `{report_path}` after applying — the report records what was published and when

See `references/example-run.md`, `references/artifact-commit-flow.md`, and `../_shared/token-budget.md`.

## First Step

Read fully and follow: `./steps/step-01-discover-pr.md`
