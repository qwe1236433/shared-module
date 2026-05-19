#!/usr/bin/env python3
"""Validate a parallel-lane queue board."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

MODULE_ROOT = Path(__file__).resolve().parents[1]

from file_utils import load_yaml, write_yaml  # type: ignore  # noqa: E402
from validate_active_target_claim import validate_claim  # noqa: E402
from validate_handoff_basket import (  # noqa: E402
    SCHEMA_PATH as HANDOFF_BASKET_SCHEMA_PATH,
    validate_basket,
)


SCHEMA_PATH = (
    MODULE_ROOT
    / "schemas"
    / "queue_board.schema.yaml"
)


def _is_blank(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _is_missing_required_field(field: str, value: Any) -> bool:
    if field in {"active_claims", "blockers"} and isinstance(value, list):
        return False
    return _is_blank(value)


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _add_error(errors: list[dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append({"code": code, "path": path, "message": message})


def _repo_path(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path
    return MODULE_ROOT / path


def _parse_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _check_required_root(
    board: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    for field in _as_list(schema.get("required_root_fields")):
        if field not in board or _is_missing_required_field(str(field), board.get(field)):
            _add_error(errors, "missing_required_field", field, f"{field} is required")
    gates["root_required"] = "pass" if len(errors) == before else "fail"


def _check_types(board: dict[str, Any], errors: list[dict[str, str]]) -> None:
    string_fields = ["schema_version", "board_id", "board_status", "board_owner", "updated_at"]
    for field in string_fields:
        if field in board and not isinstance(board.get(field), str):
            _add_error(errors, "invalid_type", field, f"{field} must be a string")

    for field in ("lanes", "available_baskets", "targets", "active_claims"):
        if field in board and not isinstance(board.get(field), list):
            _add_error(errors, "invalid_type", field, f"{field} must be a list")

    if "board_rules" in board and not isinstance(board.get("board_rules"), dict):
        _add_error(errors, "invalid_type", "board_rules", "board_rules must be a mapping")


def _check_board_status(
    board: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    if board.get("board_status") not in _as_list(schema.get("allowed_board_statuses")):
        _add_error(
            errors,
            "invalid_board_status",
            "board_status",
            f"board_status must be one of {_as_list(schema.get('allowed_board_statuses'))}",
        )
    if "updated_at" in board and not _parse_datetime(board.get("updated_at")):
        _add_error(errors, "invalid_datetime", "updated_at", "updated_at must be ISO-8601 datetime text")
    gates["board_status_valid"] = "pass" if len(errors) == before else "fail"


def _check_board_rules(
    board: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> dict[str, Any]:
    before = len(errors)
    rules = _as_mapping(board.get("board_rules"))
    for field in _as_list(schema.get("required_board_rule_fields")):
        if field not in rules or _is_blank(rules.get(field)):
            _add_error(
                errors,
                "missing_required_field",
                f"board_rules.{field}",
                f"board_rules.{field} is required",
            )

    max_claims = rules.get("max_active_claims_per_target")
    if "max_active_claims_per_target" in rules and not isinstance(max_claims, int):
        _add_error(
            errors,
            "invalid_type",
            "board_rules.max_active_claims_per_target",
            "max_active_claims_per_target must be an integer",
        )
    if isinstance(max_claims, int) and max_claims != 1:
        _add_error(
            errors,
            "invalid_board_rule",
            "board_rules.max_active_claims_per_target",
            "parallel-lane boards require exactly one active claim per target",
        )

    for field in ("receivers_must_match_source_basket", "loose_notes_allowed"):
        if field in rules and not isinstance(rules.get(field), bool):
            _add_error(errors, "invalid_type", f"board_rules.{field}", f"{field} must be a boolean")

    if rules.get("receivers_must_match_source_basket") is not True:
        _add_error(
            errors,
            "invalid_board_rule",
            "board_rules.receivers_must_match_source_basket",
            "receivers_must_match_source_basket must be true",
        )
    if rules.get("loose_notes_allowed") is not False:
        _add_error(
            errors,
            "invalid_board_rule",
            "board_rules.loose_notes_allowed",
            "loose_notes_allowed must be false",
        )

    gates["board_rules_explicit"] = "pass" if len(errors) == before else "fail"
    return rules


def _check_required_fields(
    item: Any,
    required_fields: list[Any],
    errors: list[dict[str, str]],
    path_prefix: str,
) -> dict[str, Any]:
    if not isinstance(item, dict):
        _add_error(errors, "invalid_type", path_prefix, f"{path_prefix} must be a mapping")
        return {}
    for field in required_fields:
        if field not in item or _is_missing_required_field(str(field), item.get(field)):
            _add_error(
                errors,
                "missing_required_field",
                f"{path_prefix}.{field}",
                f"{path_prefix}.{field} is required",
            )
    return item


def _index_lanes(
    board: dict[str, Any],
    schema: dict[str, Any],
    handoff_schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> dict[str, dict[str, Any]]:
    before = len(errors)
    lanes: dict[str, dict[str, Any]] = {}
    allowed_lanes = set(_as_list(handoff_schema.get("allowed_lanes")))
    for index, raw_lane in enumerate(_as_list(board.get("lanes"))):
        lane = _check_required_fields(
            raw_lane,
            _as_list(schema.get("required_lane_fields")),
            errors,
            f"lanes[{index}]",
        )
        lane_id = lane.get("lane")
        if not isinstance(lane_id, str):
            continue
        if lane_id in lanes:
            _add_error(errors, "duplicate_lane", f"lanes[{index}].lane", f"duplicate lane {lane_id!r}")
        if lane_id not in allowed_lanes:
            _add_error(errors, "unknown_lane", f"lanes[{index}].lane", f"unknown lane {lane_id!r}")
        max_active_claims = lane.get("max_active_claims")
        if not isinstance(max_active_claims, int):
            _add_error(
                errors,
                "invalid_type",
                f"lanes[{index}].max_active_claims",
                "max_active_claims must be an integer",
            )
        lanes[lane_id] = lane
    gates["lanes_allowed"] = "pass" if len(errors) == before else "fail"
    return lanes


def _index_available_baskets(
    board: dict[str, Any],
    schema: dict[str, Any],
    handoff_schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> dict[str, dict[str, Any]]:
    before = len(errors)
    baskets: dict[str, dict[str, Any]] = {}
    allowed_states = set(_as_list(schema.get("allowed_basket_states")))
    allowed_lanes = set(_as_list(handoff_schema.get("allowed_lanes")))

    for index, raw_basket in enumerate(_as_list(board.get("available_baskets"))):
        path_prefix = f"available_baskets[{index}]"
        basket = _check_required_fields(
            raw_basket,
            _as_list(schema.get("required_available_basket_fields")),
            errors,
            path_prefix,
        )
        basket_ref = basket.get("basket_ref")
        if not isinstance(basket_ref, str):
            continue
        if basket_ref in baskets:
            _add_error(errors, "duplicate_basket_ref", f"{path_prefix}.basket_ref", f"duplicate basket_ref {basket_ref!r}")

        if basket.get("basket_state") not in allowed_states:
            _add_error(
                errors,
                "invalid_basket_state",
                f"{path_prefix}.basket_state",
                f"basket_state must be one of {sorted(allowed_states)}",
            )
        for lane_field in ("from_lane", "to_lane"):
            if basket.get(lane_field) not in allowed_lanes:
                _add_error(
                    errors,
                    "unknown_lane",
                    f"{path_prefix}.{lane_field}",
                    f"{lane_field} must be one of {sorted(allowed_lanes)}",
                )

        basket_path_value = basket.get("path")
        loaded_basket: dict[str, Any] | None = None
        if isinstance(basket_path_value, str) and basket_path_value.strip():
            basket_path = _repo_path(basket_path_value)
            if not basket_path.is_file():
                _add_error(errors, "basket_file_missing", f"{path_prefix}.path", f"basket file does not exist: {basket_path}")
            else:
                loaded = load_yaml(basket_path)
                if not isinstance(loaded, dict):
                    _add_error(errors, "basket_file_invalid_type", f"{path_prefix}.path", "basket file root must be a mapping")
                else:
                    loaded_basket = loaded

        if loaded_basket is not None:
            for field in ("basket_id", "from_lane", "to_lane"):
                if loaded_basket.get(field) != basket.get(field):
                    _add_error(
                        errors,
                        "basket_reference_mismatch",
                        f"{path_prefix}.{field}",
                        f"board {field} {basket.get(field)!r} does not match file value {loaded_basket.get(field)!r}",
                    )
            report = validate_basket(
                loaded_basket,
                handoff_schema,
                receiver_lane=str(loaded_basket.get("to_lane")),
            )
            if report["status"] != "passed":
                _add_error(
                    errors,
                    "basket_validation_failed",
                    f"{path_prefix}.path",
                    f"handoff basket validation failed with {report['error_count']} error(s)",
                )

        baskets[basket_ref] = basket

    gates["available_baskets_validate"] = "pass" if len(errors) == before else "fail"
    return baskets


def _index_targets(
    board: dict[str, Any],
    schema: dict[str, Any],
    handoff_schema: dict[str, Any],
    baskets: dict[str, dict[str, Any]],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> dict[str, dict[str, Any]]:
    before = len(errors)
    targets: dict[str, dict[str, Any]] = {}
    coordinates: dict[str, str] = {}
    allowed_statuses = set(_as_list(schema.get("allowed_queue_statuses")))
    allowed_lanes = set(_as_list(handoff_schema.get("allowed_lanes")))

    for index, raw_target in enumerate(_as_list(board.get("targets"))):
        path_prefix = f"targets[{index}]"
        target = _check_required_fields(
            raw_target,
            _as_list(schema.get("required_target_fields")),
            errors,
            path_prefix,
        )
        target_id = target.get("target_id")
        coordinate = target.get("coordinate")
        if not isinstance(target_id, str):
            continue
        if target_id in targets:
            _add_error(errors, "duplicate_target", f"{path_prefix}.target_id", f"duplicate target_id {target_id!r}")
        if isinstance(coordinate, str):
            if coordinate in coordinates:
                _add_error(
                    errors,
                    "duplicate_coordinate",
                    f"{path_prefix}.coordinate",
                    f"coordinate already used by {coordinates[coordinate]!r}",
                )
            coordinates[coordinate] = target_id

        lane = target.get("lane")
        if lane not in allowed_lanes:
            _add_error(errors, "unknown_lane", f"{path_prefix}.lane", f"unknown lane {lane!r}")

        status = target.get("queue_status")
        if status not in allowed_statuses:
            _add_error(
                errors,
                "invalid_queue_status",
                f"{path_prefix}.queue_status",
                f"queue_status must be one of {sorted(allowed_statuses)}",
            )

        source_ref = target.get("source_basket_ref")
        source_basket = baskets.get(source_ref)
        if not isinstance(source_ref, str) or source_basket is None:
            _add_error(
                errors,
                "source_basket_ref_missing",
                f"{path_prefix}.source_basket_ref",
                f"source_basket_ref {source_ref!r} is not listed in available_baskets",
            )
        elif source_basket.get("to_lane") != lane:
            _add_error(
                errors,
                "basket_target_lane_mismatch",
                f"{path_prefix}.lane",
                f"target lane {lane!r} must match source basket to_lane {source_basket.get('to_lane')!r}",
            )

        blockers = target.get("blockers")
        if not isinstance(blockers, list):
            _add_error(errors, "invalid_type", f"{path_prefix}.blockers", "blockers must be a list")
        elif status in {"blocked", "returned"} and not blockers:
            _add_error(errors, "missing_blockers", f"{path_prefix}.blockers", f"{status} targets require blockers")

        targets[target_id] = target

    gates["target_source_basket_exists"] = "pass" if len(errors) == before else "fail"
    return targets


def _normalize_repo_path(path_value: Any) -> str | None:
    if not isinstance(path_value, str) or not path_value.strip():
        return None
    return str(_repo_path(path_value).resolve())


def _index_active_claims(
    board: dict[str, Any],
    schema: dict[str, Any],
    targets: dict[str, dict[str, Any]],
    baskets: dict[str, dict[str, Any]],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> dict[str, list[dict[str, Any]]]:
    before = len(errors)
    claims_by_target: dict[str, list[dict[str, Any]]] = {}

    for index, raw_claim_ref in enumerate(_as_list(board.get("active_claims"))):
        path_prefix = f"active_claims[{index}]"
        claim_ref = _check_required_fields(
            raw_claim_ref,
            _as_list(schema.get("required_active_claim_fields")),
            errors,
            path_prefix,
        )
        target_id = claim_ref.get("target_id")
        lane = claim_ref.get("lane")
        claim_id = claim_ref.get("claim_id")
        if isinstance(target_id, str):
            claims_by_target.setdefault(target_id, []).append(claim_ref)

        target = targets.get(target_id)
        if target is None:
            _add_error(errors, "claim_target_missing", f"{path_prefix}.target_id", f"target {target_id!r} is not listed")
        elif target.get("lane") != lane:
            _add_error(
                errors,
                "claim_target_lane_mismatch",
                f"{path_prefix}.lane",
                f"claim lane {lane!r} does not match target lane {target.get('lane')!r}",
            )

        claim_path_value = claim_ref.get("path")
        loaded_claim: dict[str, Any] | None = None
        if isinstance(claim_path_value, str) and claim_path_value.strip():
            claim_path = _repo_path(claim_path_value)
            if not claim_path.is_file():
                _add_error(errors, "claim_file_missing", f"{path_prefix}.path", f"claim file does not exist: {claim_path}")
            else:
                loaded = load_yaml(claim_path)
                if not isinstance(loaded, dict):
                    _add_error(errors, "claim_file_invalid_type", f"{path_prefix}.path", "claim file root must be a mapping")
                else:
                    loaded_claim = loaded

        if loaded_claim is None:
            continue

        loaded_target = _as_mapping(loaded_claim.get("target"))
        for field, loaded_value in (
            ("claim_id", loaded_claim.get("claim_id")),
            ("lane", loaded_claim.get("lane")),
            ("target_id", loaded_target.get("target_id")),
        ):
            expected_value = target_id if field == "target_id" else claim_ref.get(field)
            if loaded_value != expected_value:
                _add_error(
                    errors,
                    "claim_reference_mismatch",
                    f"{path_prefix}.{field}",
                    f"board {field} {expected_value!r} does not match file value {loaded_value!r}",
                )

        report = validate_claim(loaded_claim, claim_path=_repo_path(str(claim_path_value)))
        if report["status"] != "passed":
            _add_error(
                errors,
                "active_claim_validation_failed",
                f"{path_prefix}.path",
                f"task claim validation failed with {report['error_count']} error(s)",
            )

        if loaded_claim.get("claim_status") != "active":
            _add_error(
                errors,
                "active_claim_not_active",
                f"{path_prefix}.path",
                "active_claims may only list claims whose claim_status is active",
            )

        if target is not None:
            source_ref = target.get("source_basket_ref")
            source_basket = baskets.get(source_ref)
            claim_source = _as_mapping(loaded_claim.get("source_basket"))
            if source_basket is not None:
                board_basket_path = _normalize_repo_path(source_basket.get("path"))
                claim_basket_path = _normalize_repo_path(claim_source.get("path"))
                if board_basket_path != claim_basket_path:
                    _add_error(
                        errors,
                        "claim_source_basket_mismatch",
                        f"{path_prefix}.path",
                        "claim source basket path must match the target source basket",
                    )
                if claim_source.get("expected_to_lane") != target.get("lane"):
                    _add_error(
                        errors,
                        "claim_source_receiver_mismatch",
                        f"{path_prefix}.path",
                        "claim source basket receiver must match the target lane",
                    )

        if isinstance(claim_id, str) and target is not None and target.get("active_claim_id") not in (None, claim_id):
            _add_error(
                errors,
                "target_active_claim_id_mismatch",
                f"{path_prefix}.claim_id",
                f"target active_claim_id is {target.get('active_claim_id')!r}",
            )

    gates["active_claims_validate"] = "pass" if len(errors) == before else "fail"
    return claims_by_target


def _check_claim_target_consistency(
    targets: dict[str, dict[str, Any]],
    claims_by_target: dict[str, list[dict[str, Any]]],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    duplicate_before = len(errors)
    for target_id, claims in claims_by_target.items():
        if len(claims) > 1:
            _add_error(
                errors,
                "duplicate_active_claim",
                "active_claims",
                f"target {target_id!r} has {len(claims)} active claims",
            )
    gates["one_active_claim_per_target"] = "pass" if len(errors) == duplicate_before else "fail"

    status_before = len(errors)
    for target_id, target in targets.items():
        status = target.get("queue_status")
        claims = claims_by_target.get(target_id, [])
        active_claim_id = target.get("active_claim_id")
        if status == "active_claim":
            if not claims:
                _add_error(
                    errors,
                    "target_missing_active_claim",
                    f"targets.{target_id}",
                    "target marked active_claim must have one active claim entry",
                )
            elif len(claims) == 1 and active_claim_id not in (None, claims[0].get("claim_id")):
                _add_error(
                    errors,
                    "target_active_claim_id_mismatch",
                    f"targets.{target_id}.active_claim_id",
                    f"active_claim_id must match {claims[0].get('claim_id')!r}",
                )
        elif status == "unclaimed":
            if claims:
                _add_error(
                    errors,
                    "target_unclaimed_has_active_claim",
                    f"targets.{target_id}.queue_status",
                    "target cannot be unclaimed while an active claim exists",
                )
            if not _is_blank(active_claim_id):
                _add_error(
                    errors,
                    "target_unclaimed_has_active_claim_id",
                    f"targets.{target_id}.active_claim_id",
                    "unclaimed target cannot set active_claim_id",
                )
        elif status in {"blocked", "returned", "released"} and claims:
            _add_error(
                errors,
                "closed_target_has_active_claim",
                f"targets.{target_id}.queue_status",
                f"{status} target cannot have active claims",
            )
    gates["target_claim_status_consistent"] = "pass" if len(errors) == status_before else "fail"


def _compute_next_eligible_targets(
    targets: dict[str, dict[str, Any]],
    baskets: dict[str, dict[str, Any]],
    claims_by_target: dict[str, list[dict[str, Any]]],
    gates: dict[str, str],
) -> list[dict[str, Any]]:
    eligible: list[dict[str, Any]] = []
    for target_id, target in targets.items():
        source_ref = target.get("source_basket_ref")
        source_basket = baskets.get(source_ref)
        if target.get("queue_status") != "unclaimed":
            continue
        if claims_by_target.get(target_id):
            continue
        if source_basket is None or source_basket.get("basket_state") != "available":
            continue
        if source_basket.get("to_lane") != target.get("lane"):
            continue
        if _as_list(target.get("blockers")):
            continue
        eligible.append(
            {
                "target_id": target_id,
                "coordinate": target.get("coordinate"),
                "lane": target.get("lane"),
                "priority": target.get("priority"),
                "source_basket_ref": source_ref,
                "next_allowed_action": target.get("next_allowed_action"),
            }
        )
    gates["next_eligible_targets_computed"] = "pass"
    return eligible


def _acceptance_result(errors: list[dict[str, str]]) -> str:
    codes = {error["code"] for error in errors}
    if "duplicate_active_claim" in codes:
        return "blocked_duplicate_active_claim"
    if "basket_target_lane_mismatch" in codes or "claim_source_receiver_mismatch" in codes:
        return "blocked_wrong_receiver"
    if "active_claim_validation_failed" in codes:
        return "blocked_claim_validation"
    if "missing_required_field" in codes:
        return "blocked_missing_required_field"
    if "target_unclaimed_has_active_claim" in codes or "target_missing_active_claim" in codes:
        return "blocked_queue_state_conflict"
    if errors:
        return "blocked_failed_gate"
    return "accepted"


def validate_queue_board(
    board: dict[str, Any],
    schema: dict[str, Any] | None = None,
    handoff_schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a validation report for a parallel-lane queue board."""
    schema = schema or load_yaml(SCHEMA_PATH)
    handoff_schema = handoff_schema or load_yaml(HANDOFF_BASKET_SCHEMA_PATH)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    gates = {gate: "not_run" for gate in _as_list(schema.get("validation_gates"))}

    if not isinstance(board, dict):
        _add_error(errors, "expected_mapping", "$", "Queue board root must be a mapping")
        board = {}

    if board.get("schema_version") != schema.get("schema_id"):
        _add_error(
            errors,
            "schema_version_mismatch",
            "schema_version",
            f"schema_version must equal {schema.get('schema_id')!r}",
        )

    _check_required_root(board, schema, errors, gates)
    _check_types(board, errors)
    _check_board_status(board, schema, errors, gates)
    _check_board_rules(board, schema, errors, gates)
    _index_lanes(board, schema, handoff_schema, errors, gates)
    baskets = _index_available_baskets(board, schema, handoff_schema, errors, gates)
    targets = _index_targets(board, schema, handoff_schema, baskets, errors, gates)
    claims_by_target = _index_active_claims(board, schema, targets, baskets, errors, gates)
    _check_claim_target_consistency(targets, claims_by_target, errors, gates)
    next_eligible_targets = _compute_next_eligible_targets(targets, baskets, claims_by_target, gates)

    status = "passed" if not errors else "failed"
    return {
        "schema_id": schema.get("schema_id"),
        "artifact": schema.get("artifact"),
        "status": status,
        "acceptance_result": _acceptance_result(errors),
        "error_count": len(errors),
        "errors": errors,
        "warnings": warnings,
        "validation_gates": gates,
        "details": {
            "board_id": board.get("board_id"),
            "board_status": board.get("board_status"),
            "target_count": len(_as_list(board.get("targets"))),
            "active_claim_count": len(_as_list(board.get("active_claims"))),
            "available_basket_count": len(_as_list(board.get("available_baskets"))),
        },
        "next_eligible_targets": next_eligible_targets,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Queue board YAML file")
    parser.add_argument("--schema", default=SCHEMA_PATH, type=Path, help="Queue board schema YAML file")
    parser.add_argument(
        "--handoff-schema",
        default=HANDOFF_BASKET_SCHEMA_PATH,
        type=Path,
        help="Handoff basket schema YAML file used for shared lane lists and basket validation",
    )
    parser.add_argument("--report", type=Path, help="Optional validation report output YAML")
    args = parser.parse_args(argv)

    schema = load_yaml(args.schema)
    handoff_schema = load_yaml(args.handoff_schema)
    board = load_yaml(args.input)
    report = validate_queue_board(board, schema, handoff_schema)
    report["input_path"] = str(args.input)
    report["schema_path"] = str(args.schema)
    report["handoff_schema_path"] = str(args.handoff_schema)

    if args.report:
        write_yaml(args.report, report)
    else:
        print(yaml.safe_dump(report, allow_unicode=True, sort_keys=False))

    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
