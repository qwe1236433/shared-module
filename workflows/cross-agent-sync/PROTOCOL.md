# Cross-Agent Sync Protocol

Status: portable workflow extracted from a working two-agent setup. Owners: User (adjudicator), Agent A (technical director), Agent B (code programmer). Substitute names per `README.md` variables.

This document is the single source of truth for how two agents stay in sync when they work in different worktrees of the same repository. It is part of the consensus layer.

If this file and the per-agent instruction files disagree, this file wins for inter-agent coordination rules; per-agent instruction files win for agent-local execution rules.

## 1. Role Triad

| Role | Who | Owns |
| --- | --- | --- |
| Adjudicator / direction | User | strategic direction, final approval, conflict resolution, scope and risk acceptance |
| Technical director | Agent A (e.g. Claude) | design, audit, plan, handoff, blueprint impact, consensus-layer documents |
| Code programmer | Agent B (e.g. Codex) | runtime, tests, manifests, execution receipts, implementation of approved plans |

Neither agent may override the other on consensus-layer files without user adjudication.

## 2. Worktree Map

The repository uses multiple worktrees that share a single `.git` directory.

| Worktree | Path | Primary occupant |
| --- | --- | --- |
| main | `{{REPO_ROOT}}` | User + Agent B |
| Agent A worktree | `{{REPO_ROOT}}/{{AGENT_A_WORKTREE}}` | Agent A |

Both worktrees see all branches and refs because `.git` is shared. They do NOT see each other's uncommitted working-tree files. This is the central risk this protocol exists to control.

## 3. Consensus Layer

Consensus-layer files are project truth. Only commits to these files count as delivery. Working-tree edits do not count.

Define your project's consensus-layer file set. Typical entries:

| Path pattern | Owner of truth |
| --- | --- |
| `docs/design/*` | Agent A (architecture), with Agent B review |
| `docs/research/*` | Agent A (research), with user review |
| current handoff checkpoint | both, append-only checkpoints |
| audit / finding ledger | both, finding lifecycle |
| this protocol file | both agents read, user adjudicates |
| `{{AGENT_A_INSTRUCTION_FILE}}` | Agent A, with user approval |
| `{{AGENT_B_INSTRUCTION_FILE}}` | Agent B, with user approval |

All other files (runtime code, manifests, tests, generated assets, project-specific work records, etc.) are outside this protocol and follow each agent's normal rules.

## 4. The Five Rules

### R1 — Consensus-layer writes commit immediately

When an agent finishes writing or editing a consensus-layer file, it must commit before declaring the work delivered. Uncommitted working-tree edits are drafts, not deliverables.

### R2 — Pickup must inspect the full branch graph

Before starting any task, each agent must run the full-branch inspection set, not single-branch log:

```bash
git worktree list
git branch --all --verbose --no-abbrev
git log --all --decorate --oneline --graph -10
git status --short
```

Reason: the two worktrees share `.git`. The other agent's commits on its own branch are visible as refs, but they do NOT appear in the current branch's single-branch `git log`. Without `--all`, the picking-up agent will miss them.

### R3 — Untracked files are not deliverables

If a consensus-layer file is untracked or modified but uncommitted, it is treated as NOT delivered, regardless of working-tree presence. Other agents must not rely on it. The owning agent must either commit it or explicitly flag it as a draft in the handoff.

This rule prevents two agents from believing different things are "the current truth."

### R4 — Mainline integration is explicit, not implicit

Seeing another agent's commit on its branch is not the same as integrating it. To bring another agent's consensus-layer change into the working branch, the integrating agent must perform one of:

| Action | When to use |
| --- | --- |
| `git merge <branch>` | normal integration of an agent branch into mainline |
| `git cherry-pick <commit>` | selective uptake of a subset of commits |
| Pull request review | when user wants explicit approval gate before integration |

"I saw it" is never integration.

### R5 — Consensus-layer conflicts are user-adjudicated

If two agents make incompatible consensus-layer edits, neither agent may silently overwrite the other. The agent who detects the conflict must:

1. Stop the edit
2. Summarize both sides in plain text
3. Ask the user to adjudicate

Only after user adjudication may an agent proceed.

## 5. Session-Start Checklist

Every agent, every session, before any planning or editing on a consensus-layer file:

1. Run the R2 full-branch inspection set.
2. Identify the other agent's most recent consensus-layer commit, if any.
3. Decide whether integration is needed for the current task. If yes, integrate via R4.
4. Re-read the latest committed handoff checkpoint.
5. Re-read any audit-ledger findings touching the task.
6. Output the per-agent preflight gate (see `preflight-gate.md` rule).

If step 2 surfaces an uncommitted but visible working-tree edit from the other agent (only visible inside the same worktree), treat it as R3: not a deliverable, do not rely on it.

## 6. Session-End Checklist

Every agent, every session, before declaring work done:

1. Identify which files touched fall inside the consensus layer (§3).
2. Commit those files. Group commits by intent. Do not bundle unrelated changes.
3. Update the handoff checkpoint if any of: repo state, task state, blocker, hot zone, continuation context changed.
4. Update the audit ledger if any finding appeared, changed, or was resolved.
5. In the final report, list the consensus-layer commit SHAs created this session.

If consensus-layer files were edited but not committed, the session is incomplete. The agent must either commit, or explicitly mark them as draft and explain why in the handoff.

## 7. Failure Modes And Recovery

| Failure | Symptom | Recovery |
| --- | --- | --- |
| Worktree drift | Two agents claim different "current truth" for the same consensus-layer file | R3 applies. Whichever side is uncommitted is not truth. Owning agent commits or withdraws. |
| Missed commit on pickup | Agent acts on stale handoff because it ran single-branch `git log` | R2 applies. Restart pickup with full-branch inspection. Re-run preflight gate. |
| Silent overwrite | Agent edited a consensus-layer file the other agent had also edited | R5 applies. Stop edit. Summarize both sides. Ask user. |
| Untracked drift | New consensus-layer file exists in working tree but is not tracked anywhere | R3 applies. Owning agent commits or explicitly marks it as draft in handoff. |
| Implicit integration | Agent says "I saw your update" but did not merge / cherry-pick | R4 applies. Integration must produce a commit on the working branch or explicit PR. |
| Cross-worktree write | Agent writes a consensus-layer file in the wrong worktree | Detect via R2 inspection of `git status --short` in both worktrees. Owning agent moves or commits in place. |

## 8. Non-Goals

This protocol does not:

- Replace per-agent execution rules. Those still apply inside each agent's own work.
- Cover non-consensus-layer files. Runtime code, tests, manifests, generated assets, project-specific records, ad-hoc scratch work are governed by each agent's normal rules.
- Define the merge policy for mainline branches. Branch strategy is user-owned.
- Make either agent the supervisor of the other. The user is the only adjudicator.

## 9. Version

| Field | Value |
| --- | --- |
| Source version | v1 (effective 2026-05-12, dome-TV project) |
| Portable version | v1.0.0 (extracted 2026-05-18) |
| Changes from source | Replaced project-specific paths and agent names with `{{PLACEHOLDER}}` variables; removed dome-TV-specific consensus-layer file enumeration; kept the protocol mechanics intact |
