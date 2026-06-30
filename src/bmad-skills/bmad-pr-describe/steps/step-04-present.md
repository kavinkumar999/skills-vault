---
---

# Step 4: Present the Draft (Between Step)

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **HALT** after presenting — nothing is posted to GitHub in this step
- The user owns the final wording; your draft is a proposal

## INSTRUCTIONS

### 1. Show the draft

First the title, then the body:

> **Title:** `feat(auth): add session refresh [NCC-1234]`
> (current: `quick fix` — will be updated; the ticket key is required)

Render the full assembled body (markers included) in a fenced block so the user sees exactly what will be published. When a repo template was mapped, say so: *structured per `.github/PULL_REQUEST_TEMPLATE.md`*.

### 2. Show what changes on GitHub

- **Refresh:** summarize the diff against the current generated block — sections added/removed/rewritten — and confirm the preserved hand-written parts are untouched.
- **First run on a non-empty body:** show what happens to the existing content (preserved above/below the markers, or replaced if the user confirmed that in Step 1).
- **New PR:** state title, base branch, and that it will be created as a **draft**.
- **Artifacts commit:** when `{artifacts_to_commit}` is non-empty, list the files that will be committed and pushed to **`{artifacts_commit_target}`** (the BMad output repo when `{artifacts_external_repo}` is true, otherwise the PR branch) with the rendered `{workflow.artifact_commit_message_template}` so their origin links go live. State the target remote (`{artifacts_remote_url}` or the PR repo origin). Approving the draft approves this commit+push too — say so explicitly.

### 3. Flag honesty gaps

List anything the draft marks as pending, partial, or unverified (evidence pending, unchecked checklist items, partial ACs, secrets-scan false positives the user confirmed) so the user can resolve them now or knowingly publish them.

### 4. Collect the decision

Accept:

- `apply` / `yes` — proceed to Step 5
- `edit <section>: <instruction>` — revise that section, re-present (repeat as needed)
- `title: <new title>` — override the title (must still contain `{ticket_key}` — refuse otherwise)
- `keep title` — leave the existing PR title unchanged (only if it already contains the ticket key)
- `add screenshots: <paths>` — embed and re-present
- `cancel` — stop; nothing was posted

**HALT** — waiting for approval or edits. Do not proceed until the user approves the exact draft shown.

## NEXT

Read fully and follow: `./step-05-apply.md`
