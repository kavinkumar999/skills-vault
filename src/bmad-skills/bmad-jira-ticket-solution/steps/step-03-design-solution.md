---
---

# Step 3: Design the Solution Plan

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}` — but compose the **plan** in `{workflow.reply_language}`
- Render only the sections in `{workflow.plan_sections}`, in that order
- The plan must be implementable by someone who has not seen this conversation — concrete files, methods, and steps
- No causal claim without an evidence cite from Step 2; mark anything unproven as an assumption

## INSTRUCTIONS

Draft `{plan}` — a single markdown document. Lead with a short header block: ticket key + summary, type, component(s), and **Scope** (one line; if Step 2 found the ticket should be split, say so here and scope this plan to one coherent piece).

Render each section in `{workflow.plan_sections}`:

1. **problem** — the problem in 2–4 sentences, from the ticket and confirmed by Step 2. What is wrong / what is needed, and the observable impact. For bugs, include the trigger and the symptom.

2. **root_cause** — *(bugs)* the mechanism, stated as cause→effect and anchored to `file:line`: what input/state, what the code does, why it is wrong. *(features)* the integration analysis: where the capability plugs in and why there. If more than one cause survived Step 2, present the ranked set and the discriminating evidence.

3. **evidence** — the `{verified_facts}` table from Step 2 (Fact | Evidence | Implication). This is what makes the plan trustworthy; keep it.

4. **approach** — the chosen solution, concretely: which files/classes/methods change and how, in prose a reviewer can follow. Name the pattern being followed (cite an existing example). Tie the approach back to the facts that justify it.

5. **alternatives** — options considered and **why rejected** (one line each). A plan with no alternatives reads as unconsidered; include at least the obvious "do it the other way" and the "do nothing / mitigate" options where relevant.

6. **acceptance_criteria** — numbered, testable criteria the implementation must satisfy. Derive from the ticket's ACs when present (preserve their IDs); otherwise author them from the problem. Each AC must be checkable by a test or an observation.

7. **implementation_steps** — an ordered, concrete checklist a developer follows: the change per file, in dependency order, with decisions flagged ("drop the in-Java filter — guaranteed by the query; note in PR"). This is the hand-off to `{workflow.handoff_skill}`.

8. **test_plan** — what proves each AC: unit tests (name the class/behaviors), integration/regression coverage, and any manual/repro step (for bugs, the ticket's repro turned into a verification). Map tests to ACs.

9. **risk_rollback** — what could break, blast radius, and how to undo: revert-safe? migration down-script? feature flag? deploy-order constraint? Be honest and short — written for an incident responder.

10. **ticket_corrections** — *(conditional)* only when Step 2 found the ticket/comments contradicted by the code. State the claim, the evidence that disproves it, and the correction. Omit the section if there is nothing to correct.

11. **open_questions** — the assumptions and unknowns from Step 2 that need a human/runtime answer before or during implementation, as a checklist. Never bury these inside the approach.

12. **out_of_scope** — what this plan deliberately does not cover (including any split-out work from the scope check), so reviewers don't expect it.

Assemble `{plan}` with the header block followed by the rendered sections. Keep it tight — a reviewer's time is the budget; prefer tables for mappings and short paragraphs over walls of text.

## NEXT

Read fully and follow: `./step-04-present-plan.md`
