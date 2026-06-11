---
---

# Step 2: Fetch Latest Reviewer Feedback

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Human reviewers only** — exclude `{workflow.excluded_author_logins}`
- Capture both **blockers** and **recommendations**
- Cover **every** reviewer in `{reviewers}` on the latest round — no reviewer's feedback may be silently dropped

## INSTRUCTIONS

1. **Review summary bodies** — for **each** reviewer in `{reviewers}`, parse their `review_body` into distinct items (numbered lists, bullets, "blocking:", "recommendation:", etc.). Each becomes a candidate feedback item tagged with that reviewer's login.

2. **Inline threads** — fetch via GraphQL (see `references/github-commands.md`). Keep unresolved threads whose comments are authored by any reviewer in `{reviewers}`. Map each to:
   - `thread_id` (`PRRT_…`) if inline
   - `path`, `line`
   - `reviewer_comment`
   - `source`: `inline` | `review_body` | `pr_comment`
   - `prior_reply`: `true` if any comment in the thread contains `{workflow.reply_marker}` — a previous run already answered it. Exclude these from triage (cross-check `{report_path}` if loaded; surface any item the report says was answered but looks unaddressed).

3. **PR conversation** — optional: recent issue comments from any `{reviewers}` login that contain actionable feedback.

4. **Build `{feedback_items}`** — assign sequential `id` (1, 2, 3…):

   | Field | Description |
   | --- | --- |
   | `id` | User-facing number |
   | `severity` | `blocker` \| `recommendation` \| `question` |
   | `source` | `inline` \| `review_body` \| `pr_comment` |
   | `thread_id` | GraphQL id if inline, else empty |
   | `path` / `line` | If code-related |
   | `raw_text` | Reviewer's words |
   | `reviewer` | login |

5. **Deduplicate** — merge duplicate items from review body + inline thread. If two reviewers raise the same issue, keep one item listing both reviewers — both get @-mentioned in the response.

6. **Report, grouped by reviewer:**

   > **@alice:** {B} blockers · {R} recommendations · {Q} questions
   > **@bob:** {B} blockers · {R} recommendations · {Q} questions
   > Skipped {N} item(s) already answered by a prior run.

   If empty: offer to widen (e.g. include reviewers dropped in Step 1) or end. **HALT**.

## NEXT

Read fully and follow: `./step-03-triage.md`
