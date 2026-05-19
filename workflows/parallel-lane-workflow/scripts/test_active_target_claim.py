#!/usr/bin/env python3
"""Tests for the parallel-lane active target claim validator."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MODULE_ROOT = Path(__file__).resolve().parents[1]

from file_utils import load_yaml, write_yaml  # type: ignore  # noqa: E402
from validate_active_target_claim import (  # noqa: E402
    SCHEMA_PATH,
    validate_claim,
)


EXAMPLE_ROOT = MODULE_ROOT / "examples" / "task_claims"
VALID_EXAMPLE = EXAMPLE_ROOT / "s03_fleabag_active_claim.valid.yaml"
BROAD_SCOPE_EXAMPLE = EXAMPLE_ROOT / "s03_fleabag_broad_write_scope.invalid.yaml"
MISSING_RELEASE_EXAMPLE = EXAMPLE_ROOT / "s03_fleabag_missing_release_condition.invalid.yaml"
WRONG_RECEIVER_EXAMPLE = EXAMPLE_ROOT / "s03_fleabag_wrong_source_receiver.invalid.yaml"


def _load(path: Path) -> dict:
    data = load_yaml(path)
    assert isinstance(data, dict)
    return data


def _assert_failed_with(claim: dict, expected_code: str, claim_dir: Path | None = None) -> None:
    report = validate_claim(claim, claim_dir=claim_dir)
    assert report["status"] == "failed"
    assert any(error["code"] == expected_code for error in report["errors"]), report["errors"]


def test_valid_example_passes() -> None:
    report = validate_claim(_load(VALID_EXAMPLE))
    assert report["status"] == "passed", report["errors"]
    assert report["acceptance_result"] == "accepted"
    assert report["validation_gates"]["source_basket_validates"] == "pass"


def test_broad_write_scope_fails() -> None:
    _assert_failed_with(_load(BROAD_SCOPE_EXAMPLE), "broad_write_scope")


def test_missing_release_condition_fails() -> None:
    _assert_failed_with(_load(MISSING_RELEASE_EXAMPLE), "missing_required_field")


def test_wrong_source_receiver_fails() -> None:
    _assert_failed_with(_load(WRONG_RECEIVER_EXAMPLE), "source_basket_to_lane_mismatch")


def test_duplicate_active_claim_fails() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        claim_dir = Path(temp_dir)
        first = claim_dir / "first.claim.yaml"
        second = claim_dir / "second.claim.yaml"
        shutil.copyfile(VALID_EXAMPLE, first)
        duplicate = _load(VALID_EXAMPLE)
        duplicate["claim_id"] = "S03-CLAIM-20260519-L2-FLEABAG-DUPLICATE"
        write_yaml(second, duplicate)

        report = validate_claim(duplicate, claim_path=second, claim_dir=claim_dir)
        assert report["status"] == "failed"
        assert any(error["code"] == "duplicate_active_claim" for error in report["errors"]), report["errors"]


def test_cli_writes_report() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = Path(temp_dir) / "report.yaml"
        result = subprocess.run(
            [
                sys.executable,
                str(MODULE_ROOT / "scripts" / "validate_active_target_claim.py"),
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
        test_valid_example_passes,
        test_broad_write_scope_fails,
        test_missing_release_condition_fails,
        test_wrong_source_receiver_fails,
        test_duplicate_active_claim_fails,
        test_cli_writes_report,
    ]
    for test in tests:
        test()
    print("parallel_lane_active_target_claim tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
