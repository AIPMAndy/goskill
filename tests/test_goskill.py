import io
from contextlib import redirect_stdout

from goskill import GoSkill, goskill
from goskill.criteria import Criteria, CriteriaChecker
from goskill.cli import main


def test_criteria_checker_compile():
    assert CriteriaChecker.check_compile({"errors": 0, "warnings": 2}) is True
    assert CriteriaChecker.check_compile({"errors": 1}) is False


def test_criteria_checker_coverage():
    assert CriteriaChecker.check_coverage({"coverage": 0.9}, 0.8) is True
    assert CriteriaChecker.check_coverage({"coverage": 0.5}, 0.8) is False


def test_criteria_numeric_and_string_matching():
    criteria = Criteria(coverage=">= 90%", report="complete")
    assert criteria.check({"coverage": 95, "report": "complete"}) is True
    assert criteria.last_report["passed"] is True
    assert criteria.check({"coverage": 80, "report": "complete"}) is False


def test_goskill_status_before_run():
    skill = GoSkill(goal="test", criteria={"compile": "0 errors"}, max_hours=1)
    assert skill.status["status"] == "not_started"


def test_goskill_decorator_runs_function_once_when_criteria_met():
    calls = {"count": 0}

    @goskill(goal="demo", criteria={"done": True}, max_hours=1)
    def task():
        calls["count"] += 1
        return {"done": True}

    result = task()
    assert result == {"done": True}
    assert calls["count"] == 1


def test_goskill_status_after_run():
    skill = GoSkill(goal="ship", criteria={"done": True}, max_hours=1)
    result = skill.run(lambda: {"done": True})
    assert result == {"done": True}
    status = skill.status
    assert status["status"] == "completed"
    assert status["attempts"] == 1
    assert "criteria" in status


def test_goskill_respects_max_attempts_without_sleeping():
    calls = {"count": 0}

    def task():
        calls["count"] += 1
        return {"done": False}

    skill = GoSkill(
        goal="retry-demo",
        criteria={"done": True},
        max_hours=1,
        max_attempts=3,
        check_interval_minutes=0,
        sleep_func=lambda _: None,
    )
    result = skill.run(task)
    assert result is None
    assert calls["count"] == 3
    assert skill.status["status"] == "completed"


def test_cli_version_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["goskill", "--version"])
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    assert "goskill" in buf.getvalue().lower()
