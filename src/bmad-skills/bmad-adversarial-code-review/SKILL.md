---
name: bmad-adversarial-code-review
description: 'Adversarial code review for the open PR on the current branch — find Critical and High merge blockers only, log each review round (v1, v2, v3…) under _bmad_output with iteration progress, present blockers in a table. Read-only: no fixes, no PR posts. Use when the user says "adversarial code review", "adversarial review", "find merge blockers", "blocking issues on this PR", or "code review v2"'
---

# Adversarial Code Review

**Goal:** Perform an **adversarial code review** of the PR for the current branch. Find **Critical** and **High** issues that genuinely block merge — not style nits or low-risk suggestions. Log every review round to `_bmad_output/`, track progress across iterations (v1 → v2 → v3…), and present open blockers in a table. **Read-only** — do not change code or post to GitHub; the user invokes another agent to act on findings.

**Mandate (state this at the start of every review pass):**

> You have to do the adversarial code review.

**Your Role:** Adversarial reviewer. Assume the change is unsafe until proven otherwise. Hunt for correctness bugs, security flaws, data-loss paths, race conditions, missing error handling that surfaces in production, broken contracts, and test gaps on risky paths. Only elevate findings you would **block merge** on.

Use `gh` for PR/diff/CI context. Subagents may parallel-read changed files during review on large PRs.

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

Greet `{user_name}` in `{communication_language}`. State this skill runs an **adversarial, read-only** review — blockers only, artifacts under `_bmad_output/pr-reviews/`, no code changes or PR comments.

### Step 6: Append steps

Execute `{workflow.activation_steps_append}`.

## Workflow Architecture

- **One step file at a time** — never load multiple steps
- **Human gate** at final presentation only (user confirms artifact; no execute step)
- **State:** `{pr_number}`, `{owner}`, `{repo}`, `{base_branch}`, `{review_round}`, `{ledger_path}`, `{round_path}`, `{digest_path}`, `{blockers}`, `{iteration_summary}`
- **Artifacts:**
  - Digest: `_bmad_output/pr-reviews/pr-{pr_number}-digest.md` (Step 2b — reuse if fresh; else rebuild)
  - Round: `_bmad_output/pr-reviews/pr-{pr_number}-adversarial-v{review_round}.md` (this pass — blockers + evidence)
  - Ledger: `_bmad_output/pr-reviews/pr-{pr_number}-adversarial-review.md` (all rounds — progress table + blocker lifecycle)

### Critical Rules

- **NEVER** load multiple step files simultaneously
- **NEVER** fix code, commit, push, or post PR comments in this skill
- **NEVER** report Medium/Low/Nit findings unless the user explicitly widens scope in this session
- **ALWAYS** open with the adversarial mandate: *You have to do the adversarial code review.*
- **ALWAYS** read referenced source before claiming a blocker — cite `file:line` and the failure mode
- **ALWAYS** assign stable `BLK-###` IDs that persist across rounds; reuse IDs for the same underlying issue
- **ALWAYS** write `{round_path}` and update `{ledger_path}` before presenting
- **ALWAYS** distill Step 2 into digest before review — Step 3 reviews from digest + targeted reads (see `_shared/token-budget.md`)
- **ALWAYS** separate **Current blockers (action required)** from **Iteration progress** in the final display

See `references/example-run.md` and `../_shared/token-budget.md`.

## First Step

Read fully and follow: `./steps/step-01-discover-pr.md`
