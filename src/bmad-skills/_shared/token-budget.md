# Token Budget (BMad Skills)

Cross-skill patterns to **distill once, investigate once, link instead of re-embed**.
Skills reference this file from `{skill-root}/../_shared/token-budget.md`.

## Core pattern: compact artifact → downstream steps

| Phase | What happens | Token win |
| --- | --- | --- |
| **Ingest** | Fetch raw source once (Jira, diff, PR threads, logs) | Avoid re-fetch |
| **Distill** | Write a one-screen compact artifact | Drop noise from later steps |
| **Investigate / draft** | Work only from compact artifact + targeted reads | Narrow search |
| **Publish** | Link to artifacts; embed only when required | No duplicate dumps |

## Rules (all skills)

1. **Never carry raw blobs forward** — summarize attachments, logs, thread bodies, and diffs into structured fields; keep full text in artifact files on disk.
2. **Reference by ID** — commands `C1`, feedback `H1`/`C1`, AC `AC-1` — instead of repeating full text.
3. **Read each file once per workflow** — group PR review threads by `path`; read a changed file once per describe run.
4. **Cap excerpts** — honor `{workflow.*_max_chars}`, `{workflow.*_max_lines}` from each skill's `customize.toml`.
5. **Link, don't embed** — prefer artifact paths and GitHub/Jira URLs in published output; use `embed_* = "link"` when available.
6. **Hunks, not files** — for large diffs, use `git diff --stat` + changed hunks only unless a file is explicitly needed.
7. **Subagents for parallel ingest** — large PRs / many threads: parallel-read at ingest, merge into one compact index.

## Per-skill compact artifacts

| Skill | Compact artifact | Downstream consumer |
| --- | --- | --- |
| `bmad-jira-solution-spec` | `{ticket_key}-compact-analysis.md` | Step 4 codebase investigation |
| `bmad-pr-describe` | `pr-{n}-digest.md` | Step 3 PR body draft |
| `bmad-adversarial-code-review` | `pr-{n}-digest.md` | Step 3 adversarial review; round + ledger artifacts |
| `bmad-pr-review-closure` | `pr-{n}-feedback-index.md` | Step 3 triage, Step 5 execute |

## When *not* to compress

- User explicitly asks for full text in chat
- Secrets scan (must see exact added lines)
- Applying a Copilot `suggestion` block (verbatim apply)
- Legal/compliance requires quoting full AC verbatim in the PR body

## Team overrides

Add caps in `{project-root}/_bmad/custom/<skill-name>.toml` under `[workflow]` without forking the skill.
