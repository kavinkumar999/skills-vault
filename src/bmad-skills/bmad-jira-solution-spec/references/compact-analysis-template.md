# Compact Analysis Template

Written to `_bmad_output/ticket-analysis/{ticket_key}-compact-analysis.md` at the end of Step 3.
**Purpose:** one-screen distillation of Jira + attachments + commands — the checklist Step 4 investigates against.

```markdown
# Compact Analysis — {ticket_key}

**Generated:** {date}  
**Jira:** [{ticket_key}]({ticket_url})  
**Repo:** {project_name}

## Ask (one line)

…

## Ticket facts

| Type | Status | Priority | Assignee |
| --- | --- | --- | --- |
| Bug | In Progress | High | … |

## Problem

**Reporter says:** …  
**Technical read:** …

## Acceptance criteria

1. AC-1: …
2. AC-2: …

## Commands

| ID | Type | Command | Safe? |
| --- | --- | --- | --- |
| C1 | repro | `curl -s …` | yes |

### Command results (if run)

| ID | Exit | Output (truncated) |
| --- | --- | --- |
| C1 | 0 | `HTTP/1.1 503 …` |

## Attachment evidence

- `error.log` — NPE at `SessionService.refresh` line 88
- `repro.sh` — curl against `/api/v1/session/refresh`

## Initial hypothesis

…

## Investigation plan (for codebase step)

1. Search: `SessionService`, `refresh`, `503`
2. Trace: mobile login → session refresh handler
3. Run C1 locally if staging URL available
4. Read tests under `**/session*`

## Gaps / blockers

- …
```

Keep the whole document scannable in &lt; 2 minutes. No `path:line` code citations here — those belong in the solution spec after Step 4.
