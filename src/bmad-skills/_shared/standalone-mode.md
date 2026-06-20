# Standalone Mode (No BMad Installed)

Use this when `{project-root}/_bmad/bmm/config.yaml` does not exist — for example,
the skill is symlinked into Cursor (`~/.cursor/skills/`) without running
`npx bmad-method install`.

## Detect standalone mode

Standalone when **any** of these are true:

- `{project-root}/_bmad/bmm/config.yaml` is missing
- `{project-root}/_bmad/scripts/resolve_customization.py` is missing
- The customization script fails because `_bmad` is not present

Tell the user once: *Running in standalone mode (BMad config not found). Using skill defaults.*

## Resolve workflow without the script

Read and merge the `workflow` block manually from available files only:

1. `{skill-root}/customize.toml` — always
2. `{project-root}/_bmad/custom/{skill-name}.toml` — if exists
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — if exists

Merge rules: scalars override; tables deep-merge; arrays of tables keyed by
`code` or `id` replace matching entries and append new ones; all other arrays append.

## Config defaults (replace BMad `config.yaml`)

| Variable | Default |
| --- | --- |
| `{project_name}` | Basename of `{project-root}` (or `gh repo view --json name -q .name`) |
| `{user_name}` | `gh api user -q .login` if `gh` works; otherwise `"there"` |
| `{communication_language}` | English; match the user's language if they consistently write in another |
| `{document_output_language}` | Same as `{communication_language}` |
| `{user_skill_level}` | `intermediate` |
| `{implementation_artifacts}` | `.bmad-output` (create if missing) |
| `{date}` | Current datetime at activation |
| `{project_context}` | Contents of `{project-root}/**/project-context.md` if any file matches |

Report paths still resolve under `{implementation_artifacts}/pr-reviews/`.

## Token budget

Read `{skill-root}/../_shared/token-budget.md` when present. Compact artifacts
(`*-digest.md`, `*-feedback-index.md`, `*-compact-analysis.md`) are written under
`_bmad_output/` so later steps do not re-carry raw diffs, threads, or ticket dumps.

## What to skip

- Do **not** run `resolve_customization.py` — merge TOML manually as above.
- Do **not** run `workflow.on_complete` via the script at the end of a workflow.
  If `on_complete` in the merged workflow is non-empty, follow it as plain text.

## Story files and BMad artifacts

Without BMad, story files may not exist under `{implementation_artifacts}`. That is
fine — **bmad-pr-describe** skips AC mapping when no story is found; **bmad-pr-describe**
`bmad_artifacts` section omits missing paths. Do not invent story content.

## Team overrides without full BMad

Projects can still drop `{project-root}/_bmad/custom/{skill-name}.toml` (or
`.user.toml`) with workflow overrides even when `config.yaml` is absent — merge
those files when present.
