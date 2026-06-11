---
name: bmad-copilot-review-closure
description: 'Fetch unresolved GitHub Copilot PR review comments, triage fix vs defer, implement fixes or deferrals, reply on each thread, and resolve. Use when the user says "copilot review", "close copilot comments", "handle copilot feedback", or "resolve copilot PR comments"'
---

# Copilot Review Closure

**Goal:** Close the loop on unresolved **GitHub Copilot** pull-request review threads — triage each comment, get your approval, then **fix**, **defer**, or **no_action**. Every disposition ends the same way: **reply on the Copilot thread, then resolve it**. Defer means no code change — not an open thread left behind.

**Your Role:** PR hygiene engineer. You fetch Copilot threads only, validate each against the code, present a clear fix/defer recommendation, wait for explicit user decisions, then execute:
- **fix** — patch code → push → reply → resolve
- **defer** — reply with the user's defer reason → resolve (no code change)
- **no_action** — reply explaining why no change → resolve

Never leave a Copilot thread unresolved after the user has decided. Never touch human reviewer threads.

Use the `gh` CLI for all GitHub operations. Subagents may help parallel-read files during triage when many threads span large diffs.

## Conventions

- Bare paths (e.g. `references/graphql-commands.md`) resolve from the skill root.
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
- `implementation_artifacts` — base folder for the per-run closure report
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. State that this workflow processes **Copilot review threads only** and will pause for approval before any code change, reply, or resolution.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Workflow Architecture

Step-file architecture — same discipline as `bmad-code-review`:

- **Micro-file design:** One step file at a time
- **Sequential enforcement:** No skipping steps
- **Human gates:** Halt at triage presentation and before executing fixes
- **State:** Track `{pr_number}`, `{owner}`, `{repo}`, and per-thread decisions in memory
- **Report artifact:** Persist triage, decisions, and per-thread results to `{report_path}` (`{implementation_artifacts}/pr-reviews/pr-{pr_number}-copilot-closure.md`) so a crashed or interrupted run can be resumed and audited

### Step Processing Rules

1. **READ COMPLETELY** — entire step file before acting
2. **FOLLOW SEQUENCE** — sections in order
3. **WAIT FOR INPUT** — halt at checkpoints
4. **LOAD NEXT** — only when directed

### Critical Rules

- **NEVER** load multiple step files simultaneously
- **NEVER** reply to or resolve human reviewer threads
- **NEVER** push code or resolve threads without explicit user approval for that batch
- **ALWAYS** reply on the thread before resolving — **including defer and no_action** (defer closes the thread; it does not leave it open for later)
- **ALWAYS** use GraphQL thread IDs (`PRRT_…`) for reply and resolve — not REST comment IDs
- **ALWAYS** compose public PR replies in `{workflow.reply_language}` and append `{workflow.reply_marker}` — chat uses `{communication_language}`, PR threads do not
- **ALWAYS** update `{report_path}` after decisions are collected and after each thread is executed — the report is the resume point, not conversation memory

## First Step

Read fully and follow: `./steps/step-01-discover-pr.md`
