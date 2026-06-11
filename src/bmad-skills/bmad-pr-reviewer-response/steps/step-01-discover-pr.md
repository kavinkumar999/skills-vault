---
---

# Step 1: Discover Pull Request and Reviewers

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Confirm `{pr_number}`, `{owner}`, `{repo}`, and `{reviewers}` before fetching feedback

## INSTRUCTIONS

1. **Verify `gh`:**

   ```bash
   gh auth status
   ```

2. **Resolve PR:**

   - Use user-provided PR number/URL, or `gh pr view --json number,url,title,latestReviews,reviews`
   - Set `{owner}`, `{repo}`, `{pr_number}`, `{pr_url}`, `{pr_body}`

3. **Identify the reviewers (multi-reviewer by default):**

   - If `{workflow.reviewer_logins}` is non-empty, restrict to those logins.
   - Otherwise take **every human reviewer** with open feedback on the latest round — each reviewer's most recent review, `CHANGES_REQUESTED` and `COMMENTED` states — excluding `{workflow.excluded_author_logins}`.
   - Build `{reviewers}` — one entry per reviewer: `login`, `review_state`, `review_body`, `review_submitted_at`.

4. **Confirm with user:**

   > Addressing feedback on PR #{pr_number}: {title} ({pr_url})
   >
   > | Reviewer | State | Submitted |
   > | --- | --- | --- |
   > | @alice | CHANGES_REQUESTED | … |
   > | @bob | COMMENTED | … |

   Offer to drop any of them (e.g. "skip bob, just alice this round"). A two-reviewer round must not get half-answered silently — narrowing is the user's call, not a default. **HALT** until confirmed.

5. **Set the report path and check for a prior run:**

   - `{report_path}` = `{implementation_artifacts}/pr-reviews/pr-{pr_number}-reviewer-response.md`
   - If the file exists, read it: items marked `posted: yes` are done (exclude); items with decisions but `posted: no` are resume candidates. Tell the user what the prior run left behind and ask **resume** or **fresh**. **HALT** until answered.
   - If it does not exist, this is a fresh run; it will be created in Step 4.

6. Skim `references/github-commands.md` for fetch patterns used in Step 2.

## NEXT

Read fully and follow: `./step-02-fetch-feedback.md`
