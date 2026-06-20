---
---

# Step 1: Discover Pull Request

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Do not gather changes until `{pr_number}`, `{owner}`, `{repo}`, and `{base_branch}` are confirmed

## INSTRUCTIONS

1. **Verify `gh`:**

   ```bash
   gh auth status
   ```

   Stop and tell the user to `gh auth login` if this fails.

2. **Resolve the target PR** — from user input (PR number/URL) or the current branch:

   ```bash
   gh pr list --head "$(git branch --show-current)" --state open --json number,url,title,headRefOid,baseRefName
   ```

   - If the user gave a PR number or URL, use it.
   - Else if exactly one open PR exists for the branch, use it.
   - Else if multiple exist and `{workflow.pr_selection}` is `first_open`, pick the **lowest** `number`.
   - Else list open PRs and **HALT** until the user picks one.

   Then load full context:

   ```bash
   gh pr view {pr_number} --json number,url,title,body,baseRefName,headRefName,headRefOid,isDraft,baseRepository,headRepositoryOwner
   ```

   Set `{owner}`, `{repo}`, `{pr_number}`, `{pr_url}`, `{base_branch}`, `{head_sha}`, `{pr_title}`.

3. **Confirm** (one line unless ambiguous):

   > Adversarial review — PR #{pr_number}: {pr_title} ({pr_url})

4. **Set artifact paths:**

   - `{ledger_path}` = `_bmad_output/pr-reviews/pr-{pr_number}-adversarial-review.md`
   - `{digest_path}` = `_bmad_output/pr-reviews/pr-{pr_number}-digest.md`

5. **Determine `{review_round}`:**

   - If `{ledger_path}` exists, read the **Iteration progress** table — next round = max `vN` + 1 (e.g. after v2 → `3`).
   - Else `{review_round}` = `1` (first adversarial pass = **v1**).

   Tell the user: *This is review round **v{review_round}**.*

6. **Skim** `references/github-pr-commands.md`.

## NEXT

Read fully and follow: `./step-02-gather-changes.md`
