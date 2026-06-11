---
---

# Step 3: Triage — Validate Each Copilot Comment

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- Read the actual code at `{path}:{line}` before classifying
- Be conservative: if the suggestion is wrong or risky, recommend **defer** or **no_action**, not fix
- `no_action` = valid pushback; thread still gets a reply explaining why no change is needed, then resolve

## INSTRUCTIONS

For each thread in `{copilot_threads}` (skip `{resume_threads}` — they are resolve-only):

1. **Read context** — open the file at the cited line(s). Read surrounding function/class.

2. **Apply the outdated policy first** — if `is_outdated` is `true`, compare the comment against the **current** code:
   - **Concern no longer applies** (the cited code was changed or removed since the comment) → auto-recommend `no_action` with draft reply: *"The code has changed since this comment was made; it no longer applies."* Note the commit or change that superseded it if identifiable.
   - **Concern still applies** despite the line shift → triage normally below, and note "outdated position, concern still valid" in the rationale.

3. **Assess validity** — is Copilot's suggestion:
   - **Correct and valuable** → candidate `fix`
   - **Partially right** → `fix` with noted scope, or `decision_needed` if ambiguous
   - **Wrong, stylistic-only, or out of scope** → `no_action` (reply explaining why)
   - **Valid but not for this PR** → `defer` with draft reason
   - **Cannot verify without more info** → `decision_needed`

4. **Prefer the suggestion block when present** — if `suggestion_block` is non-empty and you recommend `fix`:
   - Verify the block still applies cleanly to the current code at `path:line` (not outdated, no conflicting local edits).
   - If it applies → set `apply_suggestion: true` and `suggested_change` = "apply Copilot's suggestion block verbatim". Step 5 applies the block as-is instead of re-deriving the edit from prose.
   - If the context has drifted → set `apply_suggestion: false` and describe the manual fix; note why the block can't be used.

5. **Record triage entry:**

   ```text
   id: <integer>
   thread_id: PRRT_...
   recommendation: fix | defer | no_action | decision_needed
   title: <one-line summary>
   rationale: <why this recommendation>
   suggested_change: <concrete fix description, empty if no_action/defer>
   apply_suggestion: true | false
   draft_defer_reason: <if defer, draft reason for user to edit>
   ```

6. **Deduplicate** — if two threads describe the same issue, merge and note merged IDs.

## NEXT

Read fully and follow: `./step-04-present.md`
