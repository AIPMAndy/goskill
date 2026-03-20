"""
Core implementation of GoSkill.
"""

import time
from typing import Dict, Any, Callable, Optional
from datetime import datetime, timedelta

from .criteria import Criteria


class GoSkill:
    """
    A goal-driven agent that keeps running until success criteria are met.
    
    Example:
        skill = GoSkill(
            goal="Migrate Android to HarmonyOS",
            criteria={"compile": "0 errors", "test": "100%"}
        )
        skill.run()
    """
    
    def __init__(
        self,
        goal: str,
        criteria: Dict[str, Any],
        max_hours: int = 100,
        check_interval_minutes: int = 5
    ):
        self.goal = goal
        self.criteria = Criteria(**criteria)
        self.max_hours = max_hours
        self.check_interval = check_interval_minutes * 60
        self.start_time = None
        self.attempts = 0
    
    def run(self, task_func: Optional[Callable] = None) -> Any:
        """
        Run the skill until criteria are met or max time reached.
        
        Args:
            task_func: Optional function to execute
            
        Returns:
            Final result when criteria are met
        """
        self.start_time = datetime.now()
        print(f"🚀 GoSkill started: {self.goal}")
        print(f"⏱️  Max runtime: {self.max_hours} hours")
        print(f"✅ Success criteria: {self.criteria}")
        
        while True:
            self.attempts += 1
            print(f"\n📍 Attempt #{self.attempts}")
            
            # Execute task
            if task_func:
                result = task_func()
            else:
                result = self._execute()
            
            # Check criteria
            if self.criteria.check(result):
                print(f"\n✅ Goal achieved after {self.attempts} attempts!")
                return result
            
            # Check timeout
            elapsed = datetime.now() - self.start_time
            if elapsed > timedelta(hours=self.max_hours):
                print(f"\n⏰ Max time ({self.max_hours}h) reached. Stopping.")
                return None
            
            # Wait before retry
            print(f"⏳ Criteria not met. Retrying in {self.check_interval//60} minutes...")
            time.sleep(self.check_interval)
    
    def _execute(self) -> Any:
        """Default execution logic. Override or pass task_func."""
        # Placeholder - actual implementation would do real work
        return {"status": "incomplete"}
    
    @property
    def status(self) -> Dict[str, Any]:
        """Get current status."""
        if not self.start_time:
            return {"status": "not_started"}
        
        elapsed = datetime.now() - self.start_time
        return {
            "status": "running",
            "goal": self.goal,
            "attempts": self.attempts,
            "elapsed_hours": elapsed.total_seconds() / 3600,
            "max_hours": self.max_hours
        }


def goskill(goal: str, criteria: Dict[str, Any], max_hours: int = 100):
    """
    Decorator to make a function run with GoSkill.
    
    Example:
        @goskill(goal="Migrate code", criteria={"compile": "0 errors"})
        def migrate():
            # Your migration code
            pass
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            skill = GoSkill(goal=goal, criteria=criteria, max_hours=max_hours)
            return skill.run(lambda: func(*args, **kwargs))
        return wrapper
    return decorator
