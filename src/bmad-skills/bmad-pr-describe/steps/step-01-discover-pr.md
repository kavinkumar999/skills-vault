---
---

# Step 1: Discover Pull Request (or Branch)

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Do not gather context until `{pr_number}` (or the create-PR decision), `{owner}`, `{repo}`, and `{base_branch}` are confirmed

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
     gh pr view --json number,url,title,body,baseRefName,headRefName,isDraft,baseRepository,headRepositoryOwner
     ```

   - Set `{owner}`, `{repo}`, `{pr_number}`, `{pr_url}`, `{base_branch}`, `{existing_body}`.

3. **If the branch has no PR**, follow `{workflow.create_if_missing}`:

   - `"ask"` → offer: *No PR exists for this branch. Create a draft PR with the generated description? (yes/no)* — if yes, set `{create_pr}: true`, derive `{base_branch}` (repo default or user-specified), and continue; the PR is created in Step 5 with the approved body. **HALT** until answered.
   - `"never"` → tell the user to create a PR first and stop.

4. **Confirm with the user** (one line unless ambiguous):

   > Drafting description for PR #{pr_number}: {title} ({pr_url})

   or, when creating:

   > Drafting description for a new draft PR: {head_branch} → {base_branch}

   If multiple open PRs exist and none is current, list them and ask which to use. **HALT** until confirmed.

5. **Check the existing body for prior generated content:**

   - If `{existing_body}` contains `{workflow.body_marker_begin}`, this is a **refresh**: the content between the markers will be regenerated; everything outside is hand-written and preserved verbatim. Tell the user.
   - Otherwise this is a **first run**: the generated block will be appended (or become the whole body if the existing one is empty/template boilerplate — confirm before replacing non-empty unmarked content).

6. **Set the report path:** `{report_path}` = `{implementation_artifacts}/pr-reviews/pr-{pr_number}-describe.md` (use the head branch name instead of a number until a new PR is created).

7. **Load reference** — skim `references/github-commands.md` for the commands used in Steps 2 and 5.

## NEXT

Read fully and follow: `./step-02-gather-context.md`
