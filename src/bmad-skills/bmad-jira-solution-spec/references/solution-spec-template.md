# Solution Spec Template

Full artifact: `_bmad_output/ticket-analysis/{ticket_key}-solution-spec.md`  
Builds on: `{ticket_key}-compact-analysis.md` (Step 3)

```markdown
# Solution Spec — {ticket_key}

**Generated:** {date}
**Jira:** [{ticket_key}]({ticket_url})
**Compact analysis:** [compact-analysis.md](./{ticket_key}-compact-analysis.md)
**Attachments:** `./{ticket_key}/attachments/`
**Story file:** {story_file or "—"}
**Repo:** {project_name}

---

## Compact analysis (summary)

{3-line executive summary OR embed full compact report when embed_compact_analysis = "full"}

## Ticket summary

| Field | Value |
| --- | --- |
| Summary | … |
| Type | … |
| Status | … |

## Attachments and commands

### Attachments ingested

| File | Local path | Key extract |
| --- | --- | --- |
| error.log | `ticket-analysis/{key}/attachments/error.log` | … |

### Commands

| ID | Type | Command | Validated? |
| --- | --- | --- | --- |
| C1 | repro | `curl …` | ✅ matches code path |

## Problem statement

…

## Acceptance criteria

| ID | Criterion | Validation |
| --- | --- | --- |
| AC-1 | … | ✅ Confirmed |

## Code validation

| Claim | Evidence (attachment / command / code) | Verdict |
| --- | --- | --- |
| … | `path:line` | Confirmed |

### Key files

- `path/to/file.ts` — …

## Root cause

1. **High** — … (`path:line`) — supported by `error.log`, C1

## Proposed solution

…

## Implementation plan

| # | Task | Files | Size |
| --- | --- | --- | --- |
| 1 | … | … | S |

## Risks

- …

## Test plan

- Repro: run C1 after fix expects 200
- Unit: extend `session.test.ts`

## Open questions

| Question | Blocking? |
| --- | --- |
| … | No |

## Next step — invoke implementation

**Recommended:** `{agent_code}` — {agent_label}

> {agent_prompt_hint}

**Artifacts:** compact analysis + this spec + attachments folder

**Suggested prompt:**

> Implement [{ticket_key}]({ticket_url}) per the solution spec. Start with task 1.
```

Only include sections listed in `{workflow.sections}`.
