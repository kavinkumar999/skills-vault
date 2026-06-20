# Example Run — Adversarial Code Review

## v1 — first pass

```text
User: Run adversarial code review on this PR

Agent: You have to do the adversarial code review.
       PR #42: feat(auth): session refresh [NCC-1234]
       This is review round v1.
```

Finds 3 Critical/High blockers → writes:

- `_bmad_output/pr-reviews/pr-42-adversarial-v1.md`
- `_bmad_output/pr-reviews/pr-42-adversarial-review.md` (ledger)
- `_bmad_output/pr-reviews/pr-42-digest.md`

Presents **Current blockers** table (3 open) and **Iteration progress** (v1 only).

## v2 — after fixes

User fixes BLK-001 and BLK-002 via another agent, pushes, re-invokes skill.

```text
Agent: This is review round v2.
       v1: 3 blockers → resolved 2 → 1 open
       Found 1 new blocker this round → 2 open total.
```

Ledger iteration table now has v1 and v2 rows. BLK-001/002 marked resolved; BLK-004 new.

## v3 — clean pass

```text
Agent: No Critical or High merge blockers remain open.
       v1: 3 → v2: 2 open → v3: 0 open (resolved 2 this round).
```

User may merge or invoke **bmad-pr-describe** / **bmad-pr-review-closure** next.

## Handoff

This skill never edits code. After approving the artifact display, invoke implementation or **bmad-pr-review-closure** to act on `BLK-###` items.
