# Compact PR Digest Template

Written at Step 2b: `_bmad_output/pr-reviews/pr-{pr_number}-digest.md`  
**Purpose:** one-screen distillation of diff + story + test evidence — Step 3 drafts the PR body from this, not the raw diff.

```markdown
# PR Digest — #{pr_number}

**Generated:** {date}
**Branch:** {head} → {base}
**Ticket:** {ticket_key}
**Story:** {story_file or "—"}

## One-line summary

…

## Change digest (by area)

| Area | Files | What changed |
| --- | --- | --- |
| src/auth | 3 | session refresh + retry |
| tests | 2 | unit coverage for 503 path |

## Per-file one-liners

- `src/http/client.ts` — add retry on 503
- `src/auth/session.ts` — wire refresh through client

## Acceptance criteria (extract only)

| ID | Criterion | PR signal |
| --- | --- | --- |
| AC-1 | … | `session.ts`, tests |

## Test gates

| Gate | Result | Detail |
| --- | --- | --- |
| `:module:test` | pass | 42 tests, 0 failed |

## Risk / diagram flags

- **Risks:** migration 0042, config `SESSION_TTL`
- **Diagram worthy:** yes — Client → AuthService → TokenStore

## Artifact links (paths only)

- digest: `pr-reviews/pr-{n}-digest.md`
- story: `{tracked_story_path}`

## Drafting notes for Step 3

- Lead summary with …
- Omit diagram if …
```

Keep the digest scannable in &lt; 2 minutes. No full diff hunks, no full story prose, no raw test log dumps.
