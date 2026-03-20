"""Core implementation of GoSkill."""

from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

from .criteria import Criteria


class GoSkill:
    """
    A goal-driven helper that keeps running until criteria are met.

    Example:
        skill = GoSkill(
            goal="Migrate Android to HarmonyOS",
            criteria={"compile": "0 errors", "test": "100%"}
        )
        skill.run(lambda: {"compile": "0 errors", "test": "100%"})
    """

    def __init__(
        self,
        goal: str,
        criteria: Dict[str, Any],
        max_hours: int = 100,
        check_interval_minutes: float = 5,
        max_attempts: Optional[int] = None,
        sleep_func: Callable[[float], None] = time.sleep,
    ):
        self.goal = goal
        self.criteria = Criteria(**criteria)
        self.max_hours = max_hours
        self.check_interval_minutes = check_interval_minutes
        self.check_interval = check_interval_minutes * 60
        self.max_attempts = max_attempts
        self.sleep_func = sleep_func
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.attempts = 0
        self.last_result: Any = None

    def run(self, task_func: Optional[Callable[[], Any]] = None) -> Any:
        """Run until criteria are met, attempts are exhausted, or time runs out."""
        self.start_time = datetime.now()
        self.end_time = None
        print(f"🚀 GoSkill started: {self.goal}")
        print(f"⏱️  Max runtime: {self.max_hours} hours")
        if self.max_attempts is not None:
            print(f"🔁 Max attempts: {self.max_attempts}")
        print(f"✅ Success criteria: {self.criteria}")

        while True:
            self.attempts += 1
            print(f"\n📍 Attempt #{self.attempts}")

            result = task_func() if task_func else self._execute()
            self.last_result = result

            if self.criteria.check(result):
                self.end_time = datetime.now()
                print(f"\n✅ Goal achieved after {self.attempts} attempts!")
                return result

            if self.criteria.last_report.get("details"):
                print("🔎 Criteria check:", self.criteria.last_report["details"])

            if self.max_attempts is not None and self.attempts >= self.max_attempts:
                self.end_time = datetime.now()
                print(f"\n🛑 Max attempts ({self.max_attempts}) reached. Stopping.")
                return None

            elapsed = datetime.now() - self.start_time
            if elapsed > timedelta(hours=self.max_hours):
                self.end_time = datetime.now()
                print(f"\n⏰ Max time ({self.max_hours}h) reached. Stopping.")
                return None

            print(f"⏳ Criteria not met. Retrying in {self.check_interval_minutes} minutes...")
            self.sleep_func(self.check_interval)

    def _execute(self) -> Any:
        """Default execution logic. Override or pass task_func."""
        return {"status": "incomplete"}

    @property
    def status(self) -> Dict[str, Any]:
        """Get current status snapshot."""
        if not self.start_time:
            return {"status": "not_started", "goal": self.goal, "criteria": self.criteria.criteria}

        now = self.end_time or datetime.now()
        elapsed = now - self.start_time
        state = "completed" if self.end_time else "running"
        return {
            "status": state,
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
):
    """Decorator to run a function with GoSkill semantics."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            skill = GoSkill(
                goal=goal,
                criteria=criteria,
                max_hours=max_hours,
                check_interval_minutes=check_interval_minutes,
                max_attempts=max_attempts,
            )
            return skill.run(lambda: func(*args, **kwargs))

        return wrapper

    return decorator
