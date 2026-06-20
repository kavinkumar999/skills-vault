---
---

# Step 4: Validate Against the Codebase (Investigation)

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- **Drive this step from `{compact_analysis}` and `{investigation_plan}`** — do not re-interpret the ticket from scratch
- **Read or search before you cite** — no hallucinated file paths, symbols, or line numbers
- Large repos: use semantic search and targeted reads; subagents may parallel-read when many areas are implicated
- When the ticket references a service/repo different from `{project-root}`, say so and limit analysis to what is present — record `{scope_limitation}`

## INSTRUCTIONS

1. **Load investigation inputs:**

   - Read `{compact_report_path}` (or in-memory `{compact_analysis}` from Step 3).
   - Use `{search_queries}` and `{investigation_plan}` as the search checklist — work through it in order; add items only when code reveals new leads.
   - Cross-check **command results** and **attachment evidence** against what the code actually does.

2. **Code discovery (run in parallel when independent):**

   - Semantic search for each investigation-plan area.
   - Exact search (`rg` / grep) for error strings, stack frames, route paths, env vars, and identifiers from attachments and commands.
   - Trace call paths from entry points named in the compact analysis.

   Record `{code_findings}`:

   | Finding | Location | Ties to (AC / command / attachment) |
   | --- | --- | --- |
   | Timeout in refresh flow | `src/auth/session.ts:88-120` | C1 repro, `error.log` |

3. **Re-run ticket commands against local/dev when useful:**

   - If Step 3 left commands unrun and local env is available, run **approved** repro/diagnostic commands and compare output to attachment evidence.
   - Record `{command_validation}` — command ID → expected (from ticket) vs observed (from run) vs code explanation.

4. **Build the validation table `{validation}`:**

   | Ticket claim | Evidence (attachment / command / code) | Verdict |
   | --- | --- | --- |
   | "Login fails on mobile" | `error.log` + `MobileAuthAdapter` | ✅ Confirmed |
   | "Missing retry on 503" | C1 returns 503; no retry in `HttpClient` | ✅ Confirmed gap |

   Verdicts: **Confirmed**, **Partial**, **Not found**, **Contradicted**, **Out of scope**.

5. **Root-cause hypothesis `{root_cause}`:**

   - Update the Step 3 hypothesis with **file:line** evidence.
   - Rank by confidence (High / Medium / Low). Note what attachment or command result supports each.

6. **Scope and blast radius** → `{risk_signals}` for Step 5.

7. **Open questions `{open_questions}`** — carry forward gaps from compact analysis; add any surfaced by code.

8. **Select recommended agent** from `{workflow.agent_routes}` → `{agent_code}`, `{agent_label}`, `{agent_prompt_hint}`.

9. **Report investigation summary** — findings count, validation verdicts, command/attachment alignment, recommended agent. If **no relevant code** in `{project-root}`, **HALT** and ask whether to switch repo or continue Jira-only.

## NEXT

Read fully and follow: `./step-05-draft-solution-spec.md`
