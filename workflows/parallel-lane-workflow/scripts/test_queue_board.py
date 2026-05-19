#!/usr/bin/env python3
"""Tests for the parallel-lane queue board validator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]

from file_utils import load_yaml  # type: ignore  # noqa: E402
from validate_queue_board import SCHEMA_PATH, validate_queue_board  # noqa: E402


EXAMPLE_ROOT = MODULE_ROOT / "examples" / "queue_boards"
VALID_EXAMPLE = EXAMPLE_ROOT / "s03_parallel_lane_queue_board.valid.yaml"
DUPLICATE_CLAIM_EXAMPLE = EXAMPLE_ROOT / "s03_parallel_lane_queue_board_duplicate_claim.invalid.yaml"
UNCLAIMED_CONFLICT_EXAMPLE = EXAMPLE_ROOT / "s03_parallel_lane_queue_board_unclaimed_conflict.invalid.yaml"
WRONG_RECEIVER_EXAMPLE = EXAMPLE_ROOT / "s03_parallel_lane_queue_board_wrong_receiver.invalid.yaml"
BAD_CLAIM_EXAMPLE = (
    MODULE_ROOT
    / "examples"
    / "task_claims"
    / "s03_fleabag_broad_write_scope.invalid.yaml"
)


def _load(path: Path) -> dict:
    data = load_yaml(path)
    assert isinstance(data, dict)
    return data


def _assert_failed_with(board: dict, expected_code: str) -> None:
    report = validate_queue_board(board)
    assert report["status"] == "failed"
    assert any(error["code"] == expected_code for error in report["errors"]), report["errors"]


def test_valid_example_passes_and_lists_next_target() -> None:
    report = validate_queue_board(_load(VALID_EXAMPLE))
    assert report["status"] == "passed", report["errors"]
    assert report["acceptance_result"] == "accepted"
    assert report["next_eligible_targets"] == [
        {
            "target_id": "S03-D3-CAND-003-CASABLANCA",
            "coordinate": "S03-L2A-D3-CASABLANCA",
            "lane": "S03-L2-D3-PROMOTION",
            "priority": "P2",
            "source_basket_ref": "S03-BASKET-REF-CASABLANCA-L2-NEXT-GATE-20260519",
            "next_allowed_action": "separate A02 and A05 source clips and preserve locator limits",
        }
    ]


def test_duplicate_active_claim_fails() -> None:
    _assert_failed_with(_load(DUPLICATE_CLAIM_EXAMPLE), "duplicate_active_claim")


def test_unclaimed_target_with_active_claim_fails() -> None:
    _assert_failed_with(_load(UNCLAIMED_CONFLICT_EXAMPLE), "target_unclaimed_has_active_claim")


def test_wrong_receiver_fails() -> None:
    _assert_failed_with(_load(WRONG_RECEIVER_EXAMPLE), "basket_target_lane_mismatch")


def test_invalid_active_claim_fails() -> None:
    board = _load(VALID_EXAMPLE)
    board["active_claims"][0]["path"] = str(BAD_CLAIM_EXAMPLE.relative_to(MODULE_ROOT))
    _assert_failed_with(board, "active_claim_validation_failed")


def test_cli_writes_report() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = Path(temp_dir) / "report.yaml"
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_ROOT / "scripts" / "validate_queue_board.py"),
                "--input",
                str(VALID_EXAMPLE),
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
        test_valid_example_passes_and_lists_next_target,
        test_duplicate_active_claim_fails,
        test_unclaimed_target_with_active_claim_fails,
        test_wrong_receiver_fails,
        test_invalid_active_claim_fails,
        test_cli_writes_report,
    ]
    for test in tests:
        test()
    print("parallel_lane_queue_board tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
