"""Criteria checking utilities for GoSkill."""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, Optional


class Criteria:
    """Container for success criteria with lightweight evaluation support."""

    def __init__(self, checker: Optional[Callable[[Any, Dict[str, Any]], Dict[str, Any] | bool]] = None, **kwargs: Any):
        self.criteria = kwargs
        self.checker = checker
        self.last_report: Dict[str, Any] = {}

    def _parse_numeric_expression(self, expression: str) -> Optional[tuple[str, float, bool]]:
        m = re.match(r"^\s*(>=|<=|>|<|==?)\s*(-?[0-9]+(?:\.[0-9]+)?)\s*(%)?\s*$", expression)
        if not m:
            return None
        op, raw, percent = m.groups()
        return op, float(raw), bool(percent)

    def _compare_numeric(self, actual: float, expression: str) -> bool:
        parsed = self._parse_numeric_expression(expression)
        if not parsed:
            return False
        op, expected, _ = parsed
        if op == ">":
            return actual > expected
        if op == ">=":
            return actual >= expected
        if op == "<":
            return actual < expected
        if op == "<=":
            return actual <= expected
        return actual == expected

    def _normalize_numeric(self, value: Any, expect_percent_scale: bool) -> float:
        if isinstance(value, str) and value.strip().endswith("%"):
            numeric = float(value.strip().rstrip("%"))
            return numeric if expect_percent_scale else numeric / 100
        if isinstance(value, (int, float)):
            numeric = float(value)
            if expect_percent_scale and 0 <= numeric <= 1:
                return numeric * 100
            return numeric
        return float(value)

    def _run_custom_checker(self, result: Any) -> Optional[bool]:
        if not self.checker:
            return None
        custom = self.checker(result, self.criteria)
        if isinstance(custom, bool):
            self.last_report = {
                "passed": custom,
                "reason": "custom_checker",
                "details": {},
            }
            return custom
        if isinstance(custom, dict):
            passed = bool(custom.get("passed", False))
            self.last_report = {
                "passed": passed,
                "reason": custom.get("reason", "custom_checker"),
                "details": custom.get("details", {}),
            }
            return passed
        raise TypeError("custom checker must return bool or dict")

    def check(self, result: Any) -> bool:
        custom_outcome = self._run_custom_checker(result)
        if custom_outcome is not None:
            return custom_outcome

        if result in (None, False):
            self.last_report = {"passed": False, "reason": "empty_result", "details": {}}
            return False

        if not self.criteria:
            self.last_report = {"passed": True, "reason": "no_criteria", "details": {}}
            return True

        if not isinstance(result, dict):
            self.last_report = {"passed": False, "reason": "non_dict_result", "details": {}}
            return False

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
                        parsed = self._parse_numeric_expression(exp)
                        if parsed:
                            _, _, expect_percent_scale = parsed
                            actual_numeric = self._normalize_numeric(actual, expect_percent_scale)
                            passed = self._compare_numeric(actual_numeric, exp)
                        else:
                            passed = False
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
