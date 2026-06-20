# Custom PR Skills (BMad custom module)

Custom skills kept outside the BMAD-METHOD repo so upstream pulls stay clean.

## Skills

- **bmad-jira-solution-spec** (`JS`) — Pull an assigned Jira ticket, validate it against the codebase, and write a **solution spec** artifact (problem, root cause, implementation plan). Recommends which agent to invoke next (e.g. `bmad-dev-story`, `investigate-service-incident`).
- **bmad-pr-describe** (`PD`) — Generate or refresh the PR description from the diff, story file, and test evidence: summary, AC mapping, checklist, BMad artifact links. Creates a draft PR when none exists.
- **bmad-adversarial-code-review** (`AR`) — **Adversarial, read-only** review of the open PR: find **Critical** and **High** merge blockers only, log each round (v1, v2, v3…) under `_bmad_output/pr-reviews/` with iteration progress. No code changes or PR posts — hand off to an implementation agent when ready.
- **bmad-pr-review-closure** (`RC`) — Unified review closure for **Copilot** and/or **human** feedback: triage, fix/defer, reply, resolve Copilot threads, post Issue/Resolution replies for humans.

Lifecycle: **JS** (solution spec) → implement (`bmad-dev-story` or routed agent) → **PD** (describe) → **AR** (adversarial review) → fix blockers → **AR** (v2, v3…) → **RC** (review closure) → **PD** (refresh description after fixes).

Each skill includes `references/example-run.md`.

### Migration from v1 (split review skills)

`bmad-copilot-review-closure` (`CP`) and `bmad-pr-reviewer-response` (`RB`) are merged into **bmad-pr-review-closure** (`RC`). Set `{review_scope}` to `copilot`, `human`, or `both`. Legacy reply markers from the old skills are still honored. Move team overrides to `_bmad/custom/bmad-pr-review-closure.toml`.

## Install

Add the vault (or this family alone) as a custom source when installing BMad.
Replace `<vault-path>` with the absolute path to this repo, or use a git URL.

**Whole vault** (picker lists every family):

```bash
npx bmad-method install \
  --directory <your-project> \
  --modules bmm \
  --custom-source <vault-path> \
  --tools claude-code \
  --yes
```

**This family only**:

```bash
npx bmad-method install \
  --directory <your-project> \
  --modules bmm \
  --custom-source <vault-path>/src/bmad-skills \
  --tools claude-code \
  --yes
```

Or interactively: run `npx bmad-method install`, answer **Yes** to
"Do you want to install custom or community modules (Git URL or local path)?"
and paste `<vault-path>` or `<vault-path>/src/bmad-skills`.

The installer reads this folder directly (local sources are not copied to a
cache), so edits here are picked up on the next install/quick-update.

## Standalone mode (Cursor / no BMad)

Skills work without a full BMad install when symlinked into Cursor or copied into a
repo that has no `_bmad/` folder. On activation, if `{project-root}/_bmad/bmm/config.yaml`
is missing, the agent uses defaults from `_shared/standalone-mode.md` and
`{skill-root}/customize.toml` only.

Set `test_command` and other workflow knobs in `{skill-root}/customize.toml`, or add
`{project-root}/_bmad/custom/<skill-name>.toml` for team overrides even without full BMad.

## Token budget (all skills)

Shared patterns live in `_shared/token-budget.md`: **ingest once → compact artifact → downstream steps use the digest**.

| Skill | Compact artifact | Saves tokens by |
| --- | --- | --- |
| **JS** `bmad-jira-solution-spec` | `{key}-compact-analysis.md` | Jira/comments/logs distilled before codebase search |
| **PD** `bmad-pr-describe` | `pr-{n}-digest.md` | Diff + story AC extract before PR body draft |
| **AR** `bmad-adversarial-code-review` | `pr-{n}-digest.md` + `pr-{n}-adversarial-v*.md` | Diff digest before review; per-round blocker artifact |
| **RC** `bmad-pr-review-closure` | `pr-{n}-feedback-index.md` | Thread excerpts + per-file grouping before triage |

Tune caps in `_bmad/custom/<skill-name>.toml` (`diff_file_threshold`, `thread_excerpt_max_chars`, etc.).

## Behavior and configuration

All skills:

- Write per-run reports under `_bmad_output/pr-reviews/pr-{number}-*.md`
  (triage, decisions, per-item results). Interrupted runs resume from it; it also
  serves as the audit trail.
- Stamp every PR reply with an invisible marker so re-runs never double-post —
  a crash between "replied" and "resolved" is finished, not repeated.
- Post all public PR content in `reply_language` (default `en`) even when chat
  runs in another language.

Tunable per project in `_bmad/custom/<skill-name>.toml` (team) or
`<skill-name>.user.toml` (personal):

| Key | Default | Effect |
| --- | --- | --- |
| `test_command` | `""` | If set, runs after fixes; failure halts before push |
| `ticket_pattern` | `[A-Z][A-Z0-9]+-\d+` (any Jira key) | Extracted from branch/commits/story; asked for if missing; required in title and commits |
| `commit_message_template` | conventional `fix:` message | `{pr_number}` and `{ticket_key}` substituted |
| `auto_push` | `"ask"` | `"always"` pushes without confirmation |
| `reply_language` | `"en"` | Language for all PR-visible posts |
| `reply_marker` | skill-specific HTML comment | Re-run duplicate guard |

Copilot items apply ` ```suggestion ` blocks verbatim when they still apply cleanly.
Review closure scope is `copilot`, `human`, or `both` (default `both`). Human reviewers
are all with open feedback unless pinned via `reviewer_logins`. Copilot threads always
resolve after reply; human thread resolve is configurable (`human_resolve_threads`).

PR describe keeps its generated content between `<!-- bmad-pr-describe:begin/end -->`
markers in the PR body — refreshes replace only that block and preserve hand-written
content around it. Its own knobs: `sections` (which body sections to render),
`checklist_items`, `create_if_missing` (`"ask"` offers a draft PR when the branch
has none), and `apply_mode`. It also: generates the PR **title** via `title_template`
(ticket key from `ticket_pattern` is mandatory in title and commits — e.g.
`feat(auth): add session refresh [NCC-1234]`); maps content into the repo's
`PULL_REQUEST_TEMPLATE.md` when one exists (`respect_repo_template`); runs a
**secrets scan** on the diff that halts on findings (`secrets_scan`,
`secrets_patterns`); and conditionally renders a **Risk & rollback** section
(migrations/config/flags detected) and a **Mermaid diagram** for cross-component
flow changes. **BMad artifacts:** `_bmad_output/` is the symlink (BMad reads here only);
git tracks files elsewhere — commit + push tracked paths, link in PR body.

**Jira solution spec** (`bmad-jira-solution-spec`, menu `JS`): pulls Jira via Atlassian MCP,
**downloads attachments**, **extracts repro/diagnostic commands**, writes a **compact analysis**
(`{key}-compact-analysis.md`) for approval, investigates the codebase against that plan, then
writes the full solution spec. Routes to an implementation agent via `agent_routes`.
Knobs: `attachment_max_count`, `run_diagnostic_commands`, `embed_compact_analysis`, `sections`.

## Optional: add menu shortcuts to the dev agent

To expose these skills in Amelia's (bmad-agent-dev) menu, add this to
`_bmad/bmm/bmad-agent-dev/customize.toml` in your **installed project**
(not the BMAD-METHOD repo — repo edits are lost on upstream updates):

```toml
[[agent.menu]]
code = "JS"
description = "Analyze assigned Jira ticket against codebase and produce a solution spec with implementation handoff"
skill = "bmad-jira-solution-spec"

[[agent.menu]]
code = "PD"
description = "Generate or refresh the PR description from diff, story, and test evidence before requesting review"
skill = "bmad-pr-describe"

[[agent.menu]]
code = "AR"
description = "Adversarial read-only PR review — find Critical/High merge blockers, log v1/v2/v3 progress under _bmad_output"
skill = "bmad-adversarial-code-review"

[[agent.menu]]
code = "RC"
description = "Close PR review feedback — Copilot and/or human: triage, fix, reply, resolve"
skill = "bmad-pr-review-closure"
```
