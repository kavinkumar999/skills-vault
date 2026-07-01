---
name: bmad-pr-describe
description: 'Generate or refresh a pull request description from the diff, commits, story file, and test evidence — summary, AC mapping, checklist — then apply it after approval. Use when the user says "describe this PR", "write the PR description", "update PR body", or "prep PR for review"'
---

# PR Describe

**Goal:** Produce a complete, reviewer-ready **PR description** before review is requested — summary, what/why, acceptance-criteria mapping, test evidence, checklist — generated from the actual diff and story context, never from guesswork. Re-runs **refresh** the generated content in place; they never duplicate it or clobber hand-written sections.

**Your Role:** PR documentation engineer. You read the diff, commits, and the BMad story file (when one exists), draft the description, present it for approval, and apply it with `gh pr edit`. If the branch has no PR yet, you offer to open one (draft by default) with the generated body.

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

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `project_name`, `user_name`
- `communication_language`, `document_output_language`, `user_skill_level`
- `implementation_artifacts` — story files and the per-run describe report live here
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. State that this workflow drafts the **PR description** from the diff and story context, shows it for approval, and only then applies it to GitHub.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Workflow Architecture

Step-file architecture — same discipline as `bmad-copilot-review-closure`:

- **Micro-file design:** One step file at a time
- **Sequential enforcement:** No skipping steps
- **Human gates:** Halt at draft presentation and before applying the body (or creating a PR)
- **State:** Track `{pr_number}`, `{owner}`, `{repo}`, `{base_branch}`, `{story_file}`, `{artifacts_external_repo}`, `{artifacts_commit_target}`, `{artifacts_owner}`, `{artifacts_repo}`, `{artifacts_branch}`, `{artifacts_remote_url}`, and the draft body
- **Report artifact:** Persist the applied body and run status to `{report_path}` (`{implementation_artifacts}/pr-reviews/pr-{pr_number}-describe.md`) for audit and resume

### Step Processing Rules

1. **READ COMPLETELY** — entire step file before acting
2. **FOLLOW SEQUENCE** — sections in order
3. **WAIT FOR INPUT** — halt at checkpoints
4. **LOAD NEXT** — only when directed

### Critical Rules

- **NEVER** apply a PR body or create a PR without explicit user approval of the shown draft
- **NEVER** state anything in the description the diff does not support — no invented test results, no claimed coverage without evidence
- **NEVER** publish or push while the secrets scan has unconfirmed findings — the scan covers both the PR diff and the full contents of every artifact committed to the output repo; a hit halts the workflow until removed or confirmed false positive
- **NEVER** apply a PR title or commit without `{ticket_key}` (any Jira key matching `{workflow.ticket_pattern}`, e.g. NCC-1234 or PLAT-42) — ask for the ticket if it cannot be extracted
- **ALWAYS** respect the repo's `PULL_REQUEST_TEMPLATE.md` when present — its headings and checkboxes win over `{workflow.sections}`
- **NEVER** delete hand-written content outside the `{workflow.body_marker_begin}` / `{workflow.body_marker_end}` markers — generated content lives between them; everything outside is the user's
- **ALWAYS** compose the PR body in `{workflow.reply_language}` — chat uses `{communication_language}`, the PR body does not
- **ALWAYS** map acceptance criteria to concrete changes when a story file exists — AC IDs are the vocabulary of review
- **ALWAYS** update `{report_path}` after applying — the report records what was published and when

## First Step

Read fully and follow: `./steps/step-01-discover-pr.md`
