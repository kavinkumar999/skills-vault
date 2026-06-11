---
---

# Step 4: Present Triage — Fix or Defer (Between Step)

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- This is the **between** presentation — show recommendations **before** any code change, reply, or resolution
- **HALT** after presenting until the user responds with explicit decisions
- Do not execute fixes in this step

## INSTRUCTIONS

### 1. Present the triage table

Render every thread in a numbered table:

| # | File | Rec | Recommendation | Rationale |
| --- | --- | --- | --- | --- |
| 1 | `path:line` | 🔧 fix | Short title | One sentence |
| 2 | `path:line` | ⏸ defer | Short title | Draft defer reason |
| 3 | `path:line` | ✋ no_action | Short title | Why no change needed |
| 4 | `path:line` | ❓ decision | Short title | What you need from user |

**Legend:** 🔧 fix (code change + reply + resolve) · ⏸ defer (reply with defer reason + resolve — **no code change, thread still closed**) · ✋ no_action (reply explaining why + resolve) · ❓ decision_needed

Tell the user explicitly: **every choice ends with a reply on the Copilot thread and thread resolution.** Defer does not mean "come back later and leave the thread open."

Below the table, for each `fix` item, show Copilot's comment excerpt (first ~200 chars) and your `suggested_change`.

### 2. Summarize counts

> **Copilot triage:** {F} fix · {D} defer · {N} no_action · {Q} need your decision

### 3. Resolve `decision_needed` items first

For each ❓ item, ask a short specific question. **HALT** until answered. Update recommendation to fix, defer, or no_action.

### 4. Collect user decisions

Ask the user to respond with their choices. Accept formats like:

```text
fix 1, 2, 4
defer 3 — waiting on API schema from platform team
no_action 5
```

Or:

```text
fix all
defer 3
```

Parsing rules:

- `fix all` / `fix everything` → all items recommended as fix
- `fix 1, 2, 3` → explicit fix list
- `defer N` → must include reason inline or in next message
- `no_action N` → reply explaining pushback, no code change
- Any item not mentioned → **HALT** and ask (do not assume)

For each **defer**, if reason is missing, ask:

> Quick reason for deferring #{id}? (shown on the PR thread)

**HALT** — waiting for your fix/defer/no_action decisions. Do not proceed until every thread has a final disposition.

### 5. Build `{execution_plan}`

After user confirms, build an ordered list:

```text
- id: 1, action: fix, thread_id: PRRT_..., apply_suggestion: true|false, summary: ...
- id: 3, action: defer, thread_id: PRRT_..., reason: ...
```

Append any `{resume_threads}` as `action: resolve_only` entries (no reply — they already carry one).

Store `{execution_plan}` for Step 5.

### 6. Write the closure report

Create `{report_path}` (make the `pr-reviews/` directory if needed) recording the state so far:

```markdown
# Copilot Review Closure — PR #{pr_number}

- PR: {pr_url}
- Run started: {date}
- Status: in_progress

## Triage and decisions

| # | thread_id | File | Recommendation | User decision | Reason/Summary |
| --- | --- | --- | --- | --- | --- |

## Execution results

| # | thread_id | replied | resolved | commit | error |
| --- | --- | --- | --- | --- | --- |
```

Fill the triage table now; the execution table starts empty and is updated per thread in Step 5. If resuming, update the existing file in place instead of overwriting completed rows.

## NEXT

Read fully and follow: `./step-05-execute.md`
