---
---

# Step 2b: Compact PR Digest

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Distill only** — no adversarial findings here
- When `{reuse_digest}` is true, validate head SHA in the existing digest matches `{head_sha}`; if mismatch, rebuild

## INSTRUCTIONS

1. **If `{reuse_digest}` is true** and SHA matches → load `{digest_path}` into `{change_digest}` and skip to step 4.

2. **Synthesize `{change_digest}`** from Step 2 outputs. Follow `references/compact-digest-template.md` (same shape as `bmad-pr-describe` digest).

   Hard limits:
   - Per-file one-liners: max `{workflow.digest_max_file_lines}`; overflow → "and N more files (see diff)"
   - One-line summary: ≤ `{workflow.digest_summary_max_chars}` characters
   - AC rows: ID + one-line criterion only
   - CI: table of check name + conclusion only

3. **Write** `{change_digest}` to `{digest_path}`.

4. **Report in chat** (≤ 6 lines):

   > Digest ready — {file_count} files, CI: {pass/fail/mixed}, risks flagged: {yes/no}.
   > Artifact: `{digest_path}`

   Do not paste the full digest unless the user asks.

## NEXT

Read fully and follow: `./step-03-adversarial-review.md`
