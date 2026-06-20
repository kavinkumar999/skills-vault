---
name: bmad-jira-solution-spec
description: 'Pull an assigned Jira ticket, validate it against the codebase, and produce a solution spec artifact — problem statement, root-cause analysis, proposed fix, and implementation plan — then recommend the right agent to implement. Use when the user says "analyze my Jira ticket", "what do I need to do for this ticket", "solution spec for NCC-1234", "break down this Jira issue", or "I was assigned a ticket and need a plan"'
---

# Jira Solution Spec

**Goal:** When a developer is assigned a Jira ticket, pull the ticket context **including attachments and repro/diagnostic commands**, write a **compact analysis** for review, then investigate the codebase against that plan and produce a full **solution spec** under BMad output artifacts. End with a clear **handoff** — which agent or workflow the developer should invoke to implement the fix.

**BMad artifacts:** `_bmad_output/` is a **symlink** (BMad reads here only). Git tracks the files elsewhere — commit and push those tracked paths when the user wants the spec on the branch.

**Your Role:** Ticket analyst and solution architect. Jira tells you *what* was asked; the codebase tells you *what is true*. The spec bridges both and must never invent file paths or behaviors the code does not support.

Use the **Atlassian MCP** for Jira when available (`getAccessibleAtlassianResources`, `getJiraIssue`, `searchJiraIssuesUsingJql`). Fall back to asking the user for ticket details or a paste when MCP is unavailable or unauthenticated.

## Conventions

- Bare paths (e.g. `references/jira-commands.md`) resolve from the skill root.
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
- `implementation_artifacts` — story files and the per-run solution spec live here
- `date` as system-generated current datetime
- `project_context` = `**/project-context.md` (load if exists)

**If BMad is not installed** (config file missing), you are in **standalone mode**. Read `{skill-root}/../_shared/standalone-mode.md` when that path exists; otherwise apply its defaults inline: treat `_bmad_output/` as the artifacts symlink, resolve `{user_name}` via `gh api user` when `gh` works, `{communication_language}` = English unless the user writes in another language, `{project_name}` = repo basename. Tell the user once that standalone mode is active. Skip `on_complete` script invocation at workflow end.

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`. State that you will pull the Jira ticket (with attachments and commands), produce a **compact analysis** for approval, investigate the codebase against that plan, then write the full solution spec to `_bmad_output/`.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. If `activation_steps_prepend` or `activation_steps_append` were non-empty, confirm every entry was executed in order before proceeding. Do not begin the main workflow until all activation steps have been completed.

## Workflow Architecture

Step-file architecture — same discipline as `bmad-pr-describe`:

- **Micro-file design:** One step file at a time
- **Sequential enforcement:** No skipping steps
- **Human gates:** Halt at **compact analysis** review (Step 3) and before writing the final solution spec (Step 6)
- **State:** Track `{ticket_key}`, `{ticket_url}`, `{ticket_commands}`, `{attachments}`, `{attachment_summaries}`, `{compact_analysis}`, `{compact_report_path}`, `{investigation_plan}`, `{code_findings}`, `{validation}`, `{solution_spec_draft}`, `{agent_code}`, `{agent_label}`, `{agent_prompt_hint}`, `{report_path}`
- **Artifacts:**
  - Compact analysis: `_bmad_output/ticket-analysis/{ticket_key}-compact-analysis.md` (Step 3)
  - Attachments: `_bmad_output/ticket-analysis/{ticket_key}/attachments/`
  - Solution spec: `_bmad_output/ticket-analysis/{ticket_key}-solution-spec.md` (Step 6)

### Step Processing Rules

1. **READ COMPLETELY** — entire step file before acting
2. **FOLLOW SEQUENCE** — sections in order
3. **WAIT FOR INPUT** — halt at checkpoints
4. **LOAD NEXT** — only when directed

### Critical Rules

- **NEVER** write the final artifact without explicit user approval of the shown draft
- **NEVER** `git add _bmad_output/` — only the git-tracked paths from `git ls-files`
- **NEVER** claim a file, class, function, or behavior exists without reading or searching the codebase
- **NEVER** invent acceptance criteria or scope beyond what the ticket and code support — flag gaps explicitly
- **ALWAYS** download and summarize Jira **attachments** — extract commands from description, comments, and attachment text
- **ALWAYS** produce a **compact analysis** and get user approval before codebase investigation
- **ALWAYS** drive Step 4 investigation from `{investigation_plan}` in the compact analysis
- **ALWAYS** distinguish **ticket claims** (what Jira says) from **code reality** (what you verified) — use a validation table; cite attachment and command evidence in the chain
- **ALWAYS** end with a **recommended agent / next step** from `{workflow.agent_routes}` — the developer must know what to invoke next
- **ALWAYS** compose artifacts in `{workflow.document_language}` — chat uses `{communication_language}`, artifacts do not
- **ALWAYS** update `{compact_report_path}` after Step 3 and `{report_path}` after Step 6 approval

See `references/example-run.md`, `references/compact-analysis-template.md`, `references/solution-spec-template.md`, and `../_shared/token-budget.md`.

## First Step

Read fully and follow: `./steps/step-01-discover-ticket.md`
