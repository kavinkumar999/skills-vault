---
---

# Step 6: Present, Publish, and Hand Off

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **HALT** after presenting — do not write the solution spec file until the user approves
- Compact analysis artifact was already written in Step 3 — do not overwrite without user consent
- **NEVER** `git add _bmad_output/` — only git-tracked paths from `git ls-files`

## INSTRUCTIONS

### 1. Present the draft

Show `{solution_spec_draft}` in a fenced markdown block. Lead with:

> **{ticket_key}** — {issue_type}: {summary} → handoff: **{agent_code}**
> Compact analysis: `{compact_report_path}`

Highlight:
- Attachment/command evidence vs code validation
- Confirmed vs disputed claims
- Blocking open questions
- Implementation size (S/M/L)

### 2. Collect the decision

- `approve` / `yes` — write solution spec, proceed to Phase A
- `edit <section>: <instruction>` — revise, re-present
- `agent: <code>` — override handoff
- `revisit compact` — return to Step 3 mentally; user edits compact analysis, then re-run from Step 4
- `cancel` — stop

**HALT** until approved.

### 3. Phase A — Write the solution spec

Write `{solution_spec_draft}` to `{report_path}`.

Resolve git-tracked path for `{report_path}` and `{compact_report_path}` when applicable.

### 4. Phase B — Optional commit (`{workflow.commit_spec}`)

When committing, include both artifacts when tracked:

```bash
git add <tracked_compact_path> <tracked_spec_path>
git commit -m "{workflow.spec_commit_message_template}"
git push
```

Also commit `{attachment_dir}` only when attachments are meant to live in-repo and paths are trackable — otherwise reference Jira attachment names only.

### 5. Phase C — Hand off

> **Solution spec ready** — [{ticket_key}]({ticket_url})
>
> Compact analysis: `{compact_report_path}`
> Full spec: `{report_path}`
>
> **Invoke next:** `{agent_code}` — {agent_label}
>
> ```
> Implement {ticket_key} per the solution spec. Compact analysis and attachments are in ticket-analysis/{ticket_key}/.
> {agent_prompt_hint}
> ```

### On Complete

If `{project-root}/_bmad/scripts/resolve_customization.py` exists, run it for `workflow.on_complete`. In standalone mode, read `on_complete` from `customize.toml`. Follow if non-empty.
