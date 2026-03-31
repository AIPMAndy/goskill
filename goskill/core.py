"""Core implementation of GoSkill."""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

from .criteria import Criteria


@dataclass
class GoSkillResult:
    success: bool
    status: str
    attempts: int
    elapsed_hours: float
    result: Any
    goal: str
    criteria_report: Dict[str, Any]


class GoSkill:
    """A goal-driven helper that keeps running until criteria are met."""

    def __init__(
        self,
        goal: str,
        criteria: Dict[str, Any],
        max_hours: int = 100,
        check_interval_minutes: float = 5,
        max_attempts: Optional[int] = None,
        verbose: bool = True,
        sleep_func: Callable[[float], None] = time.sleep,
        checker: Optional[Callable[[Any, Dict[str, Any]], Dict[str, Any] | bool]] = None,
    ):
        self.goal = goal
        self.criteria = Criteria(checker=checker, **criteria)
        self.max_hours = max_hours
        self.check_interval_minutes = check_interval_minutes
        self.check_interval = check_interval_minutes * 60
        self.max_attempts = max_attempts
        self.verbose = verbose
        self.sleep_func = sleep_func
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.attempts = 0
        self.last_result: Any = None
        self.terminal_status: Optional[str] = None

    def _log(self, message: str) -> None:
        if self.verbose:
            print(message)

    def _build_result(self, success: bool, status: str, result: Any) -> GoSkillResult:
        now = self.end_time or datetime.now()
        elapsed = 0.0 if not self.start_time else (now - self.start_time).total_seconds() / 3600
        return GoSkillResult(
            success=success,
            status=status,
            attempts=self.attempts,
            elapsed_hours=elapsed,
            result=result,
            goal=self.goal,
            criteria_report=self.criteria.last_report,
        )

    def run(self, task_func: Optional[Callable[[], Any]] = None) -> Any:
        self.start_time = datetime.now()
        self.end_time = None
        self.terminal_status = None
        self._log(f"🚀 GoSkill started: {self.goal}")
        self._log(f"⏱️  Max runtime: {self.max_hours} hours")
        if self.max_attempts is not None:
            self._log(f"🔁 Max attempts: {self.max_attempts}")
        self._log(f"✅ Success criteria: {self.criteria}")

        while True:
            self.attempts += 1
            self._log(f"\n📍 Attempt #{self.attempts}")

            result = task_func() if task_func else self._execute()
            self.last_result = result

            if self.criteria.check(result):
                self.end_time = datetime.now()
                self.terminal_status = "success"
                self._log(f"\n✅ Goal achieved after {self.attempts} attempts!")
                return result

            if self.criteria.last_report.get("details"):
                self._log(f"🔎 Criteria check: {self.criteria.last_report['details']}")

            if self.max_attempts is not None and self.attempts >= self.max_attempts:
                self.end_time = datetime.now()
                self.terminal_status = "max_attempts_reached"
                self._log(f"\n🛑 Max attempts ({self.max_attempts}) reached. Stopping.")
                return None

            elapsed = datetime.now() - self.start_time
            if elapsed > timedelta(hours=self.max_hours):
                self.end_time = datetime.now()
                self.terminal_status = "timeout"
                self._log(f"\n⏰ Max time ({self.max_hours}h) reached. Stopping.")
                return None

            self._log(f"⏳ Criteria not met. Retrying in {self.check_interval_minutes} minutes...")
            self.sleep_func(self.check_interval)

    def run_with_result(self, task_func: Optional[Callable[[], Any]] = None) -> GoSkillResult:
        raw = self.run(task_func)
        if raw is not None and self.criteria.last_report.get("passed"):
            return self._build_result(True, "success", raw)
        if self.max_attempts is not None and self.attempts >= self.max_attempts:
            return self._build_result(False, "max_attempts_reached", raw)
        return self._build_result(False, "timeout", raw)

    def _execute(self) -> Any:
        return {"status": "incomplete"}

    @property
    def status(self) -> Dict[str, Any]:
        if not self.start_time:
            return {
                "status": "not_started",
                "terminal_status": None,
                "goal": self.goal,
                "criteria": self.criteria.criteria,
            }

        now = self.end_time or datetime.now()
        elapsed = now - self.start_time
        state = "completed" if self.end_time else "running"
        return {
            "status": state,
            "terminal_status": self.terminal_status,
            "goal": self.goal,
            "attempts": self.attempts,
            "elapsed_hours": elapsed.total_seconds() / 3600,
            "max_hours": self.max_hours,
            "max_attempts": self.max_attempts,
            "check_interval_minutes": self.check_interval_minutes,
            "criteria": self.criteria.criteria,
            "last_check": self.criteria.last_report,
            "last_result": self.last_result,
        }


def goskill(
    goal: str,
    criteria: Dict[str, Any],
    max_hours: int = 100,
    check_interval_minutes: float = 5,
    max_attempts: Optional[int] = None,
    verbose: bool = True,
):
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            skill = GoSkill(
                goal=goal,
                criteria=criteria,
                max_hours=max_hours,
                check_interval_minutes=check_interval_minutes,
                max_attempts=max_attempts,
                verbose=verbose,
            )
            return skill.run(lambda: func(*args, **kwargs))

        return wrapper

    return decorator
