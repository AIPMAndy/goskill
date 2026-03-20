"""Criteria checking utilities for GoSkill."""

from __future__ import annotations

import re
from typing import Any, Dict


class Criteria:
    """Container for success criteria with lightweight evaluation support."""

    def __init__(self, **kwargs: Any):
        self.criteria = kwargs
        self.last_report: Dict[str, Any] = {}

    def _compare_numeric(self, actual: float, expression: str) -> bool:
        m = re.match(r"^\s*(>=|<=|>|<|==?)\s*([0-9]+(?:\.[0-9]+)?)\s*%?\s*$", expression)
        if not m:
            return False
        op, raw = m.groups()
        expected = float(raw)
        if op == ">":
            return actual > expected
        if op == ">=":
            return actual >= expected
        if op == "<":
            return actual < expected
        if op == "<=":
            return actual <= expected
        return actual == expected

    def _normalize_percent(self, value: Any) -> float:
        if isinstance(value, str) and value.strip().endswith("%"):
            return float(value.strip().rstrip("%"))
        if isinstance(value, (int, float)):
            return float(value) * 100 if 0 <= float(value) <= 1 else float(value)
        return float(value)

    def check(self, result: Any) -> bool:
        if result in (None, False):
            self.last_report = {"passed": False, "reason": "empty_result", "details": {}}
            return False

        if not self.criteria:
            self.last_report = {"passed": True, "reason": "no_criteria", "details": {}}
            return True

        if not isinstance(result, dict):
            self.last_report = {"passed": True, "reason": "non_dict_result", "details": {}}
            return True

        details: Dict[str, Dict[str, Any]] = {}
        all_passed = True

        for key, expected in self.criteria.items():
            actual = result.get(key)
            passed = False

            if actual is None:
                passed = False
            elif isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
                passed = float(actual) >= float(expected)
            elif isinstance(expected, str) and isinstance(actual, (int, float, str)):
                exp = expected.strip()
                if exp.endswith("%") or exp.startswith((">", "<", "=")):
                    try:
                        passed = self._compare_numeric(self._normalize_percent(actual), exp)
                    except Exception:
                        passed = False
                else:
                    passed = str(actual).strip().lower() == exp.lower()
            else:
                passed = actual == expected

            details[key] = {
                "expected": expected,
                "actual": actual,
                "passed": passed,
            }
            all_passed = all_passed and passed

        self.last_report = {"passed": all_passed, "reason": "criteria_checked", "details": details}
        return all_passed

    def __repr__(self) -> str:
        return f"Criteria({self.criteria})"


class CriteriaChecker:
    """Check if results meet defined criteria."""

    @staticmethod
    def check_compile(result: Dict[str, Any]) -> bool:
        errors = result.get("errors", 0)
        return errors == 0

    @staticmethod
    def check_test_pass_rate(result: Dict[str, Any], threshold: float = 1.0) -> bool:
        total = result.get("total_tests", 0)
        passed = result.get("passed_tests", 0)
        if total == 0:
            return False
        return (passed / total) >= threshold

    @staticmethod
    def check_performance(result: Dict[str, Any], baseline: float, threshold: float = 0.9) -> bool:
        current = result.get("performance", 0)
        if baseline == 0:
            return False
        return (current / baseline) >= threshold

    @staticmethod
    def check_coverage(result: Dict[str, Any], threshold: float = 0.8) -> bool:
        coverage = result.get("coverage", 0)
        return coverage >= threshold
