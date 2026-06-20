---
---

# Step 3: Adversarial Code Review

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Read-only** — no code edits, no PR comments
- Open this step by stating the mandate verbatim:

  > **You have to do the adversarial code review.**

- Report only `{workflow.allowed_severities}` — merge blockers you would refuse to ship without fix or explicit risk acceptance
- Every finding needs `file:line`, failure mode, and why it blocks merge

## INSTRUCTIONS

### 1. Adversarial stance

Assume the change breaks production until disproven. Prioritize:

- Correctness under failure (errors, timeouts, partial writes)
- Security (authz bypass, injection, secret exposure, unsafe defaults)
- Data integrity (lost updates, non-idempotent side effects, migration rollback)
- Concurrency / races
- Contract breaks (API, events, DB schema) without migration or version guard
- Missing or misleading tests on the risky paths you identified

Do **not** report style, naming, or "nice to have" refactors.

### 2. Review inputs

Work from `{change_digest}` at `{digest_path}` plus **targeted** reads of changed files (hunks and surrounding context). On large PRs, parallel-read by area; merge into one `{blockers}` list.

Cross-check prior round: for each previously **open** `BLK-###`, verify whether the issue still exists on `{head_sha}`.

### 3. Build `{blockers}`

Each blocker:

| Field | Description |
| --- | --- |
| `id` | Stable `BLK-###` — reuse from prior round if same issue; new ID if new issue |
| `severity` | `critical` or `high` only |
| `location` | `path:line` (or `path` if line unknown) |
| `title` | Short imperative (≤ 80 chars) |
| `failure_mode` | What breaks in production |
| `evidence` | Code fact or behavior observed (≤ `{workflow.blocker_evidence_max_chars}` chars) |
| `status` | `open` · `resolved` · `regressed` |
| `round_found` | First round this appeared (e.g. `v1`) |

**Status rules this round:**

- **open** — still present (new or carried forward)
- **resolved** — was open last round, fixed on `{head_sha}` (list in resolved section, not in action table)
- **regressed** — was resolved earlier, issue is back

If no Critical/High blockers remain **open**, say so explicitly — that is a valid outcome.

### 4. Counts for `{iteration_summary}`

| Metric | Value |
| --- | --- |
| `found_this_round` | New open blockers first seen in v{review_round} |
| `still_open` | Carried forward open from prior rounds |
| `resolved_this_round` | Marked resolved since last round |
| `regressed_this_round` | Regressed since last round |
| `total_open` | Open blockers after this pass |

## NEXT

Read fully and follow: `./step-04-write-artifacts.md`
