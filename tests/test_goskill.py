import io
from contextlib import redirect_stdout

from goskill import GoSkill, goskill
from goskill.criteria import CriteriaChecker
from goskill.cli import main


def test_criteria_checker_compile():
    assert CriteriaChecker.check_compile({"errors": 0, "warnings": 2}) is True
    assert CriteriaChecker.check_compile({"errors": 1}) is False


def test_criteria_checker_coverage():
    assert CriteriaChecker.check_coverage({"coverage": 0.9}, 0.8) is True
    assert CriteriaChecker.check_coverage({"coverage": 0.5}, 0.8) is False


def test_goskill_status_before_run():
    skill = GoSkill(goal="test", criteria={"compile": "0 errors"}, max_hours=1)
    assert skill.status["status"] == "not_started"


def test_goskill_decorator_runs_function_once_when_criteria_met():
    calls = {"count": 0}

    @goskill(goal="demo", criteria={"compile": "0 errors"}, max_hours=1)
    def task():
        calls["count"] += 1
        return {"done": True}

    result = task()
    assert result == {"done": True}
    assert calls["count"] == 1


def test_cli_version_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["goskill", "--version"])
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    assert "goskill" in buf.getvalue().lower()
