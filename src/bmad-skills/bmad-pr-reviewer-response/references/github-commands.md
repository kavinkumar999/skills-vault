# GitHub Commands for PR Reviewer Response

## Prerequisites

```bash
gh auth status
```

## Discover PR

```bash
gh pr view --json number,url,title,body,headRepositoryOwner,headRepository,baseRepository,reviews,latestReviews
```

## Latest human review (filter bots)

From `reviews` / `latestReviews` JSON:

- Keep reviews where `author.login` is NOT in `{workflow.excluded_author_logins}`
- Prefer the most recent `CHANGES_REQUESTED` or `COMMENTED` review
- Capture: `author.login`, `body`, `submittedAt`, `state`

## Fetch inline review threads (human only)

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      reviewThreads(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          comments(first: 50) {
            nodes {
              id
              body
              createdAt
              author { login }
            }
          }
        }
      }
    }
  }
}' -F owner=OWNER -F repo=REPO -F number=PR_NUMBER
```

Filter threads:

- `isResolved: false`
- At least one comment from a human reviewer (not in `excluded_author_logins`)
- Restrict to logins in `{reviewers}` (all human reviewers selected in Step 1)
- Skip threads already containing `{workflow.reply_marker}` — answered by a prior run

## Fetch PR conversation comments (top-level)

```bash
gh api repos/{owner}/{repo}/issues/{pr_number}/comments
```

Include recent human comments that look like review feedback (blockers, recommendations).

## Edit PR description

```bash
gh pr edit {pr_number} --body-file /path/to/updated-body.md
# or
gh pr edit {pr_number} --body "updated markdown..."
```

## Reply to inline review thread

```bash
gh api graphql -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId
    body: $body
  }) {
    comment { id url }
  }
}' -f threadId="PRRT_..." -f body="**Issue:** ... **Resolution:** ..."
```

Body rules: write in `{workflow.reply_language}`; end with `{workflow.reply_marker}` on its own line (invisible on GitHub, detected by re-runs to prevent duplicate replies). Applies to thread replies **and** the summary comment below.

## Post top-level PR comment (summary or review-body response)

```bash
gh pr comment {pr_number} --body "**Reviewer response summary**

| # | Issue | Resolution | Status |
| --- | --- | --- | --- |
| 1 | ... | ... | ✅ Ready |
"
```

## Push code fixes

```bash
git add <files>
git commit -m "fix: address reviewer feedback on <topic> (#<pr_number>)"
git push
```

## Optional: resolve thread after reply

Only when the user confirms threads should be marked resolved:

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id isResolved }
  }
}' -f threadId="PRRT_..."
```

Human-review workflows often leave resolution to the reviewer; default is **reply only**, resolve only if user asks.
