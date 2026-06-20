# Ledger Template

Master file: `_bmad_output/pr-reviews/pr-{pr_number}-adversarial-review.md`  
**Purpose:** cumulative iteration progress and blocker lifecycle across v1, v2, v3…

```markdown
# Adversarial Review Ledger — PR #{pr_number}

**PR:** {pr_url}
**Started:** {date of v1}
**Last updated:** {date}

## Iteration progress

| Round | Date | Head SHA | Found | Resolved | Still open | Regressed | Total open | Artifact |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| v1 | 2026-06-20 | abc1234 | 3 | 0 | 0 | 0 | 3 | [v1](pr-42-adversarial-v1.md) |
| v2 | 2026-06-21 | def5678 | 1 | 2 | 1 | 0 | 2 | [v2](pr-42-adversarial-v2.md) |
| v3 | 2026-06-22 | ghi9012 | 0 | 2 | 0 | 0 | 0 | [v3](pr-42-adversarial-v3.md) |

## Blocker lifecycle

| ID | Severity | Title | First seen | Last status | Current |
| --- | --- | --- | --- | --- | --- |
| BLK-001 | critical | Missing null guard | v1 | v3 | resolved |
| BLK-002 | high | Race on refresh | v1 | v2 | resolved |
| BLK-003 | high | Webhook retry gap | v2 | v3 | open |

**Current:** {total_open} open blockers after v{latest_round}.
```

Upsert lifecycle rows by `BLK-###`. `Current` = `open` | `resolved` | `regressed`.
