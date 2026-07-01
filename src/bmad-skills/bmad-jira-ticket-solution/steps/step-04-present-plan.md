---
---

# Step 4: Present the Plan (Between Step)

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **HALT** after presenting — nothing is written or committed in this step
- The user owns the solution direction; your plan is a proposal

## INSTRUCTIONS

### 1. Show the plan

Render the full assembled `{plan}` in the chat so the user sees exactly what will be written. State where it will land: `{planning_artifacts}/<plan_filename>` (filename from `{workflow.plan_filename_template}`), and — when known — the output repo it will be committed to.

### 2. Flag the honesty gaps

List plainly, so the user can resolve or knowingly accept them:

- **Open questions** — the unverified assumptions the approach rests on.
- **Confidence** — if the root cause is ranked/uncertain rather than proven, say so and name what would confirm it.
- **Scope** — if you recommended splitting the ticket, restate it here.
- **Ticket corrections** — anything in the ticket the code contradicts.

### 3. State what happens on approval

- The plan is written to `{planning_artifacts}/<plan_filename>`.
- Per `{workflow.commit_plan}`: `"ask"` → you will confirm once more before committing/pushing to the output repo; `"always"` → it is committed+pushed on approval (subject to the default-branch guard in Step 5); `"never"` → file only.
- No product code is touched. Implementation is a separate hand-off to `{workflow.handoff_skill}`.

### 4. Collect the decision

Accept:

- `apply` / `yes` — proceed to Step 5 (write the plan)
- `edit <section>: <instruction>` — revise that section and re-present (repeat as needed)
- `dig <question>` — go back to Step 2 to investigate further, then re-draft
- `cancel` — stop; nothing was written

**HALT** — waiting for approval or edits. Do not proceed until the user approves the exact plan shown.

## NEXT

Read fully and follow: `./step-05-write-plan.md`
