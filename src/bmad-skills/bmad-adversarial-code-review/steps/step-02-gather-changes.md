---
---

# Step 2: Gather Changes — Diff, Commits, CI, Story

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Every blocker in Step 3 must trace to evidence gathered here or targeted reads in Step 3
- Large diffs: changed hunks only — see `{workflow.diff_file_threshold}`
- Follow `{skill-root}/../_shared/token-budget.md` — ingest once, distill in Step 2b

## INSTRUCTIONS

1. **Diff and commits:**

   ```bash
   gh pr diff {pr_number} --stat
   gh pr diff {pr_number}
   gh pr view {pr_number} --json commits
   git log {base_branch}..HEAD --oneline
   ```

   **Diff read mode** (`{workflow.diff_read_mode}`):
   - When changed file count ≤ `{workflow.diff_file_threshold}`: read hunks for each file.
   - When above threshold: hunks for **risk-touched** files (auth, migrations, public API, concurrency, payments) and one-liners from headers for the rest.

   Build `{change_summary}`: per-file one-liners grouped by area; note adds/deletes/renames, migrations, breaking changes.

2. **CI / test signal:**

   ```bash
   gh pr checks {pr_number}
   ```

   Record `{ci_status}`: failing checks are review input (do not treat green CI as proof of safety).

3. **Story / ticket context (optional):**

   - Search `_bmad_output/` for a story matching branch, `{workflow.ticket_pattern}`, or sprint status.
   - If found, extract AC IDs + criterion text only (no full narrative).
   - Extract `{ticket_key}` from branch, commits, or story; ask once if missing (informational only — does not block review).

4. **Prior review rounds:**

   - If `{ledger_path}` exists, read prior `BLK-###` rows and which were **open** at end of last round.
   - If `pr-{pr_number}-adversarial-v*.md` files exist, skim the latest round's blocker table for carry-forward IDs.

5. **Digest reuse check:**

   - If `{digest_path}` exists, same `{head_sha}`, and file mtime within `{workflow.digest_reuse_max_hours}` hours → set `{reuse_digest}: true` and skip full re-ingest (still verify CI and head SHA).
   - Else `{reuse_digest}: false`.

6. **Risk signals** for adversarial focus:

   - Auth/permissions, schema migrations, external API contracts, concurrency, feature flags, error swallowing, partial rollback, missing idempotency, secrets in diff.

7. **Report gathered** (≤ 8 lines): file count, CI summary, prior round open blockers count, digest reuse yes/no. If diff is empty, **HALT**.

## NEXT

Read fully and follow: `./step-02b-compact-digest.md`
