# Project Quality Governance Framework

Purpose: portable governance framework for AI-assisted software projects.

Use this file as the seed document for a new repository or an existing
repository that needs stronger agent discipline. It defines the quality system,
file boundaries, agent workflow, review gates, report format, synchronization
protocol, and adoption checklist needed to keep AI development coherent.

This is not a project blueprint. It is a reusable framework for building one.

Portability rule: every project-specific name, path, command, schema, system,
provider, runtime artifact, and workflow state must be supplied by the target
repository. Do not copy values from the source project into a new project.

## 0. Project Profile Variables

Before adopting this framework, define a target project profile. These values
are the only approved place to bind the framework to a specific repository.

| Variable | Meaning | Example value |
| --- | --- | --- |
| `{{PROJECT_NAME}}` | Human-readable project name. | `my-product` |
| `{{REPO_ROOT}}` | Repository root. Prefer relative paths in docs. | `.` |
| `{{PRIMARY_AGENT_FILE}}` | Main coding-agent instruction file. | `AGENTS.md` |
| `{{OPTIONAL_AGENT_FILES}}` | Other agent-specific instruction files. | `CLAUDE.md` |
| `{{MANIFEST_FILE}}` | Root manifest path if used. | `system_manifest.yaml` |
| `{{DESIGN_DIR}}` | Design-truth directory. | `docs/design` |
| `{{DEV_DIR}}` | Developer protocol and command directory. | `docs/dev` |
| `{{AUDIT_DIR}}` | Optional audit evidence directory. | `docs/audits` |
| `{{SOURCE_DIRS}}` | Source roots owned by the project. | `src`, `apps`, `packages` |
| `{{TEST_COMMANDS}}` | Real commands for this repository. | Defined in `TEST_COMMANDS.md` |
| `{{PACKAGE_MANAGER}}` | Package manager if applicable. | `npm`, `pnpm`, `uv`, `poetry` |
| `{{LANGUAGE_STACK}}` | Runtime languages and frameworks. | `TypeScript`, `Python` |
| `{{CI_SYSTEM}}` | CI owner if applicable. | `GitHub Actions` |

Adoption requirement:

- Replace placeholders with target-project values only after inspecting the new
  repository.
- Prefer relative paths unless an absolute path is required by a tool.
- Put machine-local paths, secrets, provider credentials, and generated output
  locations in local environment files or manifests, not in this framework.
- If the target project does not need a file in the expanded profile, omit it
  and state why in the adoption checkpoint.

## 1. What This Framework Solves

AI agents often fail in predictable ways:

- they optimize one file while breaking upstream or downstream contracts
- they confuse chat history with repository truth
- they keep old and new implementations active in parallel
- they silently fallback when required data is missing
- they change manifests without deciding whether architecture changed
- they skip tests but write confident summaries
- they hardcode paths, project names, provider names, or runtime assumptions
- they write broad prose instead of verifiable closure reports

This framework prevents those failures by separating:

| Concern | Owner |
| --- | --- |
| Project reality | blueprint/design docs |
| Agent execution rules | `{{PRIMARY_AGENT_FILE}}` and optional agent files |
| Shared checkpoint state | `{{DEV_DIR}}/AGENT_SYNC.md` |
| Current handoff | `{{DESIGN_DIR}}/06_HANDOFF.md` |
| Audit/finding state | `{{DESIGN_DIR}}/07_AUDIT_STATUS.md` |
| Final report format | `{{DESIGN_DIR}}/09_REPORT_TEMPLATES.md` |
| Test command details | `{{DEV_DIR}}/TEST_COMMANDS.md` |
| Runtime paths and dependencies | manifests |
| Machine-local values | environment files, ignored local config, or secret manager |

## 2. Adoption Profiles

Use the smallest profile that fits the target repository. Do not create files
only because this framework lists them.

### Minimal Profile

Use for small projects with one application or a small number of modules.

```text
root/
├─ {{PRIMARY_AGENT_FILE}}
├─ {{MANIFEST_FILE}}                  # optional if the project has no manifest model yet
├─ PROJECT_QUALITY_FRAMEWORK.md
└─ docs/
   ├─ design/
   │  ├─ 00_BLUEPRINT.md
   │  ├─ 06_HANDOFF.md                # optional if no continuation/handoff is expected
   │  ├─ 07_AUDIT_STATUS.md            # optional if no durable finding ledger is needed
   │  └─ 09_REPORT_TEMPLATES.md        # optional if report format lives in agent file
   └─ dev/
      ├─ AGENT_SYNC.md                 # optional if single-agent only
      └─ TEST_COMMANDS.md
```

### Expanded Profile

Use for multi-system projects, long-running agent work, complex contracts,
cross-module data flow, audit closure, or repeated handoffs.

```text
root/
├─ {{PRIMARY_AGENT_FILE}}
├─ {{OPTIONAL_AGENT_FILES}}
├─ {{MANIFEST_FILE}}
├─ PROJECT_QUALITY_FRAMEWORK.md
└─ docs/
   ├─ design/
   │  ├─ 00_BLUEPRINT.md
   │  ├─ 01_ARCHITECTURE.md
   │  ├─ 02_MODULE_CONTRACTS.md
   │  ├─ 03_DATA_FLOW.md
   │  ├─ 04_DECISIONS.md
   │  ├─ 05_ROADMAP.md
   │  ├─ 06_HANDOFF.md
   │  ├─ 07_AUDIT_STATUS.md
   │  ├─ 08_AGENT_BEHAVIOR.md
   │  └─ 09_REPORT_TEMPLATES.md
   └─ dev/
      ├─ AGENT_SYNC.md
      └─ TEST_COMMANDS.md
```

### No-Manifest Profile

Use only when the target repository is small and has not adopted manifests.
The agent instructions must then explicitly name:

- source roots
- public entrypoints
- owned outputs
- required tests
- generated artifact directories
- config owners

Upgrade to a manifest when entrypoints, outputs, dependencies, or validation
commands stop fitting in one short instruction section.

## 3. File Responsibility Boundaries

| File | Owns | Must Not Own |
| --- | --- | --- |
| `00_BLUEPRINT.md` | Global invariants, system boundaries, data ownership, quality priorities. | Agent workflow, command tables, report templates, issue dumps. |
| `01_ARCHITECTURE.md` | System topology, layers, runtime structure, responsibility map. | Field-level schemas, current task notes. |
| `02_MODULE_CONTRACTS.md` | Inputs, outputs, schemas, validators, defaults, failure modes. | Implementation bodies. |
| `03_DATA_FLOW.md` | Artifact movement, ownership boundaries, lifecycle transitions. | Design rationale, backlog. |
| `04_DECISIONS.md` | Architecture-significant decisions and tradeoffs. | Every small implementation detail. |
| `05_ROADMAP.md` | Planned work, sequencing, blocked design tasks. | Current checkpoint, audit ledger. |
| `06_HANDOFF.md` | Current checkpoint only. | Historical log, audit ledger, global blueprint. |
| `07_AUDIT_STATUS.md` | Confirmed findings, residual risks, validation gaps. | Current task handoff or agent workflow. |
| `08_AGENT_BEHAVIOR.md` | Cross-agent behavior routing when needed. | A second agent rulebook. |
| `09_REPORT_TEMPLATES.md` | Final report, handoff, audit, decision, roadmap formats. | Project architecture facts. |
| `{{PRIMARY_AGENT_FILE}}` | Coding-agent execution rules. | Shared checkpoint state or global design facts. |
| Optional agent files | Agent-specific execution rules for other tools. | Other agents' workflows unless intentionally shared. |
| `AGENT_SYNC.md` | Shared checkpoint protocol and status vocabulary. | Project architecture or task execution loop. |
| `TEST_COMMANDS.md` | Concrete test, validator, audit command table. | Global design facts. |
| `{{MANIFEST_FILE}}` | Entrypoints, dependencies, runtime paths, outputs, tests. | Design rationale or prose reports. |

If files disagree, fix the stale file instead of inventing a local exception.

## 4. Execution Read Order

Every coding or review task must start by establishing global context.

Required order:

1. Read the agent-specific execution file, such as `{{PRIMARY_AGENT_FILE}}`.
2. Read `{{DEV_DIR}}/AGENT_SYNC.md` if this is multi-agent or continuation work.
3. Read the latest checkpoint in `{{DESIGN_DIR}}/06_HANDOFF.md` if present.
4. Read `{{DESIGN_DIR}}/00_BLUEPRINT.md`.
5. Read task-impact design docs:
   - architecture: `01_ARCHITECTURE.md`
   - contracts: `02_MODULE_CONTRACTS.md`
   - data flow: `03_DATA_FLOW.md`
   - decisions: `04_DECISIONS.md`
   - roadmap: `05_ROADMAP.md`
   - audit status: `07_AUDIT_STATUS.md`
6. Read manifests if entrypoints, dependencies, runtime paths, outputs, tests,
   or source-of-truth ownership may change.
7. Read the smallest relevant source files.

The blueprint is pre-execution context, not an after-the-fact documentation
cleanup step.

## 5. Requirement Clarification Gate

Classify unclear requirements by risk.

High-risk domains:

| Domain | Examples |
| --- | --- |
| architecture | layers, system boundaries, long-term structure |
| module boundary | ownership, allowed dependencies, public interfaces |
| API or contract | request/response shape, schema, required fields |
| data flow | producer, consumer, transformation, lifecycle |
| manifest | `reads_from`, `writes_to`, entrypoint, runtime path |
| defaults | source of truth, fallback ownership |
| destructive operations | delete, move, overwrite, regenerate, mass rewrite |
| generated assets | output paths, naming, provenance, overwrite rules |
| user-authored content | original text, approved assets, manual decisions |
| validation gates | pass/fail behavior, test expectations |
| acceptance criteria | what counts as done |
| roadmap priority | sequencing, deferred work, blockers |
| irreversible changes | expensive-to-reverse migrations or rewrites |

Rules:

| Situation | Required behavior |
| --- | --- |
| High-risk domain and user intent/scope/risk acceptance is unclear | Stop and ask before editing. |
| Goal is clear, change is local/reversible, source of truth is not changed | Make the smallest safe implementation and state assumptions. |
| Requirement is blocked by missing architecture or contract decision | Ask using the requirement blocker format. |
| User asks for broad deletion, overwrite, migration, generated asset rewrite, or irreversible work | Ask for explicit approval unless already clearly granted. |

Never use TODOs, stubs, silent fallbacks, degraded behavior, or declarations to
pretend a task is complete.

## 6. Requirement Blocker Format

Use this format when blocked:

```md
## Requirement Blocker

I cannot safely complete this task because one or more required decisions are unclear.

### Blocking Question

...

### Why This Blocks Implementation

...

### Affected Files / Modules

- `...`

### Safe Options

Option A: ...
Impact: ...

Option B: ...
Impact: ...

### My Recommendation

...

Please choose one option before I continue.
```

## 7. Blueprint Impact Check

Every code change and every confirmed review finding must pass this check.

| Step | Required action |
| --- | --- |
| 1 | Classify the change or finding. |
| 2 | Decide whether it changes a design fact. |
| 3 | If design fact changed, update the matching design document. |
| 4 | If no design fact changed, explain why in the final report. |

Allowed classifications:

- design fact changed
- implementation-only defect
- test/audit gap
- stale documentation
- false positive

Design impact without a matching doc update means the task is incomplete.

## 8. Boundary Re-Entry Check

Boundary Re-Entry Check is required when a change or confirmed finding affects:

| Trigger | Examples |
| --- | --- |
| module input contract | accepted fields, required fields, validators |
| module output contract | produced packet shape, public return payload |
| manifest dependency | `reads_from`, `writes_to`, `produces_for`, entrypoints |
| cross-directory dependency | imports, path references, shared utility ownership |
| public API / schema / config | CLI flags, YAML schema, package exports, defaults |
| data ownership boundary | source-of-truth owner, writer system, approval owner |
| generated asset path or naming contract | output directories, filenames, handoff names |

Required steps:

1. Name the target system and touched boundary.
2. Check upstream input contract and manifest link.
3. Check downstream output contract and manifest link.
4. Compare route with data-flow docs and current manifests.
5. Run at least one boundary smoke or paired validator when available.
6. If no boundary check exists or cannot run, report the exact gap and risk.

If marking this check `not_applicable`, provide evidence:

```text
No runtime boundary, API contract, data flow, manifest dependency,
cross-directory dependency, generated asset path, or naming contract changed.
```

## 9. Manifest Change Classification

Any root or system manifest change must be classified.

| Class | Meaning | Required action |
| --- | --- | --- |
| runtime correction | Corrects stale, false, duplicate, or invalid manifest statements without changing actual architecture or data flow. | Check affected paths exist and explain why design docs do not need updates. |
| architecture/data-flow change | Changes dependency direction, `reads_from`, `writes_to`, module responsibility, contract boundary, or runtime integration behavior. | Check/update relevant design docs and run Boundary Re-Entry Check. |
| ambiguous | It is unclear whether this is metadata correction or real behavior change. | Stop and request human/design review. |

Report manifest classification in the final response whenever a manifest changed.

## 10. Hardcoding Control

Reusable framework material must not contain source-project constants.

Forbidden in reusable docs and templates:

- absolute Windows or Unix machine paths
- source-project names, story names, client names, workspace names, or product
  names unless they are clearly marked as replaceable examples
- provider names, model names, account names, bucket names, service URLs, API
  base URLs, or environment variable names that do not belong to the target
  project
- generated output directories copied from another project
- package-manager commands before the target repository has been inspected
- test commands that have not been verified in the target repository
- schema names, config keys, or manifest fields copied without matching
  target-project validation

Approved patterns:

- use placeholders from the Project Profile Variables table
- use relative paths for repository files
- put machine-local values in ignored local config or environment files
- put provider-specific details in target-project manifests or operations docs
- mark examples as examples and keep them separate from required commands
- require a path/reference scan before declaring the adopted framework portable

Portability scan patterns:

```text
<windows-drive-path-pattern>
<unix-home-path-pattern>
<local-dev-host-pattern>
<source-project-name>
<source-client-name>
<source-workspace-name>
<source-provider-name>
<source-model-name>
<source-output-directory>
```

Replace the placeholders above with known source-project values before using
the scan on a real migration. Keep the scan terms outside the reusable template
when the target repository enforces zero source-project string matches.

## 11. Non-Negotiable Engineering Rules

- Every schema must have paired validation.
- Missing required input must raise an explicit error.
- File/config/path absence must not return `{}`, `[]`, or `""` as fallback.
- Old and new implementations must not remain active in parallel.
- Do not create private duplicate utilities when a shared helper exists.
- Defaults must have one source of truth.
- LLM output must be schema-validated before use.
- Required tests or validators must not be skipped without exact reason.
- Fallback is allowed only when declared by design/contract or explicitly
  approved for the task.
- Chat is not project truth.
- Final report is not a substitute for repository persistence.
- Reusable templates must be free of source-project hardcoding.

## 12. Minimum Check Matrix

| Change type | Required checks |
| --- | --- |
| Docs-only | Diff whitespace check; link/path/reference scan if references changed. |
| Framework/template migration | Portability scan; placeholder replacement check; target path existence check for adopted files. |
| Manifest | Manifest schema/validator if available; paired module/path existence check; Boundary Re-Entry smoke if behavior is affected. |
| Python module | Relevant unit tests; affected pipeline test when declared; schema/validator tests for data modules. |
| TypeScript/package | Typecheck; lint. |
| Generated asset pipeline | Dry-run if available; output path check; no overwrite without explicit permission. |
| Design doc change | Blueprint index/read-order check if file list changed; cross-reference scan for renamed concepts. |
| Public API/schema/config | Contract/schema validator; compatibility check; documentation update if public. |
| Cross-system change | Boundary smoke or paired producer/consumer validator. |

The target repository's concrete command names belong in
`{{DEV_DIR}}/TEST_COMMANDS.md`.

## 13. Final Report Format

Every final response should use this order:

1. Summary
2. Files changed
3. Behavior changed
4. Blueprint impact
5. Boundary result
6. Checks run
7. Skipped / failed checks
8. Repository sync
9. Self-audit table
10. Remaining risks
11. Closure verdict

Self-audit table:

| Gate | Status | Evidence / reason |
| --- | --- | --- |
| Requirement / approval gate | executed / partial / skipped / not_applicable | ... |
| Required reading | executed / partial / skipped / not_applicable | ... |
| Blueprint Impact Check | executed / partial / skipped / not_applicable | ... |
| Manifest Change Classification | executed / partial / skipped / not_applicable | ... |
| Boundary Re-Entry Check | executed / partial / skipped / not_applicable | ... |
| Tests / checks | executed / partial / skipped / not_applicable | ... |
| Repository sync | executed / partial / skipped / not_applicable | ... |
| Scope control | executed / partial / skipped / not_applicable | ... |

Every `partial` or `skipped` row needs a concrete reason. Every
`not_applicable` row needs trigger evidence.

## 14. Checkpoint Protocol

The current checkpoint should be kept in one file, usually
`{{DESIGN_DIR}}/06_HANDOFF.md`.

Checkpoint fields:

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

Task status vocabulary:

- `proposed`
- `working`
- `input_required`
- `completed`
- `failed`
- `deferred`
- `superseded`

Finding state vocabulary:

- `new`
- `confirmed`
- `fixed`
- `deferred`
- `false_positive`
- `needs_design_decision`
- `needs_boundary_check`

Do not use `done`, `fixed`, or `green` as task status without evidence.

## 15. Starter `00_BLUEPRINT.md` Skeleton

Use this when initializing a new project:

```md
# 00_BLUEPRINT.md

Purpose: define the shared reality model for `{{PROJECT_NAME}}`.

## 1. Source Of Truth

| Truth | Source |
| --- | --- |
| Agent execution rules | `{{PRIMARY_AGENT_FILE}}` and optional agent files |
| Global design facts | `{{DESIGN_DIR}}/` |
| Runtime entrypoints/dependencies/tests | manifests |
| Current audit status | `{{DESIGN_DIR}}/07_AUDIT_STATUS.md` |
| Test commands | `{{DEV_DIR}}/TEST_COMMANDS.md` |

## 2. System Mission

...

## 3. Non-Goals

...

## 4. Core Design Read Order

...

## 5. System Landscape

| System | Responsibility | Owns | Consumes | Produces |
| --- | --- | --- | --- | --- |

## 6. Global Architecture Layers

...

## 7. Canonical Concepts

...

## 8. Data Ownership

| Data Type | Source Of Truth | Owner | May Read | May Write |
| --- | --- | --- | --- | --- |

## 9. Global Data Classes

...

## 10. Contract And Validation Principles

...

## 11. Cross-System Flow Principles

...

## 12. State And Lifecycle Invariants

...

## 13. Quality Priorities

...

## 14. Non-Negotiable Global Rules

...

## 15. File Responsibility Boundaries

...
```

## 16. Starter `{{PRIMARY_AGENT_FILE}}` Pattern

Use this compressed pattern for smaller projects:

```md
# {{PRIMARY_AGENT_FILE}}

Read `{{DESIGN_DIR}}/00_BLUEPRINT.md` before code or review work.

Before editing:

1. Classify requirement risk.
2. Read current checkpoint if present.
3. Read relevant source, manifest, tests, and design docs.
4. Run Blueprint Impact Check.
5. Run Boundary Re-Entry Check if contracts, manifests, dependencies, public
   APIs, source-of-truth boundaries, or generated paths are affected.
6. Classify manifest changes when manifests change.
7. Make the smallest safe change.
8. Run checks from `{{DEV_DIR}}/TEST_COMMANDS.md`.
9. Update handoff/audit/design docs when state changed.
10. Final report must use fixed format and self-audit table.

Never claim unrun tests passed, invent files/APIs/commands, silently fallback on
required data, keep old and new active routes, hardcode source-project values,
or use TODO/stub/degraded work to claim completion.
```

## 17. Adoption Checklist

Use this checklist when applying the framework to a new repository:

| Step | Done |
| --- | --- |
| Define the Project Profile Variables for the target repository. | [ ] |
| Run the hardcoding scan against the source framework before copying. | [ ] |
| Create or update `{{PRIMARY_AGENT_FILE}}`. | [ ] |
| Create `{{DESIGN_DIR}}/00_BLUEPRINT.md`. | [ ] |
| Decide whether the project needs expanded docs `01` through `05`. | [ ] |
| Create `{{DEV_DIR}}/AGENT_SYNC.md` if multi-agent handoff is expected. | [ ] |
| Create `{{DESIGN_DIR}}/06_HANDOFF.md` if work will continue across sessions. | [ ] |
| Create `{{DESIGN_DIR}}/07_AUDIT_STATUS.md` if findings need durable tracking. | [ ] |
| Create `{{DESIGN_DIR}}/09_REPORT_TEMPLATES.md` or embed the report format in the agent file. | [ ] |
| Create `{{DEV_DIR}}/TEST_COMMANDS.md` with real commands from the target repo. | [ ] |
| Create or update manifests for entrypoints, dependencies, outputs, and tests. | [ ] |
| Add the Minimum Check Matrix to agent instructions. | [ ] |
| Require Blueprint Impact Check before completion. | [ ] |
| Require Boundary Re-Entry Check for contract/manifest/cross-system changes. | [ ] |
| Require manifest classification for manifest edits. | [ ] |
| Require fixed final report format and self-audit table. | [ ] |
| Verify no copied source-project path, provider, workspace, or story value remains. | [ ] |

## 18. Migration Workflow For A New Project

1. Inspect the target repository before creating files.
2. Fill the Project Profile Variables table for the target repository.
3. Choose Minimal, Expanded, or No-Manifest profile.
4. Create only the files required by that profile.
5. Replace all placeholders with target-project values or keep them as explicit
   template placeholders in template files.
6. Populate `TEST_COMMANDS.md` from real target-project commands only.
7. Populate manifests only with paths and entrypoints that exist.
8. Run a portability scan for source-project names, local paths, providers, and
   copied output directories.
9. Run the target project's available docs/checks/tests.
10. Write a checkpoint that records files created, checks run, skipped checks,
    and remaining adoption gaps.

Do not mark adoption complete until the target project can explain:

- where project truth lives
- where agent rules live
- what files are optional and why
- what commands are real and verified
- which boundaries require re-entry checks
- which manifests or source files own runtime entrypoints

## 19. Common Anti-Patterns

| Anti-pattern | Replacement |
| --- | --- |
| "Run tests" without command names | Maintain `TEST_COMMANDS.md` with exact commands. |
| All design facts in the agent rulebook | Put project facts in `{{DESIGN_DIR}}/`; keep agent files procedural. |
| Blueprint as issue dump | Put findings in `07_AUDIT_STATUS.md`. |
| Handoff as history log | Keep only current checkpoint in `06_HANDOFF.md`. |
| Manifest edit without classification | Classify as runtime correction, architecture/data-flow change, or ambiguous. |
| `not_applicable` without evidence | List the triggers that were not touched. |
| Silent fallback | Fail explicitly or use declared/approved fallback. |
| Old and new routes both active | Choose one active route and remove/deprecate the other. |
| Free-form final summary | Use fixed final report order and self-audit table. |
| Copying source-project paths into a new repo | Use Project Profile Variables and relative target paths. |
| Copying source-project commands into `TEST_COMMANDS.md` | Verify commands in the target repo first. |
| Treating optional docs as mandatory | Choose the smallest adoption profile that fits current complexity. |
