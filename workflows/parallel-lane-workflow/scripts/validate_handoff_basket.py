#!/usr/bin/env python3
"""Validate a parallel-lane handoff basket."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

MODULE_ROOT = Path(__file__).resolve().parents[1]

from file_utils import load_yaml, write_yaml  # type: ignore  # noqa: E402


SCHEMA_PATH = (
    MODULE_ROOT
    / "schemas"
    / "handoff_basket.schema.yaml"
)


def _is_blank(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _add_error(errors: list[dict[str, str]], code: str, path: str, message: str) -> None:
    errors.append({"code": code, "path": path, "message": message})


def _route_values(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str):
        return [value]
    return []


def _check_required_root(
    basket: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    for field in _as_list(schema.get("required_root_fields")):
        if field not in basket or _is_blank(basket.get(field)):
            _add_error(errors, "missing_required_field", field, f"{field} is required")
    gates["root_required"] = "pass" if len(errors) == before else "fail"


def _check_types(
    basket: dict[str, Any],
    errors: list[dict[str, str]],
) -> None:
    string_fields = [
        "schema_version",
        "basket_id",
        "from_lane",
        "to_lane",
        "source_packet",
        "accepted_input_state",
        "produced_output_state",
        "gate_result",
        "downstream_allowed_action",
        "next_basket_owner",
    ]
    for field in string_fields:
        if field in basket and not isinstance(basket.get(field), str):
            _add_error(errors, "invalid_type", field, f"{field} must be a string")

    if "ready_for_downstream" in basket and not isinstance(basket.get("ready_for_downstream"), bool):
        _add_error(
            errors,
            "invalid_type",
            "ready_for_downstream",
            "ready_for_downstream must be a boolean",
        )

    if "precision_lock_required" in basket and not isinstance(basket.get("precision_lock_required"), bool):
        _add_error(
            errors,
            "invalid_type",
            "precision_lock_required",
            "precision_lock_required must be a boolean",
        )

    for field in ("downstream_forbidden_action", "blockers"):
        if field in basket and not isinstance(basket.get(field), list):
            _add_error(errors, "invalid_type", field, f"{field} must be a list")


def _check_route(
    basket: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> dict[str, Any]:
    routes = schema.get("basket_routes")
    if not isinstance(routes, dict):
        _add_error(errors, "schema_error", "basket_routes", "schema basket_routes must be a mapping")
        gates["route_known"] = "fail"
        return {}

    basket_id = basket.get("basket_id")
    route = routes.get(basket_id)
    if not isinstance(route, dict):
        _add_error(errors, "unknown_basket_route", "basket_id", f"Unknown basket_id: {basket_id!r}")
        gates["route_known"] = "fail"
        return {}

    gates["route_known"] = "pass"

    from_allowed = _route_values(route.get("from_lane"))
    to_allowed = _route_values(route.get("to_lane"))
    if basket.get("from_lane") not in from_allowed:
        _add_error(
            errors,
            "from_lane_mismatch",
            "from_lane",
            f"from_lane must be one of {from_allowed}",
        )
    if basket.get("to_lane") not in to_allowed:
        _add_error(errors, "to_lane_mismatch", "to_lane", f"to_lane must be one of {to_allowed}")

    gates["lane_allowed"] = (
        "pass"
        if not any(err["code"] in {"from_lane_mismatch", "to_lane_mismatch"} for err in errors)
        else "fail"
    )
    return route


def _check_receiver(
    basket: dict[str, Any],
    receiver_lane: str | None,
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    if receiver_lane is None:
        gates["receiver_matches"] = "not_requested"
        return
    if basket.get("to_lane") != receiver_lane:
        _add_error(
            errors,
            "blocked_wrong_receiver",
            "to_lane",
            f"Basket is addressed to {basket.get('to_lane')!r}, not receiver {receiver_lane!r}",
        )
        gates["receiver_matches"] = "fail"
        return
    gates["receiver_matches"] = "pass"


def _check_state_transition(
    basket: dict[str, Any],
    route: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    input_state = basket.get("accepted_input_state")
    output_state = basket.get("produced_output_state")
    allowed_inputs = _as_list(route.get("allowed_input_states"))
    allowed_outputs = _as_list(route.get("allowed_output_states"))
    if input_state not in allowed_inputs:
        _add_error(
            errors,
            "invalid_input_state",
            "accepted_input_state",
            f"accepted_input_state must be one of {allowed_inputs}",
        )
    if output_state not in allowed_outputs:
        _add_error(
            errors,
            "invalid_output_state",
            "produced_output_state",
            f"produced_output_state must be one of {allowed_outputs}",
        )
    gates["state_transition_allowed"] = "pass" if len(errors) == before else "fail"


def _check_gate_result(
    basket: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    allowed = _as_list(schema.get("allowed_gate_results"))
    if basket.get("gate_result") not in allowed:
        _add_error(
            errors,
            "invalid_gate_result",
            "gate_result",
            f"gate_result must be one of {allowed}",
        )
        gates["gate_result_valid"] = "fail"
        return
    gates["gate_result_valid"] = "pass"


def _check_readiness(
    basket: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    ready = basket.get("ready_for_downstream")
    gate_result = basket.get("gate_result")
    blockers = _as_list(basket.get("blockers"))
    ready_results = set(_as_list(schema.get("ready_gate_results")))
    blocked_results = set(_as_list(schema.get("blocked_gate_results")))

    if ready is True and gate_result not in ready_results:
        _add_error(
            errors,
            "readiness_mismatch",
            "ready_for_downstream",
            "ready_for_downstream true requires an accepted gate result",
        )
    if ready is False and gate_result in ready_results and gate_result != "accepted_with_limits":
        _add_error(
            errors,
            "readiness_mismatch",
            "ready_for_downstream",
            "ready_for_downstream false requires a blocked or limited gate result",
        )
    if gate_result in blocked_results and ready is True:
        _add_error(
            errors,
            "blocked_gate_marked_ready",
            "gate_result",
            "blocked or returned basket cannot be ready_for_downstream",
        )
    if gate_result == "accepted_with_limits" and not blockers:
        _add_error(
            errors,
            "missing_blockers",
            "blockers",
            "accepted_with_limits requires blockers",
        )
    if gate_result in blocked_results and not blockers:
        _add_error(errors, "missing_blockers", "blockers", "blocked baskets require blockers")

    gates["readiness_consistent"] = "pass" if len(errors) == before else "fail"


def _check_downstream_actions(
    basket: dict[str, Any],
    route: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    if _is_blank(basket.get("downstream_allowed_action")):
        _add_error(
            errors,
            "missing_allowed_action",
            "downstream_allowed_action",
            "downstream_allowed_action is required",
        )

    forbidden_actions = basket.get("downstream_forbidden_action")
    if not isinstance(forbidden_actions, list) or not forbidden_actions:
        _add_error(
            errors,
            "missing_forbidden_action",
            "downstream_forbidden_action",
            "downstream_forbidden_action must be a non-empty list",
        )
    else:
        allowed_global = set(_as_list(schema.get("allowed_forbidden_actions")))
        allowed_route = set(_as_list(route.get("allowed_forbidden_actions")))
        allowed = allowed_route or allowed_global
        for index, action in enumerate(forbidden_actions):
            if action not in allowed:
                _add_error(
                    errors,
                    "invalid_forbidden_action",
                    f"downstream_forbidden_action[{index}]",
                    f"Unsupported forbidden action {action!r}; expected one of {sorted(allowed)}",
                )

    gates["downstream_actions_explicit"] = "pass" if len(errors) == before else "fail"


def _check_precision_trigger(
    basket: dict[str, Any],
    schema: dict[str, Any],
    errors: list[dict[str, str]],
    gates: dict[str, str],
) -> None:
    before = len(errors)
    precision_required = basket.get("precision_lock_required")
    trigger = basket.get("precision_trigger")
    allowed = _as_list(schema.get("allowed_precision_triggers"))

    if precision_required is True:
        if _is_blank(trigger):
            _add_error(
                errors,
                "missing_precision_trigger",
                "precision_trigger",
                "precision_trigger is required when precision_lock_required is true",
            )
        elif trigger not in allowed:
            _add_error(
                errors,
                "invalid_precision_trigger",
                "precision_trigger",
                f"precision_trigger must be one of {allowed}",
            )
    elif precision_required is False and not _is_blank(trigger) and trigger not in allowed:
        _add_error(
            errors,
            "invalid_precision_trigger",
            "precision_trigger",
            f"precision_trigger must be one of {allowed}",
        )

    gates["precision_trigger_valid"] = "pass" if len(errors) == before else "fail"


def _acceptance_result(errors: list[dict[str, str]]) -> str:
    codes = {error["code"] for error in errors}
    if "blocked_wrong_receiver" in codes:
        return "blocked_wrong_receiver"
    if "missing_required_field" in codes or "missing_allowed_action" in codes:
        return "blocked_missing_required_field"
    if errors:
        return "blocked_failed_gate"
    return "accepted"


def validate_basket(
    basket: dict[str, Any],
    schema: dict[str, Any] | None = None,
    *,
    receiver_lane: str | None = None,
) -> dict[str, Any]:
    """Return a validation report for a handoff basket."""
    schema = schema or load_yaml(SCHEMA_PATH)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    gates = {gate: "not_run" for gate in _as_list(schema.get("validation_gates"))}

    if not isinstance(basket, dict):
        _add_error(errors, "expected_mapping", "$", "Basket root must be a mapping")
        basket = {}

    if basket.get("schema_version") != schema.get("schema_id"):
        _add_error(
            errors,
            "schema_version_mismatch",
            "schema_version",
            f"schema_version must equal {schema.get('schema_id')!r}",
        )

    _check_required_root(basket, schema, errors, gates)
    _check_types(basket, errors)
    route = _check_route(basket, schema, errors, gates)
    _check_receiver(basket, receiver_lane, errors, gates)
    if route:
        _check_state_transition(basket, route, errors, gates)
        _check_downstream_actions(basket, route, schema, errors, gates)
    _check_gate_result(basket, schema, errors, gates)
    _check_readiness(basket, schema, errors, gates)
    _check_precision_trigger(basket, schema, errors, gates)

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
            "basket_id": basket.get("basket_id"),
            "from_lane": basket.get("from_lane"),
            "to_lane": basket.get("to_lane"),
            "receiver_lane": receiver_lane,
            "source_packet": basket.get("source_packet"),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Handoff basket YAML file")
    parser.add_argument("--schema", default=SCHEMA_PATH, type=Path, help="Basket schema YAML file")
    parser.add_argument("--receiver-lane", help="Lane that is trying to consume the basket")
    parser.add_argument("--report", type=Path, help="Optional validation report output YAML")
    args = parser.parse_args(argv)

    schema = load_yaml(args.schema)
    basket = load_yaml(args.input)
    report = validate_basket(basket, schema, receiver_lane=args.receiver_lane)
    report["input_path"] = str(args.input)
    report["schema_path"] = str(args.schema)

    if args.report:
        write_yaml(args.report, report)
    else:
        print(yaml.safe_dump(report, allow_unicode=True, sort_keys=False))

    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
