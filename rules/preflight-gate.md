# preflight-gate

Mandatory self-check an agent must output and satisfy before any planning, editing, reviewing, summarizing, or memory modification. Forces explicit recall of task type, affected layer, required context, and approval needs before action.

## When to apply

Before any substantive task. Skip only for routine acknowledgements, status reports, or quick factual confirmations.

## Format

The agent must output (and satisfy) every field below before proceeding.

```text
1. Task type:
   planning / implementation / review / refactor / documentation / audit / handoff / memory-maintenance

2. Affected layer:
   blueprint / architecture / contracts / data flow / runtime / tests / roadmap / audit / handoff / memory / none

3. Plan / Approval Gate:
   required / not_required
   Reason:

4. Required reading:
   - shared state file (e.g. AGENT_SYNC.md): loaded / not_needed / missing
   - latest checkpoint (e.g. 06_HANDOFF.md): loaded / not_needed / missing
   - blueprint file (e.g. 00_BLUEPRINT.md): loaded / not_needed / missing
   - relevant design / contract / source files: loaded / not_needed / missing
   - git status and changed files: loaded / not_needed / missing
   - relevant tests: loaded / not_needed / missing

5. Blueprint Impact pre-check:
   design_fact_may_change / implementation_only / documentation_only / memory_only / unclear

6. Boundary Re-Entry trigger:
   triggered / not_triggered / unclear
   Trigger evidence:

7. Can proceed:
   yes / no
```

## Rules

- If any required item is `missing`, the agent must stop and load it (or ask the user) before proceeding.
- If `Can proceed: no`, the agent must NOT edit files. State the blocker and route to the appropriate next action.
- If `Plan / Approval Gate: required`, the agent must enter plan mode and obtain user approval before any edits.

## Why this exists

Without a preflight gate, agents tend to start editing before they understand:

- which layer of the project the edit touches
- what design facts may shift as a result
- which files need to be loaded as context before the edit is safe
- whether the change crosses a module/contract boundary

A preflight gate makes those checks visible to the user and the agent, preventing silent assumption-based edits.

## How to install

- User-global: copy into `~/.claude/rules/preflight-gate.md`
- Project-local: paste into project `CLAUDE.md` / `AGENTS.md` as a mandatory `§Preflight Gate` section

## Variables to localize

When using this rule, replace generic file names with the target project's actual files:

- `AGENT_SYNC.md` → project's shared state protocol (if any)
- `06_HANDOFF.md` → project's current checkpoint file
- `00_BLUEPRINT.md` → project's blueprint / design-truth file
