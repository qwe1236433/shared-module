# Parallel Lane Workflow Module

Status: reusable docs-only workflow module.

Date: 2026-05-19

Packaged layout:

```text
workflows/parallel-lane-workflow/
  schemas/
  scripts/
  examples/
  docs/
```

Run the self-tests from this folder:

```powershell
python scripts/test_handoff_basket.py
python scripts/test_active_target_claim.py
python scripts/test_queue_board.py
```

## 1. Purpose

This module captures the reusable workflow behind the S03 parallel material /
D.3 / deep-relation work. It is meant to be copied or adapted for other complex
research, design, data, or implementation tracks where one big task is too
slow if every worker shares the same file and maturity level.

The pattern is:

```text
split one broad task into maturity lanes
  -> give each lane a coordinate and starter card
  -> let lanes run in parallel
  -> pass packets forward only through explicit gates
  -> loop each lane onto the next target
```

This module now includes docs-dev schemas and validators for the handoff-basket,
task-claim, and queue-board boundaries. It still does not create runtime
manifests, database tables, prompts, web UI routes, production queues, or
accepted evidence gates. Those can only be added later through the normal
architecture / manifest / Boundary Re-Entry process.

## 2. When To Use This Module

Use this module when a task has all of these properties:

- Multiple people or windows can work at the same time.
- Work has different maturity levels, such as raw material, verified evidence,
  draft contract, accepted contract, downstream relation, and implementation.
- A lower-maturity output must not be mistaken for a higher-maturity result.
- The same broad topic has many repeated targets, so each lane must loop from
  one target to the next.
- Coordination by chat memory alone is causing drift, duplication, or vague
  handoffs.

Do not use this module for small one-file fixes, single-command checks, or work
where one person must make a single indivisible decision.

## 3. Core Concepts

| Concept | Meaning |
| --- | --- |
| Work coordinate | Short address for a lane target, such as `S03-L2B-D3-FLEABAG`. It names where work belongs but is not a full instruction. |
| Starter card | The concrete task card a new window must follow after receiving a coordinate. |
| Lane | A repeatable work stream with its own allowed inputs, outputs, and forbidden promotions. |
| Maturity state | A named state that says how trustworthy or usable an artifact is. |
| Packet | A structured handoff artifact produced by a lane. |
| Handoff basket | The only container a downstream lane may consume. It contains the packet, gate result, forbidden use, and next allowed action. |
| Task claim file | The explicit ownership file a window takes before editing one target. It binds one basket, one lane, one target, one write scope, and one release condition. |
| Queue board | The file-based queue UI that lists available baskets, target status, active claims, and next eligible targets. |
| Promotion gate | The evidence or validation required before a packet can move to the next maturity state. |
| Loop contract | The rule that lets one lane finish one target and pick the next target without renegotiating the whole plan. |

## 4. Coordinate Grammar

A coordinate should be compact but not overloaded.

Recommended shape:

```text
<system>-<lane>-<maturity>-<target>
```

Examples:

```text
S03-L1-MATERIAL-SUPPLY
S03-L2A-D3-CASABLANCA
S03-L2B-D3-FLEABAG
S03-L3-DEEP-RELATION-PREP
```

Every coordinate should also have a human-readable window title:

```text
<lane plain name> / <target> / <current gate>
```

Example:

```text
Lane 2B D.3 Promotion / Fleabag S2E3 / legal timecode and source gate
```

Coordinate rule:

```text
The coordinate tells a worker where they are.
The starter card tells them what to do next.
```

If a window receives only a coordinate, it should open the matching starter
card. It should not spend the main answer explaining the coordinate unless the
user asked for explanation.

## 5. Lane Design Template

Define each lane with this table:

| Field | Required content |
| --- | --- |
| Lane ID | Stable identifier, for example `L1`, `L2A`, `L3`. |
| Plain name | Human-readable name. |
| Purpose | What this lane exists to advance. |
| Allowed inputs | Exact maturity states or files this lane may consume. |
| Allowed outputs | Exact packet types or maturity states this lane may produce. |
| Forbidden outputs | States this lane may not claim. |
| First targets | The current target queue. |
| Active target claim | The single target currently owned by the window. |
| Promotion gates | Evidence or checks required before output can move forward. |
| Handoff packet | Required fields in the lane's final note. |

Minimum lane table:

```text
Lane:
Purpose:
Allowed inputs:
Allowed outputs:
Forbidden outputs:
Current target:
Active target claim:
Required gates:
Next target queue:
```

## 6. Starter Card Template

Every reusable lane should provide a starter card so a new window can begin
without interpreting the whole system from scratch.

```text
Window title:
Coordinate:
Plain meaning:
Current input files:
Current target:
Active target claim:
This window must do:
Required output:
Forbidden claims:
Next target queue:
Stop condition:
```

Starter-card rules:

1. Use imperative tasks, not only labels.
2. State the next evidence gate, not the whole long-term dream.
3. Include explicit forbidden claims.
4. Include a next-target queue so the lane can loop.
5. Include a stop condition when evidence is missing or the target is blocked.
6. Include a human-readable window title so the lane is clear without decoding
   the coordinate.
7. Declare exactly one active target before doing work.

## 7. Maturity State Model

A good lane workflow has a shared maturity ladder. The exact labels change by
domain, but the ladder should preserve this shape:

```text
raw lead
  -> candidate packet
  -> authority / existence checked
  -> exact unit locked
  -> professional / validator support attached
  -> false-positive / negative case guarded
  -> draft record
  -> accepted record
  -> downstream relation / integration ready
```

State rules:

- A packet can move forward only when the required gate is present.
- A lower state must never be counted as a higher state.
- A state name must describe usable maturity, not emotional confidence.
- If a state is partial, name the missing gate directly.

## 8. Packet Template

Every lane output should be a packet, not loose notes.

Minimum packet:

```text
packet_id:
window_title:
coordinate:
lane:
target:
active_target_claim:
input_refs:
state_before:
work_performed:
state_after:
evidence_added:
blocked_promotions:
forbidden_use:
next_lane:
next_target:
checks_run:
```

The `forbidden_use` field is mandatory. It prevents downstream windows from
treating a partial result as accepted evidence, runtime behavior, or a schema
fixture.

## 9. Handoff Basket Contract

A packet is the work content. A basket is the transfer boundary.

The downstream lane may consume only a basket, not loose notes, chat
explanations, implied intent, or a worker's confidence. This is the rule that
keeps the workflow from depending on an AI being clever.

Minimum basket:

```text
schema_version:
basket_id:
from_lane:
to_lane:
source_packet:
accepted_input_state:
produced_output_state:
gate_result:
ready_for_downstream:
downstream_allowed_action:
downstream_forbidden_action:
blockers:
next_basket_owner:
precision_lock_required:
```

Basket rules:

1. A lane may only deposit one basket after writing its packet.
2. A downstream lane may only take a basket whose `to_lane` matches its lane.
3. If `ready_for_downstream` is false, the receiver must not upgrade, infer, or
   repair the basket silently. It may only mark blocked or return the basket.
4. `downstream_allowed_action` must be an action, not a vague instruction.
5. `downstream_forbidden_action` must name the exact promotions that remain
   illegal.
6. The receiver must not use background knowledge to fill missing basket
   fields.
7. If the basket is incomplete, the receiver stops at basket validation.

## 9.1 Task Claim Contract

The basket says what can be consumed. The task claim says who may consume it
and where they may write.

The task claim exists so a receiving window cannot begin by interpreting the
whole workflow from chat. It must claim one target from one validated basket,
then work inside a declared write scope.

Minimum claim:

```text
schema_version:
claim_id:
lane:
target:
  target_id:
  coordinate:
  plain_name:
source_basket:
  basket_id:
  path:
  expected_to_lane:
claim_status:
claimed_by:
claim_started_at:
review_after:
write_scope:
forbidden_write_scope:
allowed_actions:
forbidden_actions:
acceptance_standard_ref:
release_condition:
handoff_basket_on_release:
  expected_basket_id:
  expected_to_lane:
  required_before_release:
```

Claim rules:

1. A window may hold only one `active` claim for one target.
2. A target may have only one active claim at a time.
3. The claim must point to an existing source basket.
4. The source basket must validate for the claiming lane.
5. `write_scope` must name concrete files or narrow targets, not broad
   directories or wildcard paths.
6. `forbidden_write_scope` must name files or zones the window must not touch.
7. A claim cannot be released until it deposits, returns, or blocks with the
   expected basket condition.
8. The worker must not use chat context or memory to repair a missing claim
   field.

Folder layout:

```text
examples/task_claims/
```

In a consuming project, create separate live folders for active / released /
blocked claims. This package keeps only reusable examples and validators.

## 9.2 Queue Board Contract

The queue board says what can be picked next.

It is a file-based UI, not a runtime queue, database table, or web app. Its job
is to keep several windows from guessing which target is available.

Minimum board:

```text
schema_version:
board_id:
board_status:
board_owner:
updated_at:
lanes:
available_baskets:
targets:
active_claims:
board_rules:
```

Target states:

```text
unclaimed
active_claim
blocked
returned
released
```

Board rules:

1. A target can have at most one active claim.
2. A target cannot be both `unclaimed` and actively claimed.
3. A target lane must match the `to_lane` of its source basket.
4. Every available basket must validate before it can seed a target.
5. Every active claim must validate before the board can pass.
6. Blocked or returned targets must name blockers.
7. The board may compute `next_eligible_targets`, but it must not upgrade
   maturity or fill missing evidence.
8. Workers may claim only targets that are listed as next eligible by the board
   report.

Folder layout:

```text
examples/queue_boards/
```

In a consuming project, create separate live and archived board folders. This
package keeps only reusable examples and validators.

## 10. Fixed Worker Rules

Each lane worker must follow fixed behavior rules:

```text
read the queue board and assigned starter card
select only a next eligible target
claim one active target
take only allowed input baskets
validate the task claim
perform only listed gates
write one packet
deposit one handoff basket
mark blocked promotions
release or carry active target claim
```

The worker must not:

```text
reinterpret the upstream task
merge loose notes into evidence
promote confidence into maturity
change another lane's acceptance standard
repair missing fields by inference
consume a basket addressed to another lane
work outside the declared claim scope
claim a target not listed as eligible by the queue board
```

## 11. Fixed Acceptance Standard

Each basket has a fixed acceptance result:

```text
accepted
accepted_with_limits
blocked_missing_required_field
blocked_failed_gate
blocked_wrong_receiver
returned_to_previous_lane
```

Acceptance requires:

- required fields are present
- `from_lane` and `to_lane` are valid
- `produced_output_state` is allowed for the producer lane
- `accepted_input_state` is allowed for the receiver lane
- `gate_result` matches the required gate
- forbidden use is explicit
- blockers are listed when the basket is not fully ready

No receiver may invent missing fields. Missing required input is a blocker, not
an invitation to guess.

## 12. Loop Contract

Each lane should behave like a repeatable production line:

```text
claim one target
  -> run the lane gates
  -> write the output packet
  -> deposit the handoff basket
  -> mark state_after
  -> list blocked_promotions
  -> release or carry the active_target_claim
  -> choose next_target
  -> stop or continue
```

Loop stop conditions:

- The next target lacks an input packet.
- The next target needs a human / design decision.
- The next target would require crossing into another lane.
- The lane has become the bottleneck and more upstream volume would create
  clutter.
- A required source, file, schema, validator, or boundary check is missing.

## 13. Parallel Safety Rules

Use these rules when several windows work at once:

1. One lane owns one maturity level.
2. One window owns one target at a time.
3. One file section should not be edited by two windows at the same time.
4. If multiple windows need the same board, they should write separate packets
   and merge into the board later.
5. If a result is untracked or uncommitted in a consensus-layer path, treat it
   as a draft, not delivered truth.
6. If a lane cannot verify a gate, it must mark the target blocked instead of
   upgrading the state.
7. If a window loops to another target, it must declare the new active target
   before editing shared files.
8. A receiver may consume only an addressed handoff basket, never a loose packet
   or chat summary.

## 14. Extraction Criteria

A project-specific lane map is ready to become a reusable module only when it
has:

- At least three lanes with distinct maturity levels.
- Repeated targets in at least two lanes.
- Starter cards that let a new window start without interpretation.
- A shared maturity state ladder.
- Packet templates with mandatory forbidden-use fields.
- Handoff baskets with fixed receiver, allowed action, forbidden action, and
  acceptance result.
- A loop contract.
- Conflict rules for shared boards / files.
- A clear boundary between docs-only planning and runtime activation.

The S03 workflow reached this threshold after the material lane, D.3 promotion
lane, deep-relation preparation lane, coordinate grammar, starter cards, and
loop rules were defined.

## 15. Migration Template

To migrate this module to another project or system, create a project-specific
lane map with this structure:

```text
1. Purpose
2. Starting truth
3. Work coordinates are not task commands
4. Lane table
5. Maturity state flow
6. Loop rule
7. Packet shapes
8. Handoff basket shapes
9. Starter cards
10. Fixed worker rules
11. Fixed acceptance standards
12. Current assignments
13. File ownership and conflict rules
14. Cross-window handoff rule
15. Efficiency rule
16. Closure / next queue
```

Then replace the S03-specific labels with project-specific labels, while
preserving the maturity gates, handoff baskets, and forbidden-use boundaries.

## 16. Machine Check Layer

The first machine-checkable layer lives under:

```text
schemas/handoff_basket.schema.yaml
scripts/validate_handoff_basket.py
scripts/test_handoff_basket.py
schemas/active_target_claim.schema.yaml
scripts/validate_active_target_claim.py
scripts/test_active_target_claim.py
schemas/queue_board.schema.yaml
scripts/validate_queue_board.py
scripts/test_queue_board.py
```

This layer checks basket shape, receiver ownership, state transitions,
downstream allowed / forbidden actions, blocker consistency, precision trigger
naming, source-basket linkage, active target ownership, write-scope narrowness,
release conditions, queue target status, duplicate active claims, and next
eligible targets. It deliberately stops before runtime queue ownership, web UI,
database state, manifest wiring, or accepted evidence admission.

## 17. Promotion To Runtime

This module is documentation only. If a future team wants to turn it into a
runtime queue, validator, or UI board, that future work must add:

- schema for lane packets
- manifest entries for readers / writers
- tests for invalid promotion
- explicit default ownership
- Boundary Re-Entry check
- design decision if it changes architecture or data flow
- web/database queue UI or persistent claim storage if the module stops being
  docs-dev only

Until those exist, lane maps, baskets, claims, and queue boards remain docs-dev
workflow artifacts, not runtime state machines.

## 18. Minimal Copy Block

For fast reuse, copy this block first:

```text
Window title:
Coordinate:
Starter card:
Lane:
Allowed input:
Allowed output:
Forbidden output:
Current target:
Active target claim:
Required gate:
Output packet:
Handoff basket:
Downstream allowed action:
Downstream forbidden action:
Acceptance result:
Blocked promotion:
Next target:
```

This is the smallest useful unit of the module.
