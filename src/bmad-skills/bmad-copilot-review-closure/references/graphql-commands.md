# GitHub GraphQL Commands for Copilot Review Closure

Use `gh api graphql` for thread state, replies, and resolution. REST comment IDs are **not** thread IDs.

## Prerequisites

```bash
gh auth status
```

## Discover owner/repo from current branch

```bash
gh pr view --json number,url,headRepositoryOwner,headRepository,baseRepository
```

If not on a PR branch, the user must supply PR number or URL.

## Fetch all review threads (paginate if >100)

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      title
      url
      reviewThreads(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          startLine
          diffSide
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

Repeat with `-f after=END_CURSOR` while `hasNextPage` is true.

## Filter to Copilot + unresolved

Keep a thread when:

- `isResolved` is `false`
- First comment's `author.login` is in `{workflow.copilot_author_logins}`
- Optionally skip `isOutdated: true` if the line no longer exists (note to user)

## Reply to a thread

```bash
gh api graphql -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId
    body: $body
  }) {
    comment { id url }
  }
}' -f threadId="PRRT_..." -f body="Your reply text"
```

Body rules: write in `{workflow.reply_language}`; end with `{workflow.reply_marker}` on its own line (invisible on GitHub, detected by re-runs to prevent duplicate replies).

## Resolve a thread

**Required for fix, defer, and no_action.** Defer does not skip resolution — reply first, then resolve.

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id isResolved }
  }
}' -f threadId="PRRT_..."
```

## Verify remaining unresolved Copilot threads

Re-run the fetch query and count threads matching Copilot authors with `isResolved: false`.

## Push after code fixes

```bash
git status
git add <files>
git commit -m "fix: address Copilot review comment on <path>"
git push
```

Resolve threads **after** the fix is pushed so the reply references committed work.
