---
---

# Step 2: Analyze the Code

## RULES

- YOU MUST ALWAYS SPEAK OUTPUT in `{communication_language}`
- This step is **read-only** — search and read code; never edit it
- Every fact that will feed the plan must trace to a concrete `file:line` you actually read
- Distinguish **verified** (you read the code and it says so) from **inferred** (plausible but unconfirmed)

## INSTRUCTIONS

1. **Locate the entry points** named or implied by the ticket — the component/service, the symptom's surface (an endpoint, a scheduled task, an event handler, a log line, a stack frame). Use `Grep`/`Glob` and the project's structure to find them. Record candidates with paths.

2. **Trace the implicated paths** at the breadth set by `{workflow.analysis_depth}`:

   - `"quick"` — the obvious method(s) and what they call.
   - `"standard"` — the path end-to-end: callers → the suspect code → callees, plus the tests that cover it and the data/config it reads.
   - `"deep"` — standard, plus adjacent subsystems that share state and relevant git history (`git log -p`/`git blame` on the suspect lines to see when/why the behavior was introduced).

   When `{workflow.use_subagents}` is true **and** the trace spans multiple modules, dispatch parallel read-only explorers (the `Explore` agent, or `feature-dev:code-explorer`) — one per subsystem — and have each return file:line findings, not file dumps. Otherwise trace inline. Either way, **you** read the decisive lines yourself before recording them as verified.

3. **For a bug — establish the root cause.** Follow the data and control flow to the line where behavior diverges from intent. State the mechanism: what input/state triggers it, what the code does, why that is wrong. If more than one cause is plausible, rank them and note what evidence would confirm/eliminate each. Do not settle on a cause you cannot point at in code.

4. **For a feature — establish the seams.** Identify where the new behavior plugs in: the interfaces/classes to extend, the data model and persistence touched, the events/messages involved, the config/flags, and the call sites that must change. Note existing patterns to follow (cite an example file).

5. **Build `{verified_facts}`** — a table, each row with evidence and its implication. This is the backbone of the plan's credibility:

   | Fact | Evidence | Implication |
   | --- | --- | --- |
   | `assignedAt` is stored as a Long | `BasicWorkitem.setAssignedAt(Long)` `…:142` | numeric `lte(...,0)` filter is safe |
   | sync runs every 30 min | `QueueEmailCacheSyncTask` `…:38` | spike cadence matches the refresh |

6. **Record assumptions & unknowns** separately — anything you could not confirm in code (runtime data shapes, prod config values, external service behavior). These become the plan's *Open questions*, never silent assumptions baked into the approach.

7. **Cross-check the ticket against the code.** Where a description claim or a comment is contradicted by what the code actually does, record it for the plan's *Ticket corrections* section — with the evidence. (Example pattern: a comment asserting a helper "masks errors as empty" when the code returns null on error.)

8. **Scope check.** From what you found, judge whether the ticket is one coherent change or several. If it is several, note the split — Step 3 recommends it rather than designing an over-large plan.

9. **Report what you found** (concise): the entry points, the root cause or seams (one paragraph), the count of verified facts, and the open questions. This is the raw material the user will see shaped into a plan in Step 4.

## NEXT

Read fully and follow: `./step-03-design-solution.md`
