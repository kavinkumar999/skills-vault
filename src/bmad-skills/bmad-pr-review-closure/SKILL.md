---
name: bmad-pr-review-closure
description: 'Close the loop on PR review feedback — Copilot threads and/or human reviewers. Triage fix vs defer, implement fixes, reply on each thread, resolve Copilot threads, post issue/resolution replies for humans. Use when the user says "copilot review", "close copilot comments", "address reviewer feedback", "PR blocking comments", "respond to PR review", or "resolve PR comments"'
---

# PR Review Closure

**Goal:** Close the loop on **all PR review feedback** the user selects — **Copilot** inline threads and/or **human reviewer** blockers and recommendations. Triage each item, get approval, then execute fixes and post replies. Copilot items always end with **reply + resolve**. Human items get **Issue / Resolution** replies; resolve threads only when the user asks.

**Your Role:** PR review engineer. One workflow, two sources — never mix them in a single fetch pass, but handle both in one run when `{review_scope}` is `both`.

| Source | Scope | After each item |
| --- | --- | --- |
| **Copilot** | `{workflow.copilot_author_logins}` only | Reply → **always resolve** |
| **Human** | Reviewers in `{reviewers}`, exclude bots | Reply (Issue/Resolution); resolve optional |

Use the `gh` CLI. Subagents may parallel-read files during triage on large PRs.

## Conventions

- Bare paths resolve from the skill root.
- `{skill-root}` — installed directory (`customize.toml` lives here).
- `{project-root}` — project working directory.
- `{skill-name}` — skill directory basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

**If the script fails**, merge `workflow` from `{skill-root}/customize.toml` → `{project-root}/_bmad/custom/{skill-name}.toml` → `{skill-name}.user.toml` (skip missing files; scalars override, tables deep-merge).

### Step 2–3: Prepend steps and persistent facts

Execute `{workflow.activation_steps_prepend}`. Load `{workflow.persistent_facts}` (`file:` entries → load from `{project-root}`).

### Step 4: Load Config

**If `{project-root}/_bmad/bmm/config.yaml` exists**, load `project_name`, `user_name`, `communication_language`, `document_output_language`, `user_skill_level`, `implementation_artifacts`, `date`, and `project_context` (`**/project-context.md`).

**If BMad is absent**, read `{skill-root}/../_shared/standalone-mode.md` or inline defaults (`_bmad_output/` for reports, `gh api user` for `{user_name}`). Skip `on_complete` script at workflow end.

### Step 5: Greet

Greet `{user_name}` in `{communication_language}`. State this skill handles **Copilot and/or human** PR feedback with approval gates before changes.

### Step 6: Append steps

Execute `{workflow.activation_steps_append}`.

## Workflow Architecture

- **One step file at a time** — never load multiple steps
- **Human gates** at triage presentation and before execute
- **State:** `{pr_number}`, `{owner}`, `{repo}`, `{review_scope}`, `{reviewers}`, `{feedback_index}`, `{index_path}`, `{files_to_read}`, `{copilot_threads}`, `{feedback_items}`, `{execution_plan}`, `{ticket_key}`
- **Artifacts:**
  - Index: `_bmad_output/pr-reviews/pr-{pr_number}-feedback-index.md` (Step 2b — triage from this)
  - Report: `_bmad_output/pr-reviews/pr-{pr_number}-review-closure.md` (full thread appendix + execution audit)

### Critical Rules

- **NEVER** load multiple step files simultaneously
- **NEVER** treat a Copilot thread as human feedback or vice versa
- **NEVER** push or post without explicit user approval for that batch
- **ALWAYS** reply before resolving Copilot threads (including defer and no_action)
- **ALWAYS** use GraphQL thread IDs (`PRRT_…`) for inline replies
- **ALWAYS** append `{workflow.reply_marker}` to PR posts; also treat legacy markers `<!-- bmad-copilot-closure -->` and `<!-- bmad-pr-reviewer-response -->` as prior replies
- **ALWAYS** build `pr-{n}-feedback-index.md` after fetch — triage and present from index excerpts, not full thread bodies (see `_shared/token-budget.md`)
- **ALWAYS** update `{report_path}` after decisions and after each executed item

See `references/example-run.md` and `../_shared/token-budget.md`.

## First Step

Read fully and follow: `./steps/step-01-discover-pr.md`
