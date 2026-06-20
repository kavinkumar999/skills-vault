---
---

# Step 3: Draft the Description

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}` — but compose the **PR body** in `{workflow.reply_language}`
- Render only the sections listed in `{workflow.sections}`, in that order
- **Drive from `{change_digest}` and `{digest_path}`** — do not re-read the raw diff or full story file; cite files from the digest's per-file one-liners
- Reviewer time is the budget: lead with what matters, keep prose tight, prefer tables for mappings
- No claim without a source from the digest / Step 2 gates — test output, or CI checks

## INSTRUCTIONS

### 0. Draft the PR title

Render `{pr_title}` from `{workflow.title_template}`: `{type}` = conventional type from the dominant change (feat/fix/docs/refactor/test/chore), `{scope}` = affected area (drop the parens when no clear scope), `{summary}` = short imperative summary, `{ticket_key}` from Step 2 — **the ticket key is mandatory in the title**. Example: `feat(auth): add session refresh [NCC-1234]`.

For an existing PR whose title differs, propose the new title alongside the body in Step 4 (the user can keep the old one — unless it lacks the ticket key, which you flag as a must-fix).

### 1. Map into the repo template (when `{repo_template}` exists)

The repo's template wins the structure fight: keep **its** headings and order, fill **its** checkboxes honestly, and place each generated section's content under the template heading it belongs to (summary → "Description", evidence → "How was this tested", etc.). Generated sections with no matching heading go at the end of the marked block; template headings you have nothing for stay present but get an honest "n/a — <why>". The marker contract is unchanged: everything generated still lives between the body markers.

When there is no repo template, render `{workflow.sections}` as below.

### 2. Draft the sections

Draft `{generated_block}` — the content that will live between the body markers:

1. **summary** — 2–4 sentences from `{change_digest}` one-line summary + context. Link `{ticket_key}`.

2. **changes** — grouped bullet list from `{change_digest}` per-file one-liners (not a second pass over the diff). Call out breaking changes, migrations, and config changes at the top.

3. **why** — motivation from digest drafting notes or story AC; one short paragraph; skip if summary covers it.

4. **diagram** — only when `{diagram_worthy}` from digest. Mermaid diagram (≤ ~10 nodes) for cross-component flow changes only.

   ````markdown
   ```mermaid
   sequenceDiagram
     Client->>AuthService: refresh(token)
     AuthService->>TokenStore: validate + rotate
     TokenStore-->>AuthService: new session
     AuthService-->>Client: 200 {session}
   ```
   ````

5. **ac_mapping** — only when `{story_file}` exists; AC rows from digest only:

   | AC | Status | Where |
   | --- | --- | --- |
   | AC-1: <criterion> | ✅ Implemented | `src/handler.ts:42`, tests in `handler.test.ts` |
   | AC-2: <criterion> | ⚠️ Partial | <what remains and why> |
   | AC-3: <criterion> | ⏭ Not in this PR | <where it is tracked> |

   Every AC from the story gets a row. Partial or missing ACs are stated plainly — reviewers must not discover gaps themselves.

6. **test_evidence** — render `{test_gates}` as a scannable table, then the proof, then the live CI link:

   ````markdown
   ## Test evidence

   | Gate | Result |
   | --- | --- |
   | `:hndlbar-lib-assembled:test` | ✅ 305 tests, 0 failed |
   | `grep -r RemovedClass` | ✅ 0 matches |
   | Spotless (both modules) | ✅ clean |

   <details><summary>Raw output (local run, {date})</summary>

   ```
   SomeSuiteTest   tests=20 failures=0
   BUILD SUCCESSFUL in 29s
   ```
   </details>

   CI: live status on the [Checks tab]({pr_url}/checks).
   ````

   Rules: one row per gate with ✅/❌ and the counts from Step 2 — short gate names, never full wrapped command lines (the full command belongs in the raw block). The `<details>` block embeds `{evidence_raw}` verbatim with the run date — omit the block only when no local run happened. The CI line is always the Checks-tab link; **never** render a "pending at time of writing" snapshot. A ❌ row appears only when the user explicitly chose to publish with a failing gate, with a one-line honest note.

7. **screenshots** — embed user-provided paths/URLs with one-line captions. Omit the section when not UI-facing.

8. **risk_rollback** — only when `{risk_signals}` is non-empty. For each signal: what could break, blast radius, and the rollback path (revert-safe? migration down-script? flag to flip? deploy-order constraint?). Honest and short — this section exists so an incident responder at 2am knows how to undo this PR:

   ```markdown
   ### Risk & rollback
   - **Migration `0042_add_session_table`** — additive, no backfill; rollback = revert + `migrate down 0042`.
   - **Config: `SESSION_TTL` added** — missing value falls back to 3600s; no deploy-order constraint.
   ```

9. **bmad_artifacts** — lead with the directory tree link (the "all BMad output" reference), then one row per artifact:

   ```markdown
   ### BMad artifacts

   All BMad output for this PR: [`{artifacts_tree_repo_path}/`](https://github.com/{owner}/{repo}/tree/{head_branch}/{artifacts_tree_repo_path})

   | Artifact | Tracked path | Link |
   | --- | --- | --- |
   | Story | `<tracked_repo_path>` | [filename](https://github.com/{owner}/{repo}/blob/{head_branch}/<tracked_repo_path>) |
   ```

   Use tracked paths from `git ls-files` — never `_bmad_output/` in links. Include `{digest_path}` as a linked artifact when tracked. Links go live after Step 5 push. Omit section when `{bmad_artifacts}` is empty.

10. **checklist** — render `{workflow.checklist_items}` as `- [x]` / `- [ ]` based on what Step 2 actually verified. The secrets item may be pre-checked **only** when the Step 2 scan ran clean. Never pre-check an item you did not verify.

11. **reviewer_notes** — where to start reading, known trade-offs, anything deliberately out of scope. This is the section reviewers thank you for; one short list.

Assemble the draft body:

```text
{preserved_before}
{workflow.body_marker_begin}
<generated_block>
{workflow.body_marker_end}
{preserved_after}
```

## NEXT

Read fully and follow: `./step-04-present.md`
