---
---

# Step 3: Triage — Validate Against Code and PR

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Read code at cited lines and the current PR description before judging validity
- Classify **what kind of work** each item needs — not everything is a code fix

## INSTRUCTIONS

For each item in `{feedback_items}`:

1. **Read context** — file at `path:line`, related tests, PR body, linked tickets.

2. **Assess validity:**
   - **valid** — reviewer is correct; action needed
   - **partially_valid** — core concern right, scope or approach debatable
   - **invalid** — incorrect, already addressed, or misunderstanding
   - **needs_clarification** — cannot verify without user input

3. **Classify work type (`fix_kind`):**

   | fix_kind | When |
   | --- | --- |
   | `code_change` | Patch source, tests, or config |
   | `pr_description` | Update PR body (evidence, context, checklist) |
   | `evidence` | Add proof: test output, logs, screenshot, link |
   | `docs` | README, comments, ADR |
   | `reply_only` | Clarification sufficient, no repo change |
   | `decision_needed` | Ambiguous — ask user |

4. **Recommend disposition:**

   - `fix` — valid, should address now
   - `defer` — valid but not this PR (draft reason)
   - `no_action` — invalid or already done (draft pushback)
   - `decision_needed` — user must choose

5. **Record triage entry:**

   ```text
   id, severity, validity, fix_kind, recommendation, title, rationale,
   suggested_resolution, draft_response_issue, draft_response_resolution
   ```

## NEXT

Read fully and follow: `./step-04-present.md`
