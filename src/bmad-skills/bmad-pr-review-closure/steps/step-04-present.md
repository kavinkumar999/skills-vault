---
---

# Step 4: Present Triage — Wait for Decisions

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **HALT** after presenting — no code changes, replies, or pushes in this step

## INSTRUCTIONS

### 1. Present unified table (from `{feedback_index}` — excerpts only)

| # | Source | File | Rec | Title | Rationale |
| --- | --- | --- | --- | --- | --- |
| C1 | Copilot | `path:line` | fix | … | … |
| H1 | @alice | `path:line` | fix | … | … |

Do **not** repeat full thread bodies in chat — reference ID; full text is in `{report_path}` appendix. Show Copilot `suggestion_block` only for `fix` items with `has_suggestion: true` (load from appendix).

**Rec:** fix · defer · no_action · decision_needed

**Copilot:** every choice → reply + **resolve thread**.  
**Human:** every choice → **Issue / Resolution** reply; thread resolve only if user opts in later.

Show human draft Issue/Resolution pairs for fix items (compact — reference index ID).

### 2. Summarize

> Copilot: {F} fix · {D} defer · {N} no_action · {Q} decision  
> Human: {F} fix · {D} defer · {N} no_action · {Q} decision

### 3. Resolve `decision_needed` items — **HALT** per item.

### 4. Collect decisions

```text
fix C1, H1
defer H2 — tracked in PROJ-891
no_action C2
```

Unmentioned items → **HALT**. Defer requires reason.

Ask human scope: *Resolve human inline threads after reply? (yes/no — default per `{workflow.human_resolve_threads}`)*

### 5. Build `{execution_plan}`

Include `source`, `action`, `thread_id`, Copilot fields (`apply_suggestion`, `summary`) or human fields (`fix_kind`, `issue`, `resolution`, `reviewer`). Append copilot resume entries as `action: resolve_only`.

### 6. Write `{report_path}`

```markdown
# PR Review Closure — PR #{pr_number}

- PR: {pr_url}
- Scope: {review_scope}
- Reviewers: …
- Status: in_progress

## Triage and decisions
| # | Source | … |

## Execution results
| # | Source | replied/posted | resolved | commit | error |
```

## NEXT

Read fully and follow: `./step-05-execute.md`
