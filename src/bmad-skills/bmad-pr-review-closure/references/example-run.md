# Example Run — PR Review Closure

## Copilot only

```text
User: Close copilot comments
Scope: copilot
```

Triage C1–C3 → user: `fix C1, defer C2 — waiting on schema, no_action C3` → push fix → reply + resolve each Copilot thread.

## Human only

```text
User: Address reviewer feedback
Scope: human · Reviewers: @alice
```

Triage H1 (code blocker), H2 (pr_description) → fix both → Issue/Resolution replies → summary comment @alice.

## Both (one run)

```text
User: Close all PR review feedback
Scope: both
```

Copilot threads first in execution plan (reply+resolve), then human items, then human summary comment.

Report: `_bmad_output/pr-reviews/pr-42-review-closure.md`

## Legacy skills

Replaces **bmad-copilot-review-closure** and **bmad-pr-reviewer-response**. Prior reply markers from those skills are still detected as answered.
