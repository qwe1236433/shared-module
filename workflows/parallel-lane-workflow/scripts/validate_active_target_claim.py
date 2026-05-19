#!/usr/bin/env python3
"""Validate a parallel-lane active target claim."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

MODULE_ROOT = Path(__file__).resolve().parents[1]

from file_utils import load_yaml, write_yaml  # type: ignore  # noqa: E402
from validate_handoff_basket import (  # noqa: E402
    SCHEMA_PATH as HANDOFF_BASKET_SCHEMA_PATH,
    validate_basket,
)


SCHEMA_PATH = (
    MODULE_ROOT
    / "schemas"
    / "active_target_claim.schema.yaml"
)


def _is_blank(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


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


def _normalize_scope(scope: str) -> str:
    return scope.replace("\\", "/").strip().rstrip("/")


def _parse_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _check_required_root(
    claim: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    for field in _as_list(schema.get("required_root_fields")):
        if field not in claim or _is_blank(claim.get(field)):
            _add_error(errors, "missing_required_field", field, f"{field} is required")
    gates["root_required"] = "pass" if len(errors) == before else "fail"


def _check_nested_required(
    claim: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    nested_sets = [
        ("target", "required_target_fields"),
        ("source_basket", "required_source_basket_fields"),
        ("handoff_basket_on_release", "required_handoff_basket_on_release_fields"),
    ]
    for root_field, required_key in nested_sets:
        value = claim.get(root_field)
        if not isinstance(value, dict):
            if root_field in claim:
                _add_error(errors, "invalid_type", root_field, f"{root_field} must be a mapping")
            continue
        for field in _as_list(schema.get(required_key)):
            if field not in value or _is_blank(value.get(field)):
                _add_error(
                    errors,
                    "missing_required_field",
                    f"{root_field}.{field}",
                    f"{root_field}.{field} is required",
                )
    gates["nested_required"] = "pass" if len(errors) == before else "fail"


def _check_types(claim: dict[str, Any], errors: list[dict[str, str]]) -> None:
    string_fields = [
        "schema_version",
        "claim_id",
        "lane",
        "claim_status",
        "claimed_by",
        "claim_started_at",
        "review_after",
        "acceptance_standard_ref",
        "release_condition",
    ]
    for field in string_fields:
        if field in claim and not isinstance(claim.get(field), str):
            _add_error(errors, "invalid_type", field, f"{field} must be a string")

    for field in ("target", "source_basket", "handoff_basket_on_release"):
        if field in claim and not isinstance(claim.get(field), dict):
            _add_error(errors, "invalid_type", field, f"{field} must be a mapping")

    for field in ("write_scope", "forbidden_write_scope", "allowed_actions", "forbidden_actions", "blockers"):
        if field in claim and not isinstance(claim.get(field), list):
            _add_error(errors, "invalid_type", field, f"{field} must be a list")

    if "handoff_basket_on_release" in claim:
        release = _as_mapping(claim.get("handoff_basket_on_release"))
        required = release.get("required_before_release")
        if "required_before_release" in release and not isinstance(required, bool):
            _add_error(
                errors,
                "invalid_type",
                "handoff_basket_on_release.required_before_release",
                "handoff_basket_on_release.required_before_release must be a boolean",
            )


def _check_status(
    claim: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    status = claim.get("claim_status")
    allowed = _as_list(schema.get("allowed_claim_statuses"))
    if status not in allowed:
        _add_error(errors, "invalid_claim_status", "claim_status", f"claim_status must be one of {allowed}")
    gates["claim_status_valid"] = "pass" if len(errors) == before else "fail"


def _check_lane(
    claim: dict[str, Any],
    handoff_schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    lane = claim.get("lane")
    allowed_lanes = _as_list(handoff_schema.get("allowed_lanes"))
    if lane not in allowed_lanes:
        _add_error(errors, "unknown_lane", "lane", f"lane must be one of {allowed_lanes}")
    gates["lane_allowed"] = "pass" if len(errors) == before else "fail"


def _check_source_basket(
    claim: dict[str, Any],
    handoff_schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before_match = len(errors)
    lane = claim.get("lane")
    source_basket = _as_mapping(claim.get("source_basket"))
    expected_to_lane = source_basket.get("expected_to_lane")
    if expected_to_lane != lane:
        _add_error(
            errors,
            "source_basket_receiver_mismatch",
            "source_basket.expected_to_lane",
            f"source basket expected_to_lane {expected_to_lane!r} does not match claim lane {lane!r}",
        )

    basket_path_value = source_basket.get("path")
    basket_id = source_basket.get("basket_id")
    basket: dict[str, Any] | None = None
    if isinstance(basket_path_value, str) and basket_path_value.strip():
        basket_path = _repo_path(basket_path_value)
        if not basket_path.is_file():
            _add_error(
                errors,
                "source_basket_missing",
                "source_basket.path",
                f"source basket file does not exist: {basket_path}",
            )
        else:
            loaded = load_yaml(basket_path)
            if not isinstance(loaded, dict):
                _add_error(
                    errors,
                    "source_basket_invalid_type",
                    "source_basket.path",
                    "source basket root must be a mapping",
                )
            else:
                basket = loaded
                if basket.get("basket_id") != basket_id:
                    _add_error(
                        errors,
                        "source_basket_id_mismatch",
                        "source_basket.basket_id",
                        f"source_basket.basket_id {basket_id!r} does not match file basket_id {basket.get('basket_id')!r}",
                    )
                if basket.get("to_lane") != expected_to_lane:
                    _add_error(
                        errors,
                        "source_basket_to_lane_mismatch",
                        "source_basket.expected_to_lane",
                        f"source basket file is addressed to {basket.get('to_lane')!r}",
                    )

    gates["source_basket_matches_lane"] = "pass" if len(errors) == before_match else "fail"

    before_validate = len(errors)
    if basket is None:
        gates["source_basket_validates"] = "fail"
        return
    report = validate_basket(basket, handoff_schema, receiver_lane=str(lane))
    if report["status"] != "passed":
        _add_error(
            errors,
            "source_basket_validation_failed",
            "source_basket.path",
            f"source basket validation failed with {report['error_count']} error(s)",
        )
    gates["source_basket_validates"] = "pass" if len(errors) == before_validate else "fail"


def _check_write_scope(
    claim: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    scopes = claim.get("write_scope")
    forbidden_scopes = claim.get("forbidden_write_scope")
    broad_patterns = {_normalize_scope(str(item)) for item in _as_list(schema.get("broad_write_scope_patterns"))}

    if not isinstance(scopes, list) or not scopes:
        _add_error(errors, "missing_write_scope", "write_scope", "write_scope must be a non-empty list")
    else:
        for index, scope in enumerate(scopes):
            if not isinstance(scope, str) or not scope.strip():
                _add_error(errors, "invalid_write_scope", f"write_scope[{index}]", "write scope must be a non-empty string")
                continue
            normalized = _normalize_scope(scope)
            if "*" in normalized or normalized in broad_patterns or normalized.endswith("/**"):
                _add_error(
                    errors,
                    "broad_write_scope",
                    f"write_scope[{index}]",
                    f"write scope is too broad: {scope}",
                )
            if normalized.startswith("../") or "/../" in normalized:
                _add_error(
                    errors,
                    "unsafe_write_scope",
                    f"write_scope[{index}]",
                    "write scope must stay inside the repository path model",
                )

    if not isinstance(forbidden_scopes, list) or not forbidden_scopes:
        _add_error(
            errors,
            "missing_forbidden_write_scope",
            "forbidden_write_scope",
            "forbidden_write_scope must be a non-empty list",
        )
    else:
        normalized_forbidden = {
            _normalize_scope(scope) for scope in forbidden_scopes if isinstance(scope, str)
        }
        for index, scope in enumerate(scopes if isinstance(scopes, list) else []):
            if isinstance(scope, str) and _normalize_scope(scope) in normalized_forbidden:
                _add_error(
                    errors,
                    "write_scope_forbidden",
                    f"write_scope[{index}]",
                    f"write scope is explicitly forbidden: {scope}",
                )

    gates["write_scope_narrow"] = "pass" if len(errors) == before else "fail"


def _check_actions(
    claim: dict[str, Any],
    handoff_schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    if not isinstance(claim.get("allowed_actions"), list) or not claim.get("allowed_actions"):
        _add_error(errors, "missing_allowed_actions", "allowed_actions", "allowed_actions must be a non-empty list")
    else:
        for index, action in enumerate(_as_list(claim.get("allowed_actions"))):
            if not isinstance(action, str) or not action.strip():
                _add_error(
                    errors,
                    "invalid_allowed_action",
                    f"allowed_actions[{index}]",
                    "allowed action must be a non-empty string",
                )

    forbidden_actions = claim.get("forbidden_actions")
    if not isinstance(forbidden_actions, list) or not forbidden_actions:
        _add_error(
            errors,
            "missing_forbidden_actions",
            "forbidden_actions",
            "forbidden_actions must be a non-empty list",
        )
    else:
        allowed_forbidden_actions = set(_as_list(handoff_schema.get("allowed_forbidden_actions")))
        for index, action in enumerate(forbidden_actions):
            if action not in allowed_forbidden_actions:
                _add_error(
                    errors,
                    "invalid_forbidden_action",
                    f"forbidden_actions[{index}]",
                    f"unsupported forbidden action {action!r}; expected one of {sorted(allowed_forbidden_actions)}",
                )

    gates["actions_explicit"] = "pass" if len(errors) == before else "fail"


def _check_lifecycle(
    claim: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    status = claim.get("claim_status")
    release = _as_mapping(claim.get("handoff_basket_on_release"))
    blockers = _as_list(claim.get("blockers"))

    for field in ("claim_started_at", "review_after"):
        if field in claim and not _parse_datetime(claim.get(field)):
            _add_error(errors, "invalid_datetime", field, f"{field} must be ISO-8601 datetime text")

    if status == "active":
        if release.get("required_before_release") is not True:
            _add_error(
                errors,
                "missing_release_basket_requirement",
                "handoff_basket_on_release.required_before_release",
                "active claims must require a handoff basket before release",
            )
        if "released_at" in claim:
            _add_error(errors, "active_claim_has_released_at", "released_at", "active claim cannot have released_at")

    if status == "released":
        if _is_blank(claim.get("released_at")):
            _add_error(errors, "missing_released_at", "released_at", "released claims require released_at")
        if _is_blank(claim.get("actual_handoff_basket")):
            _add_error(
                errors,
                "missing_actual_handoff_basket",
                "actual_handoff_basket",
                "released claims require actual_handoff_basket",
            )

    if status in {"blocked", "returned"} and not blockers:
        _add_error(errors, "missing_blockers", "blockers", f"{status} claims require blockers")

    if status == "returned" and _is_blank(claim.get("return_to_lane")):
        _add_error(errors, "missing_return_to_lane", "return_to_lane", "returned claims require return_to_lane")

    gates["lifecycle_consistent"] = "pass" if len(errors) == before else "fail"


def _iter_claim_files(claim_dir: Path) -> list[Path]:
    if not claim_dir.exists():
        return []
    return sorted(path for path in claim_dir.rglob("*.yaml") if path.is_file())


def _check_duplicate_active_claim(
    claim: dict[str, Any],
    claim_path: Path | None,
    claim_dir: Path | None,
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    if claim_dir is None:
        gates["duplicate_active_claim"] = "not_requested"
        return

    before = len(errors)
    active_statuses = set(_as_list(schema.get("active_claim_statuses")))
    if claim.get("claim_status") not in active_statuses:
        gates["duplicate_active_claim"] = "not_applicable"
        return

    current_claim_id = claim.get("claim_id")
    current_target = _as_mapping(claim.get("target"))
    current_target_id = current_target.get("target_id")
    current_coordinate = current_target.get("coordinate")
    resolved_input = claim_path.resolve() if claim_path else None

    for path in _iter_claim_files(claim_dir):
        try:
            if resolved_input is not None and path.resolve() == resolved_input:
                continue
            other = load_yaml(path)
        except (OSError, yaml.YAMLError):
            continue
        if not isinstance(other, dict) or other.get("claim_status") not in active_statuses:
            continue
        other_target = _as_mapping(other.get("target"))
        same_target = (
            other_target.get("target_id") == current_target_id
            or other_target.get("coordinate") == current_coordinate
        )
        if same_target and other.get("claim_id") != current_claim_id:
            _add_error(
                errors,
                "duplicate_active_claim",
                "target",
                f"target is already actively claimed by {other.get('claim_id')!r} at {path}",
            )

    gates["duplicate_active_claim"] = "pass" if len(errors) == before else "fail"


def _acceptance_result(errors: list[dict[str, str]]) -> str:
    codes = {error["code"] for error in errors}
    if "duplicate_active_claim" in codes:
        return "blocked_duplicate_active_claim"
    if "source_basket_receiver_mismatch" in codes or "source_basket_to_lane_mismatch" in codes:
        return "blocked_wrong_receiver"
    if "missing_required_field" in codes or "missing_allowed_actions" in codes:
        return "blocked_missing_required_field"
    if "broad_write_scope" in codes or "write_scope_forbidden" in codes:
        return "blocked_scope_conflict"
    if errors:
        return "blocked_failed_gate"
    return "accepted"


def validate_claim(
    claim: dict[str, Any],
    schema: dict[str, Any] | None = None,
    handoff_schema: dict[str, Any] | None = None,
    *,
    claim_path: Path | None = None,
    claim_dir: Path | None = None,
) -> dict[str, Any]:
    """Return a validation report for an active target claim."""
    schema = schema or load_yaml(SCHEMA_PATH)
    handoff_schema = handoff_schema or load_yaml(HANDOFF_BASKET_SCHEMA_PATH)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    gates = {gate: "not_run" for gate in _as_list(schema.get("validation_gates"))}

    if not isinstance(claim, dict):
        _add_error(errors, "expected_mapping", "$", "Claim root must be a mapping")
        claim = {}

    if claim.get("schema_version") != schema.get("schema_id"):
        _add_error(
            errors,
            "schema_version_mismatch",
            "schema_version",
            f"schema_version must equal {schema.get('schema_id')!r}",
        )

    _check_required_root(claim, schema, errors, gates)
    _check_nested_required(claim, schema, errors, gates)
    _check_types(claim, errors)
    _check_status(claim, schema, errors, gates)
    _check_lane(claim, handoff_schema, errors, gates)
    _check_source_basket(claim, handoff_schema, errors, gates)
    _check_write_scope(claim, schema, errors, gates)
    _check_actions(claim, handoff_schema, errors, gates)
    _check_lifecycle(claim, errors, gates)
    _check_duplicate_active_claim(claim, claim_path, claim_dir, schema, errors, gates)

    status = "passed" if not errors else "failed"
    target = _as_mapping(claim.get("target"))
    source_basket = _as_mapping(claim.get("source_basket"))
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
            "claim_id": claim.get("claim_id"),
            "lane": claim.get("lane"),
            "claim_status": claim.get("claim_status"),
            "target_id": target.get("target_id"),
            "coordinate": target.get("coordinate"),
            "source_basket_id": source_basket.get("basket_id"),
            "claim_dir": str(claim_dir) if claim_dir else None,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Task claim YAML file")
    parser.add_argument("--schema", default=SCHEMA_PATH, type=Path, help="Task claim schema YAML file")
    parser.add_argument(
        "--handoff-schema",
        default=HANDOFF_BASKET_SCHEMA_PATH,
        type=Path,
        help="Handoff basket schema YAML file used for shared lane/action lists",
    )
    parser.add_argument(
        "--claim-dir",
        type=Path,
        help="Optional directory of active claims to check for duplicate target ownership",
    )
    parser.add_argument("--report", type=Path, help="Optional validation report output YAML")
    args = parser.parse_args(argv)

    schema = load_yaml(args.schema)
    handoff_schema = load_yaml(args.handoff_schema)
    claim = load_yaml(args.input)
    report = validate_claim(
        claim,
        schema,
        handoff_schema,
        claim_path=args.input,
        claim_dir=args.claim_dir,
    )
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
