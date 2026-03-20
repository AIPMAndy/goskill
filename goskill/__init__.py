"""
GoSkill - Let your Skill keep running until goal achieved.

A goal-driven multi-agent system for OpenClaw that enables continuous execution
until success criteria are met.
"""

from .core import GoSkill, goskill
from .criteria import Criteria

__version__ = "1.0.0"
__author__ = "Andy (AI PM)"

__all__ = ["GoSkill", "goskill", "Criteria"]
