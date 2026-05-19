# shared-module

Common modules library.

## Directory layout

### `skills/`
Claude Code skills — packages that extend Claude's behavior when triggered by user requests. Each skill is a self-contained folder with a `SKILL.md` file plus optional reference and template subfolders. Installed by copying the folder into `~/.claude/skills/` or `<project>/.claude/skills/`.

### `workflows/`
Multi-step procedures for repeatable tasks (e.g. audit flow, review flow, migration flow). Each workflow is a folder with a `README.md` describing the steps, plus optional checklists, templates, or supporting scripts. Used by reading the README and following the steps.

### `scripts/`
Standalone executables (Python, bash, Node, etc.) that solve one well-scoped problem each. Each script is a folder (not a bare file) containing the main file, dependencies file, README, and optional examples. Used by copying the folder and running per its README.

### `rules/`
Behavior rules — short markdown files containing global instructions for Claude or other agents. Single-concern, declarative. Used by copying content into `~/.claude/rules/` or a project's `CLAUDE.md`.

### `templates/`
Document and code skeletons — starter files for repeatable artifacts (design doc structure, PR description, ADR format, etc.). Each template is a folder with the skeleton file plus a README explaining when to use it and what variables to fill.
