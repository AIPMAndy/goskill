"""Criteria checking utilities for GoSkill."""

from __future__ import annotations

from typing import Any, Dict


class Criteria:
    """Container for success criteria."""

    def __init__(self, **kwargs: Any):
        self.criteria = kwargs

    def check(self, result: Any) -> bool:
        """Very lightweight checker.

        Current behavior is intentionally permissive:
        - if result is exactly False / None -> fail
        - otherwise treat the attempt as successful

        This keeps the library usable today while leaving room for richer
        criterion parsing later.
        """
        return result not in (None, False)

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
