---
name: bmad-pr-reviewer-response
description: 'Pull latest human PR reviewer feedback (blockers and recommendations), validate against code and PR context, wait for user decisions, then fix code or PR metadata and post side-by-side responses. Use when the user says "address reviewer feedback", "PR blocking comments", "respond to PR review", or "fix reviewer recommendations before approve"'
---

# PR Reviewer Response

**Goal:** Close the loop on **human reviewer** feedback before approval — pull the latest review comments (blockers + recommendations), validate each against the code and PR, get your explicit decisions, then execute fixes and post clear **problem → solution** replies.

**Your Role:** PR response engineer. You work **human reviewer feedback only** — never Copilot or bot threads (use `bmad-copilot-review-closure` for those). Reviewer input may require more than code: PR description updates, evidence, screenshots, test output, or docs. After each fix, post a response that states what was wrong and what you did.

**Disposition → execute → respond:**

| User decision | Typical work | Response |
| --- | --- | --- |
| **fix** | Code, tests, config, or PR body per item type | Reply on thread + problem/solution summary |
| **defer** | No change now | Reply with defer reason on thread |
| **no_action** | Push back with rationale | Reply explaining why no change |
| **evidence** | Add proof (logs, screenshot path, test output) to PR | Reply linking or pasting evidence |

Every addressed item gets a **public reply** on the PR (inline thread reply or review comment as appropriate). Defer and no_action still get replies — do not leave reviewer questions unanswered.

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
- `implementation_artifacts` — base folder for the per-run response report
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. State that this workflow addresses **human reviewer** feedback, pauses for approval before changes, and posts **problem + solution** replies when done.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Workflow Architecture

Step-file architecture — same discipline as `bmad-copilot-review-closure`:

- **Micro-file design:** One step file at a time
- **Sequential enforcement:** No skipping steps
- **Human gates:** Halt at triage presentation and before executing changes
- **State:** Track `{pr_number}`, `{owner}`, `{repo}`, `{reviewers}` (one or more human reviewers), and per-item decisions
- **Report artifact:** Persist triage, decisions, and per-item results to `{report_path}` (`{implementation_artifacts}/pr-reviews/pr-{pr_number}-reviewer-response.md`) so a crashed or interrupted run can be resumed and audited

### Critical Rules

- **NEVER** load multiple step files simultaneously
- **NEVER** process Copilot or bot-authored threads — exclude logins in `{workflow.excluded_author_logins}`
- **NEVER** push or post responses without explicit user approval for that batch
- **ALWAYS** validate feedback against actual code and PR context before recommending fix
- **ALWAYS** post a reply after executing (or deferring) each item — format: **Issue** / **Resolution**
- **ALWAYS** use GraphQL thread IDs (`PRRT_…`) for inline thread replies
- **ALWAYS** compose public PR posts in `{workflow.reply_language}` and append `{workflow.reply_marker}` — chat uses `{communication_language}`, PR posts do not
- **ALWAYS** update `{report_path}` after decisions are collected and after each item is executed — the report is the resume point, not conversation memory

## First Step

Read fully and follow: `./steps/step-01-discover-pr.md`
