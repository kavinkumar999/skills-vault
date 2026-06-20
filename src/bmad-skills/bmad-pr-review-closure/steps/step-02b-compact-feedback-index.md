---
---

# Step 2b: Compact Feedback Index

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Index only** — no triage, no code fixes, no replies
- Truncate thread bodies to `{workflow.thread_excerpt_max_chars}` in the index; store full text in report appendix
- Step 3 triages from `{feedback_index}` — do not re-fetch GraphQL

## INSTRUCTIONS

1. **Build `{feedback_index}`** from Step 2 `{copilot_threads}`, `{feedback_items}`, `{copilot_resume_threads}`. Follow `references/compact-feedback-template.md`.

   For each item:
   - `id`, `source`, `path`, `line`, `severity` (human only), `excerpt` (truncated body), `prior_reply`, `has_suggestion`
   - **Do not** duplicate `suggestion_block` in index — flag `has_suggestion: true` only

2. **Group by file `{files_to_read}`:**

   | File | Item IDs | Lines to read |
   | --- | --- | --- |
   | `client.ts` | C1, H2 | 42, 88 |

   Step 3 reads each file **once** per group.

3. **Write artifacts:**

   - `{index_path}` = `_bmad_output/pr-reviews/pr-{pr_number}-feedback-index.md` — save compact index
   - Append **Full feedback appendix** to `{report_path}` (create if new): each ID → full `raw_text` / `suggestion_block`. Chat and triage use index only.

4. **Report in chat** (≤ 6 lines):

   > Feedback index — Copilot: {fresh} fresh, {resume} resume-only · Human: {h} items across {file_count} files.
   > Index: `{index_path}`

5. **Early exit unchanged** — if nothing to triage and no resume threads, halt per Step 2C. If only resume threads, skip Step 3–4 per Step 2C.

## NEXT

Read fully and follow: `./step-03-triage.md`
