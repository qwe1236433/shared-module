# agent-checkpoint-protocol

Workflow protocol defining the **checkpoint** as the state unit that AI agents synchronize on. Replaces "agent reads chat history" with "agent reads a committed file at a known path". Includes checkpoint fields, task status vocabulary, finding state vocabulary, ownership boundary table, and checkpoint template.

## What's in this folder

- `README.md` — this file (overview + adoption guide)
- `PROTOCOL.md` — the protocol itself (vocabulary, template, rules)

## When to use

Adopt this workflow when:

- Two or more agents (or one agent across sessions) need to pick up state from prior work
- You want to stop trusting chat memory or `git log` summaries as project state
- You need a single point of truth for "where the work is right now" that both agents read before acting
- You've experienced or want to prevent: agents claiming work is `done` when validation never ran, agents using inconsistent task vocabulary (`done` vs `completed` vs `fixed`), or findings disappearing between sessions

## How to use

1. Read `PROTOCOL.md` end-to-end before activation.
2. Choose where the checkpoint lives. Recommend: one file at a known path (e.g. `docs/design/HANDOFF.md` or `docs/dev/CHECKPOINT.md`).
3. Bind agents to read the checkpoint before starting any multi-agent task, and to update it before declaring work done.
4. Adopt the task status vocabulary (PROTOCOL §4) and finding state vocabulary (PROTOCOL §5). Reject other status words (no `done`, no `fixed`, no `green` without evidence).
5. Use the checkpoint template (PROTOCOL §7) verbatim — the field set is the protocol, not a suggestion.

## Variables to localize

When using this protocol, replace these placeholders with your project's actual values:

| Placeholder | What it represents | Example |
|---|---|---|
| `{{CHECKPOINT_FILE}}` | Path to the current checkpoint file | `docs/design/06_HANDOFF.md` |
| `{{BLUEPRINT_FILE}}` | Path to the project's blueprint / design-truth file | `docs/design/00_BLUEPRINT.md` |
| `{{AUDIT_LEDGER_FILE}}` | Path to the finding ledger | `docs/design/07_AUDIT_STATUS.md` |
| `{{AGENT_INSTRUCTION_FILES}}` | Per-agent execution rule files | `CLAUDE.md`, `AGENTS.md` |
| `{{REPORT_TEMPLATE_FILE}}` | (Optional) Report format reference | `docs/design/REPORT_TEMPLATES.md` |

## Pairs naturally with

- `cross-agent-sync/` — multi-worktree coordination; this protocol's checkpoint is what R5 conflict adjudication operates on
- Rule files: `preflight-gate.md` (must load checkpoint before acting), `plan-approval-gate.md` (checkpoint records the trigger)

## Version

v1.0.0 (extracted 2026-05-18, source: dome-TV `docs/dev/AGENT_SYNC.md`)
