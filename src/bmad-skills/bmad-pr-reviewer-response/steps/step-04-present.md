---
---

# Step 4: Present Triage — Wait for User Decisions

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Between step** — show analysis before any change or PR posts
- **HALT** until user assigns an action to every item
- Do not execute fixes in this step

## INSTRUCTIONS

### 1. Present triage table

Group rows by reviewer — every reviewer from `{reviewers}` must appear, even if all their items are `no_action`:

| # | Reviewer | Sev | Kind | Valid? | Rec | Title | Rationale |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | @alice | 🚫 blocker | code | ✅ | fix | Missing null check | Reviewer correct — line 42 can NPE |
| 2 | @alice | 💡 rec | pr_description | ✅ | fix | Add test evidence | PR body lacks test output |
| 3 | @bob | 🚫 blocker | code | ❌ | no_action | Wrong pattern | Already handled in commit abc |

**Severity:** 🚫 blocker · 💡 recommendation · ❓ question  
**Kind:** code · pr_description · evidence · docs · reply_only  
**Rec:** fix · defer · no_action · decision_needed

Below the table, for each **fix** item show:
- Reviewer's words (excerpt)
- Your `suggested_resolution`
- Draft **Issue / Resolution** pair for the PR reply

### 2. Summarize

Per reviewer, then total:

> **@alice:** {B} blockers · {R} recommendations — {F} fix · {D} defer · {N} no_action · {Q} need decision
> **@bob:** …
> **Total:** {F} fix · {D} defer · {N} no_action · {Q} need decision

Tell the user: **after you decide, we implement each fix and post a side-by-side response on the PR** (inline thread or summary comment). Defer and no_action still get replies.

### 3. Resolve `decision_needed` first

**HALT** per item until answered.

### 4. Collect decisions

Accept:

```text
fix 1, 2
fix 2 — update PR description with pytest output from last run
defer 4 — schema migration is separate ticket PROJ-891
no_action 3
```

Parsing:

- `fix N` — implement per `fix_kind` (code, PR body, evidence, docs)
- `defer N — reason` — reply with defer reason, no implementation
- `no_action N` — reply with pushback
- Unmentioned items → **HALT** and ask

For **evidence** items, ask what to attach if not obvious (test log path, screenshot, CI URL).

**HALT** — waiting for your decisions on every item.

### 5. Build `{execution_plan}`

```text
- id: 1, reviewer: alice, action: fix, fix_kind: code_change, thread_id: PRRT_..., issue: ..., planned_resolution: ...
- id: 2, reviewer: alice, action: fix, fix_kind: pr_description, thread_id: ..., issue: ..., planned_resolution: ...
- id: 4, reviewer: bob, action: defer, thread_id: ..., reason: ...
```

### 6. Write the response report

Create `{report_path}` (make the `pr-reviews/` directory if needed):

```markdown
# PR Reviewer Response — PR #{pr_number}

- PR: {pr_url}
- Reviewers: @alice, @bob
- Run started: {date}
- Status: in_progress

## Triage and decisions

| # | Reviewer | Sev | Kind | Recommendation | User decision | Reason/Resolution plan |
| --- | --- | --- | --- | --- | --- | --- |

## Execution results

| # | Reviewer | fix done | posted | commit | url | error |
| --- | --- | --- | --- | --- | --- | --- |
```

Fill the triage table now; the execution table is updated per item in Step 5. If resuming, update the existing file in place instead of overwriting completed rows.

## NEXT

Read fully and follow: `./step-05-execute.md`
