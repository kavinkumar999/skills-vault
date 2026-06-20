---
---

# Step 4: Write Review Artifacts

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Write files before presenting** — chat is not the system of record
- Compose artifacts in `{workflow.reply_language}` when it differs from chat language

## INSTRUCTIONS

1. **Set `{round_path}`:**

   `_bmad_output/pr-reviews/pr-{pr_number}-adversarial-v{review_round}.md`

2. **Write `{round_path}`** using `references/round-artifact-template.md`.

   Include: PR metadata, head SHA, mandate statement, **Open blockers** table, **Resolved this round** table (if any), **Regressed** table (if any), evidence appendix by `BLK-###`.

3. **Update `{ledger_path}`** using `references/ledger-template.md`:

   - If new: create with PR header + iteration progress table + blocker lifecycle table.
   - If exists: append row to **Iteration progress**; upsert rows in **Blocker lifecycle** by `BLK-###`; link `{round_path}`.

   **Iteration progress row for v{review_round}:**

   | Round | Head SHA | Found | Resolved | Still open | Regressed | Total open | Artifact |
   | --- | --- | --- | --- | --- | --- | --- | --- |
   | v{N} | `{short_sha}` | {found_this_round} | {resolved_this_round} | {still_open} | {regressed_this_round} | {total_open} | link |

4. **Confirm files on disk** — both `{round_path}` and `{ledger_path}` must exist before Step 5.

5. **Report in chat** (≤ 4 lines):

   > Artifacts written — v{review_round}: {total_open} open, {resolved_this_round} resolved.
   > Round: `{round_path}`
   > Ledger: `{ledger_path}`

## NEXT

Read fully and follow: `./step-05-present.md`
