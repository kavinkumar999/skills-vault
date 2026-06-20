# Round Artifact Template

Written each pass: `_bmad_output/pr-reviews/pr-{pr_number}-adversarial-v{review_round}.md`

```markdown
# Adversarial Code Review — PR #{pr_number} — v{review_round}

**Generated:** {date}
**PR:** {pr_url}
**Head SHA:** {head_sha}
**Branch:** {head} → {base}

> You have to do the adversarial code review.

## Summary

| Metric | Count |
| --- | --- |
| Found this round | {found_this_round} |
| Resolved this round | {resolved_this_round} |
| Still open (carried) | {still_open} |
| Regressed | {regressed_this_round} |
| **Total open** | **{total_open}** |

## Open blockers (action required)

| ID | Severity | Location | Blocker | Failure mode | Since |
| --- | --- | --- | --- | --- | --- |
| BLK-001 | critical | `handler.ts:42` | Missing null guard on token | 500 on expired session | v1 |

## Resolved this round

| ID | Severity | Location | Blocker | Resolved in |
| --- | --- | --- | --- | --- |
| BLK-002 | high | `api.ts:10` | Unchecked promise rejection | v{review_round} |

## Regressed this round

| ID | Severity | Location | Blocker | Notes |
| --- | --- | --- | --- | --- |
| BLK-003 | high | `db.ts:88` | Migration not reversible | Reintroduced in {short_sha} |

## Evidence appendix

### BLK-001

- **Location:** `handler.ts:42`
- **Evidence:** …
- **Why it blocks merge:** …
```

Only Critical and High rows in open/resolved/regressed tables.
