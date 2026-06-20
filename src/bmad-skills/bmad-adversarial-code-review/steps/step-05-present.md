---
---

# Step 5: Present Findings — Read-Only Handoff

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **HALT** after presenting — no code changes, commits, or PR posts
- Separate **action required now** from **iteration history**

## INSTRUCTIONS

### 1. Restate mandate and round

> **You have to do the adversarial code review.** — PR #{pr_number}, round **v{review_round}** ({pr_url})

### 2. Current blockers (action required)

If `{total_open}` > 0, show this table (open items only, critical first):

| ID | Severity | Location | Blocker | Failure mode |
| --- | --- | --- | --- | --- |
| BLK-001 | critical | `path:line` | … | … |

If `{total_open}` = 0:

> **No Critical or High merge blockers remain open.** (Resolved this round: {resolved_this_round}.)

Do not dump full evidence in chat — reference `BLK-###`; details are in `{round_path}`.

### 3. Iteration progress (separate section)

Show cumulative progress across all rounds from `{ledger_path}`:

| Round | Found | Resolved | Still open | Regressed | Total open |
| --- | --- | --- | --- | --- | --- |
| v1 | … | … | … | … | … |
| v2 | … | … | … | … | … |

One-line narrative:

> v1: {n1} blockers → resolved {r1} → {o1} open · v2: … · **Current:** {total_open} open.

### 4. Resolved / regressed this round (if any)

Brief bullet list — `BLK-###` title only. Omit section if empty.

### 5. Artifacts

| Artifact | Path |
| --- | --- |
| This round | `{round_path}` |
| Ledger (all rounds) | `{ledger_path}` |
| Digest | `{digest_path}` |

### 6. Handoff (do not execute)

Tell the user:

> Review is logged under `_bmad_output/pr-reviews/`. When you are ready to act on blockers, invoke your implementation or **bmad-pr-review-closure** agent against the latest code — not this skill.

**HALT** — wait for user direction. Do not fix blockers unless the user explicitly asks in a new request.

## DONE

Workflow complete. No further steps.
