---
---

# Step 1: Discover PR and Review Scope

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Confirm `{pr_number}`, `{owner}`, `{repo}`, and `{review_scope}` before fetching

## INSTRUCTIONS

1. **Verify `gh`:** `gh auth status` — stop and tell user to `gh auth login` if it fails.

2. **Resolve PR** — from user input or:

   ```bash
   gh pr view --json number,url,title,body,reviews,latestReviews,headRepositoryOwner,headRepository,baseRepository
   ```

   Set `{owner}`, `{repo}`, `{pr_number}`, `{pr_url}`, `{pr_body}`.

3. **Set `{review_scope}`** — infer from the user's message, else ask once:

   | User intent | `{review_scope}` |
   | --- | --- |
   | copilot / copilot comments / close copilot | `copilot` |
   | reviewer / human / blocking / changes requested | `human` |
   | both / all feedback / full review closure | `both` |
   | unclear | use `{workflow.default_review_scope}` or **HALT** and ask |

4. **If scope includes `human`**, build `{reviewers}`:

   - Restrict to `{workflow.reviewer_logins}` when non-empty.
   - Else every human with `CHANGES_REQUESTED` or `COMMENTED` on the latest round, excluding `{workflow.excluded_author_logins}`.
   - Offer to drop reviewers. **HALT** until confirmed when multiple reviewers exist.

5. **Confirm:**

   > PR #{pr_number}: {title} ({pr_url})
   > Scope: {copilot | human (@alice, @bob) | both}

6. **Report path and resume:**

   - `{report_path}` = `_bmad_output/pr-reviews/pr-{pr_number}-review-closure.md`
   - If exists: read prior triage/execution rows; offer **resume** or **fresh**. **HALT** until answered.
   - Also check legacy reports `pr-{n}-copilot-closure.md` and `pr-{n}-reviewer-response.md` for resume hints if present.

7. Skim `references/github-pr-commands.md`.

## NEXT

Read fully and follow: `./step-02-fetch-feedback.md`
