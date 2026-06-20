# Example Run — Jira Solution Spec

## Full flow with attachments and commands

```text
User: Analyze NCC-4521

Agent: [getJiraIssue → Bug, session refresh timeout]
       [Download error.log, repro.sh → attachments/]
       [Extract C1: curl repro, C2: kubectl logs]

Agent: **Compact analysis — NCC-4521** — review before codebase investigation.
       [one-screen report: hypothesis, investigation plan]
       Run 1 read-only diagnostic command (C1)? yes
       [C1 → HTTP 503]

User: proceed

Agent: [writes compact-analysis.md]
       [investigates per plan: SessionService.refresh, no retry]
       [drafts solution spec with attachment/command validation table]

User: approve

Agent: solution-spec.md ready → invoke bmad-dev-story
```

## Compact analysis gate

```text
User: proceed

Agent: Investigation plan:
       1. rg "SessionService.refresh"
       2. Trace mobile auth adapter
       3. Compare C1 output to error.log line 42

[Step 4 follows this checklist — does not re-read Jira from scratch]
```

## Attachment download failure

```text
Agent: Ticket has error.log (24KB) but download failed.
       Save the file to _bmad_output/ticket-analysis/NCC-4521/attachments/ or paste the stack trace.

User: [pastes trace]

Agent: [continues to compact analysis with attachment evidence from paste]
```

## MCP unavailable

```text
Agent: Paste summary, AC, commands, and log contents for NCC-4521.

User: [pastes including curl repro command]

Agent: [compact analysis → proceed → investigation]
```
