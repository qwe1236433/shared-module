# Agent Checkpoint Protocol

Shared checkpoint protocol for two or more AI agents working in the same repository. Agents synchronize on repository checkpoints, not chat memory.

## 1. Responsibility Boundary

Define which file owns what. Adapt the table to your project; the principle is one owner per concern.

| File | Owns | Must Not Own |
| --- | --- | --- |
| `{{BLUEPRINT_FILE}}` | Global project reality: invariants, system boundaries, data ownership, quality priorities. | Agent workflow, checkpoint fields, status vocabulary, report templates. |
| this protocol file | Checkpoint protocol and task/finding status vocabulary. | Project architecture facts, system ownership, data-flow truth, agent execution workflow. |
| `{{CHECKPOINT_FILE}}` | Current checkpoint only. | Historical log, audit ledger, global blueprint. |
| `{{AUDIT_LEDGER_FILE}}` | Finding ledger and audit status. | Current task checkpoint or agent workflow rules. |
| `{{AGENT_INSTRUCTION_FILES}}` | Agent-specific execution rules. | Shared checkpoint state or global design facts. |

If these files disagree, use the table above to decide which file is stale.

## 2. State Unit

The shared state unit is a **checkpoint**.

A checkpoint records the current task state at a stable handoff point. It is not a full history log, and it is not a replacement for design docs, audit status, or git history.

Current checkpoint location:

```text
{{CHECKPOINT_FILE}}
```

## 3. Checkpoint Fields

Every checkpoint must record:

- checkpoint id
- timestamp
- owner agent
- task scope
- task status (from §4 vocabulary)
- files changed
- design facts changed
- findings state changes (from §5 vocabulary)
- checks run
- Boundary Re-Entry result
- Blueprint Impact result
- hot zones
- blockers
- next safe task

If a field is not applicable, write `none` with a concrete reason. Do not omit.

## 4. Task Status Vocabulary

Use only these task states:

- `proposed` — scoped but not started
- `working` — actively being changed or reviewed
- `input_required` — blocked on user / design decision
- `completed` — finished with checks and repository state synchronized
- `failed` — attempted and failed; reason recorded
- `deferred` — intentionally postponed with owner / next condition
- `superseded` — replaced by a newer checkpoint, task, or decision

Do NOT use `done`, `fixed`, or `green` as task status without evidence.

## 5. Finding State Vocabulary

Use only these finding states:

- `new`
- `confirmed`
- `fixed`
- `deferred`
- `false_positive`
- `needs_design_decision`
- `needs_boundary_check`

A finding is `fixed` only when the code / docs changed AND validation ran, or an exact skip reason is recorded.

## 6. Checkpoint Rules

- Read the latest checkpoint before starting any multi-agent task.
- Read this protocol file before editing the checkpoint.
- Do not rely on chat memory as project state.
- Do not overwrite another agent's hot zone without reading the latest checkpoint and current git status.
- Do not mark a design task `completed` unless the matching design doc was updated or the checkpoint explains why no update was required.
- Do not mark a runtime finding `fixed` unless a test, smoke, validator, or exact skip reason is recorded.
- If audit status and checkpoint disagree, treat the audit ledger as the finding ledger and repair the checkpoint.

## 7. Checkpoint Template

Use verbatim. The field set is the protocol, not a suggestion.

```md
## Current Checkpoint

Checkpoint ID:
Timestamp:
Owner Agent:
Task Scope:
Status:

## Files Changed

- ...

## Design Facts Changed

- ...

## Findings State Changes

- ...

## Checks Run

- ...

## Boundary Re-Entry Result

- ...

## Blueprint Impact

- ...

## Hot Zones

- ...

## Blockers

- ...

## Next Safe Task

- ...
```

## 8. Ownership Reference (example mapping)

This is an example mapping for a two-agent project (Claude + Codex). Adapt to your setup.

- `AGENTS.md` — code-agent execution rules
- `CLAUDE.md` — director-agent execution rules
- this protocol file — shared state protocol
- `{{CHECKPOINT_FILE}}` — current checkpoint
- `{{AUDIT_LEDGER_FILE}}` — finding state ledger
- `{{REPORT_TEMPLATE_FILE}}` — report and handoff formatting examples

## 9. Version

| Field | Value |
| --- | --- |
| Source version | dome-TV `docs/dev/AGENT_SYNC.md` (effective 2026-05) |
| Portable version | v1.0.0 (extracted 2026-05-18) |
| Changes from source | Replaced project-specific file paths with `{{PLACEHOLDER}}` variables; kept vocabulary, field set, rules, and template verbatim |
