# Compact PR Digest Template

Written at Step 2b: `_bmad_output/pr-reviews/pr-{pr_number}-digest.md`  
**Purpose:** one-screen distillation for adversarial review — Step 3 works from this, not the raw diff.

```markdown
# PR Digest — #{pr_number}

**Generated:** {date}
**Head SHA:** {head_sha}
**Branch:** {head} → {base}
**Ticket:** {ticket_key or "—"}

## One-line summary

…

## Change digest (by area)

| Area | Files | What changed |
| --- | --- | --- |
| src/auth | 3 | session refresh + retry |

## Per-file one-liners

- `src/http/client.ts` — add retry on 503

## CI checks

| Check | Conclusion |
| --- | --- |
| unit-tests | success |

## Risk signals (adversarial focus)

- migration 0042, auth middleware change, new external webhook

## Prior open blockers (from ledger)

| ID | Title | Since |
| --- | --- | --- |
| BLK-001 | Race on token refresh | v1 |
```

Keep scannable in under 2 minutes. No full diff hunks.
