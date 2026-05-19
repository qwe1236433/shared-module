#!/usr/bin/env python3
"""Tests for the parallel-lane handoff basket validator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]

from file_utils import load_yaml  # type: ignore  # noqa: E402
from validate_handoff_basket import (  # noqa: E402
    SCHEMA_PATH,
    validate_basket,
)


EXAMPLE_ROOT = MODULE_ROOT / "examples" / "handoff_baskets"
VALID_EXAMPLE = EXAMPLE_ROOT / "s03_fleabag_l2_next_gate.valid.yaml"
MISSING_ACTION_EXAMPLE = EXAMPLE_ROOT / "s03_fleabag_missing_allowed_action.invalid.yaml"
PRECISION_WITHOUT_TRIGGER_EXAMPLE = (
    EXAMPLE_ROOT / "s03_fleabag_precision_without_trigger.invalid.yaml"
)


def _load(path: Path) -> dict:
    data = load_yaml(path)
    assert isinstance(data, dict)
    return data


def _assert_failed_with(basket: dict, expected_code: str, receiver_lane: str | None = None) -> None:
    report = validate_basket(basket, receiver_lane=receiver_lane)
    assert report["status"] == "failed"
    assert any(error["code"] == expected_code for error in report["errors"]), report["errors"]


def test_valid_example_passes() -> None:
    report = validate_basket(_load(VALID_EXAMPLE), receiver_lane="S03-L2-D3-PROMOTION")
    assert report["status"] == "passed", report["errors"]
    assert report["acceptance_result"] == "accepted"


def test_missing_allowed_action_fails() -> None:
    _assert_failed_with(
        _load(MISSING_ACTION_EXAMPLE),
        "missing_required_field",
        receiver_lane="S03-L2-D3-PROMOTION",
    )


def test_wrong_receiver_fails() -> None:
    _assert_failed_with(
        _load(VALID_EXAMPLE),
        "blocked_wrong_receiver",
        receiver_lane="S03-L3-DEEP-RELATION-PREP",
    )


def test_precision_requires_named_trigger() -> None:
    _assert_failed_with(
        _load(PRECISION_WITHOUT_TRIGGER_EXAMPLE),
        "missing_precision_trigger",
        receiver_lane="S03-L2-D3-PROMOTION",
    )


def test_invalid_output_state_fails() -> None:
    basket = _load(VALID_EXAMPLE)
    basket["produced_output_state"] = "D4_relation_ready"
    _assert_failed_with(
        basket,
        "invalid_output_state",
        receiver_lane="S03-L2-D3-PROMOTION",
    )


def test_cli_writes_report() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = Path(temp_dir) / "report.yaml"
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_ROOT / "scripts" / "validate_handoff_basket.py"),
                "--input",
                str(VALID_EXAMPLE),
                "--receiver-lane",
                "S03-L2-D3-PROMOTION",
                "--report",
                str(report_path),
            ],
            cwd=MODULE_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        assert result.returncode == 0, result.stdout + result.stderr
        report = load_yaml(report_path)
        assert report["status"] == "passed"
        assert report["schema_id"] == load_yaml(SCHEMA_PATH)["schema_id"]


def main() -> int:
    tests = [
        test_valid_example_passes,
        test_missing_allowed_action_fails,
        test_wrong_receiver_fails,
        test_precision_requires_named_trigger,
        test_invalid_output_state_fails,
        test_cli_writes_report,
    ]
    for test in tests:
        test()
    print("parallel_lane_handoff_basket tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
