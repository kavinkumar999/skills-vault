# Compact Feedback Index Template

Written at Step 2b: `_bmad_output/pr-reviews/pr-{pr_number}-feedback-index.md`  
**Purpose:** one-screen index of all review threads — Step 3 triages from this; full bodies live in the report file.

```markdown
# Feedback Index — PR #{pr_number}

**Generated:** {date}
**Scope:** {review_scope}
**Reviewers:** @alice, @bob

## Index

| ID | Src | File:line | Sev | Excerpt | Prior? |
| --- | --- | --- | --- | --- | --- |
| C1 | copilot | `client.ts:42` | — | "Missing null check…" | no |
| H1 | @alice | `handler.ts:10` | blocker | "Race on refresh…" | no |

## By file (read once)

| File | IDs | Lines |
| --- | --- | --- |
| `client.ts` | C1 | 42, 88 |

## Resume-only (resolve, no reply)

- C4 — prior reply posted, thread open

## Counts

Copilot: {n} fresh · {r} resume · Human: {h} items
```

Excerpts ≤ `{workflow.thread_excerpt_max_chars}` chars. Full `raw_text` stored in `{report_path}` appendix only.
