---
---

# Step 2b: Compact PR Digest

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Distill only** — no PR body drafting here; no re-reading the full diff
- Compose the digest artifact in `{workflow.reply_language}` when it differs from chat language
- Step 3 must be able to run from `{change_digest}` + `{digest_path}` alone

## INSTRUCTIONS

1. **Synthesize `{change_digest}`** from Step 2 outputs only (`{change_summary}`, `{ticket_key}`, `{story_file}` AC extract, `{test_gates}`, `{risk_signals}`, `{diagram_worthy}`, `{artifacts_to_commit}`). Follow `references/compact-digest-template.md`.

   Hard limits:
   - Per-file one-liners: max `{workflow.digest_max_file_lines}` entries; overflow → "and N more files (see diff)"
   - AC rows: IDs + one-line criterion text only (no story narrative)
   - Test gates: table only — no `{evidence_raw}` in digest (raw output stays in Step 3 `<details>` block)
   - One-line summary: ≤ `{workflow.digest_summary_max_chars}` characters

2. **Set paths:**

   - `{digest_path}` = `_bmad_output/pr-reviews/pr-{pr_number}-digest.md` (use head branch name when `{pr_number}` unknown)

3. **Write artifact** — save `{change_digest}` to `{digest_path}`.

4. **Report in chat** (≤ 8 lines):

   > Digest ready — {file_count} files, {ac_count} AC, {test_gate_count} test gates, risks: {yes/no}.
   > Artifact: `{digest_path}`

   Do **not** paste the full digest in chat unless the user asks — Step 4 shows the PR draft.

5. **Hand off to Step 3:**

   - `{drafting_inputs}` = `{change_digest}` only (not raw diff, not full story file)
   - If digest is empty because diff was empty, **HALT** (same as Step 2).

## NEXT

Read fully and follow: `./step-03-draft-description.md`
