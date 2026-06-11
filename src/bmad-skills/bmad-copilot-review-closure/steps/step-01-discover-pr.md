---
---

# Step 1: Discover Pull Request

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Do not fetch threads until `{pr_number}`, `{owner}`, and `{repo}` are confirmed

## INSTRUCTIONS

1. **Verify `gh` is available and authenticated:**

   ```bash
   gh auth status
   ```

   If this fails, stop and tell the user to run `gh auth login`.

2. **Resolve the target PR:**

   - If the user provided a PR number or URL, use it.
   - Otherwise run:

     ```bash
     gh pr view --json number,url,title,headRepositoryOwner,headRepository,baseRepository
     ```

   - Set `{owner}` and `{repo}` from the PR's base repository (or head if fork workflow requires it).
   - Set `{pr_number}` from the PR number.
   - Set `{pr_url}` from the URL.

3. **Confirm with the user** (one line unless ambiguous):

   > Processing Copilot threads on PR #{pr_number}: {title} ({pr_url})

   If multiple open PRs exist and none is current, list them and ask which to use. **HALT** until confirmed.

4. **Set the report path and check for a prior run:**

   - `{report_path}` = `{implementation_artifacts}/pr-reviews/pr-{pr_number}-copilot-closure.md`
   - If the file exists, read it. It records the previous run's triage, decisions, and per-thread results.
     - Threads marked `replied: yes, resolved: no` → resume candidates (finish resolution only — never re-reply)
     - Threads marked `resolved: yes` → done; exclude from this run
     - Tell the user what the prior run left behind and ask: **resume** (finish incomplete threads, then pick up new ones) or **fresh** (re-fetch everything; completed threads are still excluded). **HALT** until answered.
   - If the file does not exist, this is a fresh run; it will be created in Step 4.

5. **Load GraphQL reference** — skim `references/graphql-commands.md` for query shapes you will use in Step 2.

## NEXT

Read fully and follow: `./step-02-fetch-threads.md`
