"""
Criteria checking utilities for GoSkill.
"""

from typing import Any, Dict, Union


class CriteriaChecker:
    """Check if results meet defined criteria."""
    
    @staticmethod
    def check_compile(result: Dict) -> bool:
        """Check if compilation has 0 errors."""
        errors = result.get("errors", 0)
        warnings = result.get("warnings", 0)
        return errors == 0
    
    @staticmethod
    def check_test_pass_rate(result: Dict, threshold: float = 1.0) -> bool:
        """Check if test pass rate meets threshold."""
        total = result.get("total_tests", 0)
        passed = result.get("passed_tests", 0)
        if total == 0:
            return False
        return (passed / total) >= threshold
    
    @staticmethod
    def check_performance(result: Dict, baseline: float, threshold: float = 0.9) -> bool:
        """Check if performance is within threshold of baseline."""
        current = result.get("performance", 0)
        return (current / baseline) >= threshold
    
    @staticmethod
    def check_coverage(result: Dict, threshold: float = 0.8) -> bool:
        """Check if code coverage meets threshold."""
        coverage = result.get("coverage", 0)
        return coverage >= threshold
