# Skills Vault

Personal collection of agent skills, organized by **family**. Each family groups
related skills for a workflow or tool chain. Families live under `src/` so the
vault can grow without mixing unrelated skills at the repo root.

## Layout

```
skills-vault/
├── .claude-plugin/marketplace.json   # plugin manifest (Cursor / Claude Code)
└── src/
    └── <family-name>/
        ├── README.md                 # family-specific docs and install steps
        ├── <skill-name>/SKILL.md     # one folder per skill
        └── …                         # optional metadata (see family README)
```

## Families

| Folder | Targets | What's inside |
| --- | --- | --- |
| [`src/bmad-skills/`](src/bmad-skills/) | BMad Method, Claude Code | PR lifecycle: describe → Copilot closure → reviewer response |

Each family README covers what its skills do, how to configure them, and any
tool-specific install steps.

## Using skills

How you wire skills in depends on the agent runtime. Use the path that matches
your setup — all examples use `<vault-path>` for this repo's root on your machine.

### Cursor

Add the vault (or individual skill folders) as project or user skills:

- **Project skills** — copy or symlink into `.cursor/skills/` in the target repo
- **User skills** — copy or symlink into `~/.cursor/skills/`
- **Plugin manifest** — register families in `.claude-plugin/marketplace.json`
  so Claude Code-compatible tooling can discover them

### Claude Code

Point at skill folders listed in `.claude-plugin/marketplace.json`, or install
skills from a family's `SKILL.md` paths directly.

### BMad Method

BMad families include `module.yaml` and `module-help.csv` for the installer.
See [`src/bmad-skills/README.md`](src/bmad-skills/README.md) for the full
install command and configuration.

### Other agents (Codex, custom runners)

Copy or symlink the `SKILL.md` folder for the skill you need. No extra metadata
required — the skill file is the contract.

## Adding a new family

1. Create `src/<family-name>/` with one subfolder per skill (each containing
   `SKILL.md`)
2. Add `src/<family-name>/README.md` — what the skills do, which tools they
   target, install steps, and configuration
3. Register in `.claude-plugin/marketplace.json` when the family should appear
   as a plugin (add a `plugins` entry with `source` and `skills` paths)
4. Add BMad metadata (`module.yaml`, `module-help.csv`) only if the family is
   meant for the BMad installer — see `src/bmad-skills/` as a reference
5. Add a row to the **Families** table above

Local paths and git clones both work as sources. Edits in this repo take effect
on the next install, symlink refresh, or agent restart depending on how you
wired the skills in.
