# plan-approval-gate

An agent must enter Plan Mode and obtain explicit user approval before writing code or editing files when the task crosses any of the trigger conditions below. Prevents broad, irreversible, or boundary-crossing changes from happening on assumed authority.

## Trigger conditions

Plan mode + user approval is REQUIRED if the task does any of:

- Touches more than 3 files
- Deletes, moves, overwrites, regenerates, or mass-rewrites files
- Changes architecture, module boundaries, contracts, data flow, defaults, or entrypoints
- Affects generated, runtime, historical, or user-authored assets
- Performs broad refactor (more than one localized concern)
- Introduces new dependencies, schemas, or directories
- Touches manifests, validators, CI gates, or deployment configuration
- Modifies user-facing copy, IDs, names, or public API

If unsure whether a trigger applies, treat it as triggered and ask.

## What "plan mode" means

The agent stops, lays out:

1. **Scope** — exact files / modules to be touched
2. **Behavior change** — what the system will do differently after the change
3. **Risk** — what could break, what's irreversible, what tests need to run
4. **Alternatives considered** — at least one rejected alternative with reasoning
5. **Approval ask** — explicit "proceed?" question to the user

Only after the user answers `proceed` may the agent edit.

## What "not triggered" means

If the task is:

- Editing one file, localized concern
- Bug fix with limited blast radius
- Documentation typo or wording tweak
- Adding a test, comment, or example
- Reverting a recent change the user authorized

...the agent may proceed without plan mode, but should still output a Preflight Gate (see `preflight-gate.md`).

## How to install

- User-global: copy into `~/.claude/rules/plan-approval-gate.md`
- Project-local: paste into project `CLAUDE.md` / `AGENTS.md` as a `§Plan / Approval Gate` section

## Why this exists

Agents asked to "just do X" often expand X without realizing — touching 7 files when X seemed like 1, or refactoring an interface to make X cleaner. The user then discovers the expansion only after the edits are committed. The plan-approval-gate forces the agent to make scope visible before edits, so the user can adjust scope or risk acceptance early.
