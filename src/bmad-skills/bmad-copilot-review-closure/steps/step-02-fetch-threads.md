---
---

# Step 2: Fetch Unresolved Copilot Threads

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Copilot threads only** — match first-comment author against `{workflow.copilot_author_logins}`
- Skip threads where `isResolved` is `true`
- Paginate until all threads are loaded

## INSTRUCTIONS

1. **Fetch review threads** using the GraphQL query in `references/graphql-commands.md`. Paginate with `after` cursor until `hasNextPage` is false.

2. **Build `{copilot_threads}`** — for each unresolved thread where the first comment author is a Copilot login:

   | Field | Source |
   | --- | --- |
   | `thread_id` | GraphQL `id` (`PRRT_…`) |
   | `path` | thread `path` |
   | `line` | `line` or `startLine` |
   | `is_outdated` | `isOutdated` |
   | `body` | first comment `body` |
   | `author` | first comment `author.login` |
   | `comment_url` | construct from PR URL + path context if needed |
   | `suggestion_block` | contents of a ` ```suggestion ` fenced block in `body`, if present (empty otherwise) |
   | `prior_reply` | `true` if **any** comment in the thread contains `{workflow.reply_marker}` |

   Assign sequential `id` integers (1, 2, 3…) for user-facing references.

3. **Split out already-replied threads (idempotency):**

   Move every thread with `prior_reply: true` into `{resume_threads}` — a previous run replied but the resolve never landed (crash, API error, manual unresolve).

   - These threads **must not get a second reply**. Their only pending action is `resolveReviewThread`.
   - If `{resume_threads}` is non-empty, tell the user:

     > {N} thread(s) already carry this workflow's reply but are still unresolved. I will resolve them without re-replying (skipping triage).

   - Cross-check against `{report_path}` if it was loaded in Step 1 and note any mismatch.

4. **Report fetch summary:**

   - Total threads on PR
   - Unresolved Copilot threads found (fresh: {X} · resume-only: {Y})
   - Threads carrying a ready-made `suggestion_block`: {S}
   - Skipped: resolved count, human-reviewer count, outdated count (if any)

5. **If `{copilot_threads}` and `{resume_threads}` are both empty:**

   > ✅ No unresolved Copilot review threads on PR #{pr_number}.

   Offer to end or re-check after a delay. **HALT** — do not continue to triage.

   If only `{resume_threads}` has entries (nothing fresh to triage), skip Steps 3–4 and go directly to Step 5 to finish resolution.

## NEXT

Read fully and follow: `./step-03-triage.md`
