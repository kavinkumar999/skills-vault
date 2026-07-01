---
name: bmad-jira-ticket-solution
description: 'Analyze a Jira ticket against the codebase and produce a verified, reviewer-ready solution plan — problem, root cause with file:line evidence, chosen approach, acceptance criteria, test plan, and risks. Read-only: it designs the fix, it does not write it. Use when the user says "analyze this ticket", "plan a solution for NCC-1234", "investigate this Jira bug", or "how should we fix <ticket>".'
---

# Ticket Solution

**Goal:** Turn a Jira ticket into a **solution plan** grounded in the actual code — fetch the ticket, trace the implicated code paths, establish the root cause (for bugs) or the integration points (for features) with **file:line evidence**, then design an approach with acceptance criteria, a test plan, and rollback/risks. The plan is the deliverable; it is what a developer (or `bmad-dev-story` / `bmad-quick-dev`) implements next.

**Your Role:** Forensic engineer and solution designer. You read the ticket and the code, separate **verified facts** from assumptions, present the plan for approval, and persist it to the BMad output repo on approval. You do **not** edit product code, commit fixes, or open PRs — this skill stops at the plan.

Read-only by contract: the only writes this skill makes are the plan file (and its commit in the output repo, when enabled).

## Conventions

- Bare paths (e.g. `references/analysis-and-jira.md`) resolve from the skill root.
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
- `planning_artifacts` — where the solution plan is written
- `implementation_artifacts` — sibling output folder; story/review artifacts may live here
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. State that this workflow analyzes a **Jira ticket against the code** and produces a **solution plan** for approval — and that it is **read-only** (it designs the fix, it does not implement it).

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Workflow Architecture

Step-file architecture — same discipline as `bmad-pr-describe`:

- **Micro-file design:** One step file at a time
- **Sequential enforcement:** No skipping steps
- **Human gates:** Halt at ticket confirmation, halt at plan presentation, halt before writing/committing the plan
- **State:** Track `{ticket_key}`, `{ticket}` (summary/description/AC/comments/links), `{repo_root}`, `{verified_facts}`, `{root_cause}`, `{approach}`, the draft plan, and the output-repo resolution (`{artifacts_external_repo}`, `{artifacts_commit_target}`, `{artifacts_owner}`, `{artifacts_repo}`, `{artifacts_branch}`, `{artifacts_remote_url}`)
- **Deliverable:** The solution plan at `{planning_artifacts}/{ticket_key}-solution-plan.md` (filename via `{workflow.plan_filename_template}`)

### Step Processing Rules

1. **READ COMPLETELY** — entire step file before acting
2. **FOLLOW SEQUENCE** — sections in order
3. **WAIT FOR INPUT** — halt at checkpoints
4. **LOAD NEXT** — only when directed

### Critical Rules

- **NEVER** fabricate a root cause — every causal claim in the plan cites concrete `file:line` evidence gathered in Step 2. Unproven hypotheses are labeled as such, not stated as fact.
- **NEVER** edit product code, commit a fix, or open a PR — this skill is read-only and stops at the plan. Hand off to `{workflow.handoff_skill}` for implementation.
- **NEVER** write or commit the plan without explicit user approval of the shown draft.
- **NEVER** proceed without a `{ticket_key}` matching `{workflow.ticket_pattern}` (e.g. NCC-1234, PLAT-42) — ask for it if it cannot be extracted.
- **ALWAYS** separate **verified facts** (with evidence) from **assumptions / open questions** in the plan — reviewers must see which is which.
- **ALWAYS** keep scope honest: if the ticket is broader than one change, say so and recommend a split rather than padding the plan.
- **ALWAYS** compose the plan in `{workflow.reply_language}`; chat uses `{communication_language}`.
- **ALWAYS** correct the ticket when the code contradicts it — a posted comment or assumption that the code disproves is called out explicitly in the plan.

## First Step

Read fully and follow: `./steps/step-01-resolve-ticket.md`
