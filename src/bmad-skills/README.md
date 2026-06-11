# Custom PR Skills (BMad custom module)

Custom skills kept outside the BMAD-METHOD repo so upstream pulls stay clean.

## Skills

- **bmad-pr-describe** (`PD`) — Generate or refresh the PR description from the diff, story file, and test evidence: summary, AC mapping, checklist. Runs before requesting review.
- **bmad-copilot-review-closure** (`CP`) — Triage unresolved Copilot PR comments: fix or defer, reply, and resolve threads.
- **bmad-pr-reviewer-response** (`RB`) — Address human reviewer PR feedback: validate blockers, fix code or PR body, post issue/resolution replies.

Together they cover the PR lifecycle: **PD** (describe) → **CP** (Copilot review) → **RB** (human review).

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

## Behavior and configuration

Both skills:

- Write a per-run report to `{implementation_artifacts}/pr-reviews/pr-{number}-*.md`
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

Copilot closure additionally applies Copilot's ` ```suggestion ` blocks verbatim
when they still apply cleanly, and auto-recommends `no_action` for outdated
comments whose code has since changed. Reviewer response addresses **all** human
reviewers with open feedback by default (pin via `reviewer_logins`).

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
flow changes. The `bmad_artifacts` section attaches the story file,
review reports, and sprint-status entry to the PR via **commit-and-link**
(`commit_artifacts = true`): new/changed artifacts are committed and pushed to the
PR branch (message via `artifact_commit_message_template`, push approved together
with the draft), then linked by branch URL — one tree link to the whole artifacts
folder plus per-file blob links. Requires the artifacts path (e.g. a `_bmad_output`
symlink target) to be tracked in git; untrackable files fall back per
`uncommitted_artifacts` (`mention` default, or `embed`/`skip`). Sources are the
`artifact_sources` globs.

## Optional: add menu shortcuts to the dev agent

To expose these skills in Amelia's (bmad-agent-dev) menu, add this to
`_bmad/bmm/bmad-agent-dev/customize.toml` in your **installed project**
(not the BMAD-METHOD repo — repo edits are lost on upstream updates):

```toml
[[agent.menu]]
code = "PD"
description = "Generate or refresh the PR description from diff, story, and test evidence before requesting review"
skill = "bmad-pr-describe"

[[agent.menu]]
code = "CP"
description = "Triage unresolved Copilot PR comments — fix or defer, reply, and resolve threads"
skill = "bmad-copilot-review-closure"

[[agent.menu]]
code = "RB"
description = "Address human reviewer PR feedback — validate blockers, fix code or PR body, post issue/resolution replies"
skill = "bmad-pr-reviewer-response"
```
