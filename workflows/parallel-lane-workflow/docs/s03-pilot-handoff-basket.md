# Parallel Lane Handoff Basket - S03 Pilot Spec

Status: docs-only handoff-basket pilot; non-runtime.

Date: 2026-05-19

Parent module: `../README.md`

Machine-check layer:

```text
schemas/handoff_basket.schema.yaml
scripts/validate_handoff_basket.py
schemas/active_target_claim.schema.yaml
scripts/validate_active_target_claim.py
schemas/queue_board.schema.yaml
scripts/validate_queue_board.py
```

S03 background rule: source reference is the default gate. Version, edition,
platform, viewing-copy, timestamp, page, panel, frame, screenshot, or legal-copy
precision is required only when a named precision trigger exists.

## 1. Purpose

This file tests the handoff-basket layer against the current S03 three-lane
workflow. It makes each lane behave like a fixed station:

```text
previous station finishes a packet
  -> deposits a basket
  -> next station takes only that basket
  -> next station validates fixed fields
  -> next station does only the allowed action
```

No receiving lane may infer missing evidence from chat memory, general
knowledge, source familiarity, or confidence language.

Paired claim rule: before a receiver starts work, it must create or validate one
task-claim file. In this reusable package, example claims live under
`../examples/task_claims/`. In a consuming project, live claims should live in a
separate project-owned active / released / blocked folder. The claim must point
to this basket, name the exact target, declare write scope, and name the basket
expected on release.

Queue-board rule: when several windows are running, a receiver should pick only
targets listed in a validated queue board's `next_eligible_targets` report. The
queue board must point to a validated source basket and must not list the same
target as both unclaimed and actively claimed.

## 2. Fixed S03 Basket Chain

| Basket | From | To | Meaning | Receiver may do | Receiver must not do |
| --- | --- | --- | --- | --- | --- |
| `S03-BASKET-L1-TO-L2-CANDIDATE` | Lane 1 material supply | Lane 2 D.3 promotion | A raw / parked candidate is ready for source-reference and D.3 preflight. | Check authority signal, source role, unit boundary, A-axis fit, and false-positive risk. | Admit source index rows, PAR, case profile, D.3, D.4, solver, schema, manifest, database, UI, prompt, provider, or runtime use. |
| `S03-BASKET-L2-TO-L2-NEXT-GATE` | Lane 2 D.3 promotion | Lane 2 D.3 promotion | Same case needs the next D.3 gate before any downstream use. | Continue source-reference, unit-boundary, professional-source, evidence-split, or false-positive work. | Skip to accepted D.3, count D.4 evidence, or ask for precision lock unless a precision trigger is named. |
| `S03-BASKET-L2-TO-L3-REVIEW-ONLY` | Lane 2 D.3 promotion | Lane 3 deep relation prep | A case is mature enough to create relation questions, but not accepted as D.3 evidence. | Draft D.4 review questions or relation-taxonomy questions only. | Count coexistence, create graph edges, assign weights, choose algorithms, or create solver inputs. |
| `S03-BASKET-L2-TO-D3-REVIEW` | Lane 2 D.3 promotion | Human / design D.3 review | A case-profile draft is ready for review. | Review whether it can become accepted D.3. | Treat the draft as accepted without review. |
| `S03-BASKET-L3-TO-FUTURE-SOLVER` | Lane 3 deep relation prep | Future solver lane | Only accepted D.3 relation evidence may move here. | Future implementation may validate graph / solver input. | Use current unaccepted S03 candidates. |

## 3. Lane 1 Basket: Material Supply To D.3 Promotion

Required basket fields:

```text
schema_version:
basket_id: S03-BASKET-L1-TO-L2-CANDIDATE
from_lane: S03-L1-MATERIAL-SUPPLY
to_lane: S03-L2-D3-PROMOTION
source_packet:
accepted_input_state:
produced_output_state: candidate_packet | source_review_packet
gate_result:
ready_for_downstream:
downstream_allowed_action:
downstream_forbidden_action:
blockers:
next_basket_owner:
precision_lock_required:
```

Fixed Lane 1 acceptance standard:

```text
accepted: authority/source signal and candidate unit are explicit
accepted_with_limits: useful lead, but source role or unit boundary is weak
blocked_missing_required_field: missing title, source ref, authority signal, or target unit
returned_to_previous_lane: packet claims PAR, D.3, D.4, solver, or runtime use
```

Lane 2 may take the basket only when the basket names a candidate unit and does
not claim D.3 maturity.

## 4. Lane 2 Basket: D.3 Promotion Internal Gate

Required basket fields:

```text
schema_version:
basket_id: S03-BASKET-L2-TO-L2-NEXT-GATE
from_lane: S03-L2-D3-PROMOTION
to_lane: S03-L2-D3-PROMOTION
source_packet:
accepted_input_state: d3_row_candidate | authority_entry_checked | source_reference_marked | professional_source_clipped | false_positive_guarded
produced_output_state:
gate_result:
ready_for_downstream:
downstream_allowed_action:
downstream_forbidden_action:
blockers:
next_basket_owner:
precision_lock_required:
precision_trigger:
```

Fixed Lane 2 acceptance standard:

```text
accepted: source reference, unit boundary, source claim / analyst inference split, and false-positive guard are present
accepted_with_limits: source reference and unit boundary exist, but professional-source clips or leaf split remain partial
blocked_missing_required_field: missing source reference, unit boundary, source-role statement, or forbidden-use field
blocked_failed_gate: packet promotes to accepted D.3, D.4, solver, or runtime without review
returned_to_previous_lane: packet only adds raw material and does not run a D.3 gate
```

Precision lock is not a default blocker. The basket may require precision only
when it names a trigger such as quote publication, screenshot / frame claim,
legal-copy proof, page / panel fixture, training data, or user-requested exact
version comparison.

## 5. Lane 2 Basket: D.3 Review Candidate

Required basket fields:

```text
schema_version:
basket_id: S03-BASKET-L2-TO-D3-REVIEW
from_lane: S03-L2-D3-PROMOTION
to_lane: HUMAN-D3-REVIEW
source_packet:
accepted_input_state: case_profile_draft | D3_profile_draft
produced_output_state: D3_review_candidate
gate_result:
ready_for_downstream: true
downstream_allowed_action: review for accepted D.3 only
downstream_forbidden_action: D.4 evidence count, solver input, runtime admission
blockers:
next_basket_owner: human/design reviewer
precision_lock_required:
```

This basket is the first point where accepted D.3 can be discussed. It still
does not accept D.3 automatically.

## 6. Lane 3 Basket: Deep Relation Prep

Required basket fields:

```text
schema_version:
basket_id: S03-BASKET-L2-TO-L3-REVIEW-ONLY
from_lane: S03-L2-D3-PROMOTION
to_lane: S03-L3-DEEP-RELATION-PREP
source_packet:
accepted_input_state: D3_review_candidate | D3_accepted
produced_output_state: D4_question | D4_hypothesis | D4_relation_ready
gate_result:
ready_for_downstream:
downstream_allowed_action:
downstream_forbidden_action:
blockers:
next_basket_owner:
precision_lock_required:
```

Fixed Lane 3 acceptance standard:

```text
accepted: input is D3_accepted and supporting evidence refs are named
accepted_with_limits: input is only D3_review_candidate, so Lane 3 may draft questions only
blocked_failed_gate: input is unaccepted D.3 candidate but asks for D.4 evidence count
returned_to_previous_lane: missing D.3 status or supporting evidence refs
```

## 7. No-Inference Rule

If a basket lacks a required field, the receiver must record:

```text
acceptance_result: blocked_missing_required_field
receiver_action: stop_at_basket_validation
missing_fields:
return_to_lane:
```

The receiver must not fill missing fields from:

- chat context
- model memory
- general knowledge of the work
- confidence language
- another lane's draft
- source material not named by the basket

## 8. Minimal S03 Basket Example

```text
schema_version: parallel_lane_handoff_basket_v1
basket_id: S03-BASKET-L2-TO-L2-NEXT-GATE
from_lane: S03-L2B-D3-FLEABAG
to_lane: S03-L2-D3-PROMOTION
source_packet: S03_L2B_D3_CAND_006_Fleabag_source_check_20260519.md
accepted_input_state: d3_row_candidate
produced_output_state: source_reference_marked
gate_result: accepted_with_limits
ready_for_downstream: true
downstream_allowed_action: separate A04 / A06 / A07 / A08 evidence and write false-positive guard
downstream_forbidden_action: accepted D.3, D.4 evidence count, solver input, runtime use
blockers: professional-source clips and D.3 review still missing
next_basket_owner: S03-L2-D3-PROMOTION
precision_lock_required: false
```

The next worker may continue the named D.3 gate. It may not treat the packet as
accepted D.3 evidence.
