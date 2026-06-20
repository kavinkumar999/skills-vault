# GitHub PR Review Commands

Use `gh api graphql` for threads. REST comment IDs are **not** thread IDs. Auth and the
`gh pr edit --body-file` contract are in `../_shared/github-commands.md`; this file covers
the review-thread GraphQL that is unique to review closure.

## Resolve the PR (extra fields review closure needs)

```bash
gh pr view --json number,url,title,body,reviews,latestReviews,headRepositoryOwner,headRepository,baseRepository
```

## Fetch review threads (paginate)

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

### Copilot filter

- `isResolved: false`
- First comment `author.login` in `{workflow.copilot_author_logins}`

### Human filter

- `isResolved: false`
- Comment from a login in `{reviewers}` and NOT in `{workflow.excluded_author_logins}`

### Prior-reply detection

Any comment body containing `{workflow.reply_marker}` or legacy `<!-- bmad-copilot-closure -->` or `<!-- bmad-pr-reviewer-response -->` → already answered.

## Reply to thread

```bash
gh api graphql -f query='
mutation($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId
    body: $body
  }) {
    comment { id url }
  }
}' -f threadId="PRRT_..." -f body="..."
```

End body with `{workflow.reply_marker}` on its own line. Write in `{workflow.reply_language}`.

## Resolve thread (Copilot: always; human: per `{workflow.human_resolve_threads}`)

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: { threadId: $threadId }) {
    thread { id isResolved }
  }
}' -f threadId="PRRT_..."
```

## PR comment (human summary)

```bash
gh pr comment {pr_number} --body "..."
```

## Edit PR description

`gh pr edit {pr_number} --body-file …` — see `../_shared/github-commands.md`.

## Push fixes

```bash
git add <files>
git commit -m "fix: address PR review feedback (#{pr_number})"
git push
```
