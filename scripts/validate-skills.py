#!/usr/bin/env python3
"""Smoke-check skills-vault structure, frontmatter, step links, and metadata."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parent.parent
BMAD_SKILLS = ROOT / "src" / "bmad-skills"
STEP_LINK_RE = re.compile(
    r"Read fully and follow:\s*`\.?/?([^`]+)`",
    re.IGNORECASE,
)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"{path}: missing YAML frontmatter")
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip("'\"")
    return data


def parse_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def resolve_step_link(skill_dir: Path, from_file: Path, target: str) -> Path | None:
    target = target.lstrip("./")
    if target.startswith("steps/"):
        candidate = skill_dir / target
    elif from_file.parent.name == "steps":
        candidate = from_file.parent / target
    else:
        candidate = skill_dir / target
    return candidate if candidate.is_file() else None


# Columns module-help.csv must carry so downstream tooling (and this script) can
# read rows by name without KeyError.
REQUIRED_CSV_COLUMNS = {
    "module",
    "skill",
    "display-name",
    "menu-code",
    "description",
    "phase",
    "preceded-by",
    "followed-by",
    "output-location",
}


def check_step_chain(skill_dir: Path, errors: list[str]) -> None:
    """Every step file must be reachable from step-01 via NEXT links, and the
    chain must be acyclic. Catches orphaned steps and accidental loops that the
    per-link existence check alone lets through."""
    steps_dir = skill_dir / "steps"
    if not steps_dir.is_dir():
        return
    step_files = sorted(steps_dir.glob("*.md"))
    if not step_files:
        return

    edges: dict[Path, list[Path]] = {}
    for step_file in step_files:
        text = step_file.read_text(encoding="utf-8")
        targets: list[Path] = []
        for match in STEP_LINK_RE.finditer(text):
            resolved = resolve_step_link(skill_dir, step_file, match.group(1))
            # Only step→step links form the chain; ignore links into references/.
            if resolved is not None and resolved.parent == steps_dir:
                targets.append(resolved)
        edges[step_file] = targets

    roots = sorted(steps_dir.glob("step-01-*.md"))
    if not roots:
        return  # missing step-01 already reported elsewhere

    reachable: set[Path] = set()
    stack = list(roots)
    while stack:
        node = stack.pop()
        if node in reachable:
            continue
        reachable.add(node)
        stack.extend(edges.get(node, []))

    for orphan in step_files:
        if orphan not in reachable:
            errors.append(
                f"{skill_dir.name}: step '{orphan.name}' is unreachable from step-01 (orphaned NEXT chain)"
            )

    # Cycle detection over the step graph (DFS with a recursion stack).
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[Path, int] = {f: WHITE for f in step_files}

    def visit(node: Path) -> None:
        color[node] = GRAY
        for nxt in edges.get(node, []):
            if color.get(nxt) == GRAY:
                errors.append(
                    f"{skill_dir.name}: step chain has a cycle through '{nxt.name}'"
                )
            elif color.get(nxt) == WHITE:
                visit(nxt)
        color[node] = BLACK

    for root in roots:
        if color[root] == WHITE:
            visit(root)


def main() -> int:
    errors: list[str] = []

    skill_dirs = sorted(
        p for p in BMAD_SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
    )
    if not skill_dirs:
        errors.append(f"No skills found under {BMAD_SKILLS}")
    else:
        csv_path = BMAD_SKILLS / "module-help.csv"
        if csv_path.is_file():
            with csv_path.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                header = set(reader.fieldnames or [])
                rows = list(reader)
            missing_cols = REQUIRED_CSV_COLUMNS - header
            if missing_cols:
                errors.append(
                    f"module-help.csv missing required columns: {sorted(missing_cols)}"
                )
            csv_skills = {row["skill"] for row in rows if row.get("skill")}
            dir_names = {d.name for d in skill_dirs}
            missing_in_csv = dir_names - csv_skills
            extra_in_csv = csv_skills - dir_names
            if missing_in_csv:
                errors.append(f"module-help.csv missing skills: {sorted(missing_in_csv)}")
            if extra_in_csv:
                errors.append(f"module-help.csv unknown skills: {sorted(extra_in_csv)}")

        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            try:
                meta = parse_frontmatter(skill_md)
            except ValueError as exc:
                errors.append(str(exc))
                continue

            name = meta.get("name", "")
            description = meta.get("description", "")
            if not name:
                errors.append(f"{skill_md}: frontmatter missing 'name'")
            elif name != skill_dir.name:
                errors.append(
                    f"{skill_md}: name '{name}' does not match directory '{skill_dir.name}'"
                )
            if not description:
                errors.append(f"{skill_md}: frontmatter missing 'description'")
            elif len(description) > 1024:
                errors.append(f"{skill_md}: description exceeds 1024 characters")

            customize = skill_dir / "customize.toml"
            if customize.is_file():
                try:
                    config = parse_toml(customize)
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"{customize}: invalid TOML — {exc}")
                else:
                    if "workflow" not in config:
                        errors.append(f"{customize}: missing [workflow] table")

            example_run = skill_dir / "references" / "example-run.md"
            if not example_run.is_file():
                errors.append(f"{skill_dir.name}: missing references/example-run.md")

            check_step_chain(skill_dir, errors)

            for step_file in sorted(skill_dir.glob("steps/*.md")):
                text = step_file.read_text(encoding="utf-8")
                for match in STEP_LINK_RE.finditer(text):
                    target = match.group(1)
                    resolved = resolve_step_link(skill_dir, step_file, target)
                    if resolved is None:
                        errors.append(
                            f"{step_file}: broken NEXT link '{target}'"
                        )

            steps_dir = skill_dir / "steps"
            first_steps = sorted(steps_dir.glob("step-01-*.md")) if steps_dir.is_dir() else []
            if not first_steps:
                errors.append(f"{skill_dir.name}: missing steps/step-01-*.md")

    shared = BMAD_SKILLS / "_shared" / "standalone-mode.md"
    if not shared.is_file():
        errors.append(f"Missing {shared}")

    token_budget = BMAD_SKILLS / "_shared" / "token-budget.md"
    if not token_budget.is_file():
        errors.append(f"Missing {token_budget}")

    github_commands = BMAD_SKILLS / "_shared" / "github-commands.md"
    if not github_commands.is_file():
        errors.append(f"Missing {github_commands}")

    if errors:
        print("validate-skills: FAILED\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"validate-skills: OK ({len(skill_dirs)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
