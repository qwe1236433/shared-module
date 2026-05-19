# cross-agent-sync

Workflow protocol for two (or more) AI agents working in different worktrees of the same repository. Defines the consensus layer, the five rules (R1-R5), session-start and session-end checklists, and failure-mode recovery procedures. Prevents silent overwrite, stale-pickup, and unintegrated-commit problems that occur when agents share `.git` but not working trees.

## What's in this folder

- `README.md` — this file (overview + how to adopt)
- `PROTOCOL.md` — the protocol itself (R1-R5, checklists, failure modes)

## When to use

Adopt this workflow when:

- Your repository hosts two or more AI agents (e.g. Claude + Codex, or any two specialized agents)
- Each agent works in its own worktree of the same git repository
- The agents share consensus-layer documents (design docs, handoff, audit ledger) that both touch
- You've experienced or want to prevent: agents claiming different "current truth" for the same file, picking up tasks based on stale single-branch logs, or silently overwriting each other's work

## How to use

1. Read `PROTOCOL.md` end-to-end before activation.
2. Define your project's **consensus-layer file set** (see PROTOCOL §3). Typical: design docs, handoff checkpoint, audit ledger, agent-execution rules. Exclude runtime code and project-specific artifacts.
3. Define your project's **worktree map** (see PROTOCOL §2). Each agent's worktree path + primary occupant.
4. Bind each agent's instruction file (`CLAUDE.md`, `AGENTS.md`, or equivalent) to follow this protocol when touching consensus-layer files.
5. Adopt the **session-start checklist** (PROTOCOL §5) and **session-end checklist** (PROTOCOL §6) as mandatory.
6. When R5 conflicts occur, escalate to the user as adjudicator.

## Variables to localize

When using this protocol, replace these placeholders with your project's actual values:

| Placeholder | What it represents | Example |
|---|---|---|
| `{{REPO_ROOT}}` | Repository root path | `C:\Users\me\Desktop\my-project\` |
| `{{AGENT_A_NAME}}` | First agent's name | `Claude` |
| `{{AGENT_B_NAME}}` | Second agent's name | `Codex` |
| `{{AGENT_A_WORKTREE}}` | First agent's worktree relative path | `.claude/worktrees/agent-a/` |
| `{{AGENT_A_INSTRUCTION_FILE}}` | First agent's per-agent rules | `CLAUDE.md` |
| `{{AGENT_B_INSTRUCTION_FILE}}` | Second agent's per-agent rules | `AGENTS.md` |
| `{{CONSENSUS_LAYER}}` | Your project's consensus-layer file set | see below |

Typical consensus-layer file set:

- `docs/design/*` (architecture, contracts, data flow, decisions, roadmap)
- `docs/dev/SHARED_PROTOCOL.md` (this protocol's installation)
- Current handoff checkpoint (single file)
- Audit / finding ledger (single file)
- Per-agent instruction files (each owned by one agent, with user approval)

## Pairs naturally with

- `agent-checkpoint-protocol/` — defines the checkpoint format that this protocol's R5 conflict adjudication refers to
- Rule files: `preflight-gate.md` (session-start gate), `plan-approval-gate.md` (before edits)

## Version

v1.0.0 (extracted 2026-05-18, source: dome-TV `docs/dev/CROSS_AGENT_SYNC.md`)
