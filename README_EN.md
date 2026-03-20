<div align="center">

# GoSkill

**Turn a one-shot Skill into a goal-driven execution loop that keeps going until success criteria are met or time runs out.**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Tests](https://github.com/AIPMAndy/goskill/actions/workflows/tests.yml/badge.svg)](https://github.com/AIPMAndy/goskill/actions/workflows/tests.yml)

**English | [简体中文](README.md)**

*Not a magic autonomous agent platform — a more honest execution wrapper for long-running tasks with explicit success criteria.*

</div>

---

## Why GoSkill?

A lot of tasks do not fail because they are impossible.
They fail because:

- they stop after one attempt
- the completion criteria are vague
- long-running work has no built-in validation loop
- the final output says “done” but nobody knows whether it actually meets the bar

GoSkill is meant to address that gap:

> **turn a one-shot task into a goal-driven execution pattern with retries, checks, and a stopping condition.**

It is better thought of as a **goal-driven execution helper**, not an all-powerful autonomous framework.

---

## In one sentence

If a normal Skill runs once and returns, GoSkill is the pattern where you:

- define the goal
- define the success criteria
- keep trying / checking / retrying
- stop only when the goal is met or time expires

---

## 🆚 What is it good for?

| Scenario | Normal function / Skill | GoSkill |
|----------|--------------------------|---------|
| One-shot short tasks | ✅ | — |
| Long-running iterative work | — | ✅ |
| Explicit acceptance criteria | 🟡 | ✅ |
| Built-in status tracking | 🟡 | ✅ |
| Multi-attempt execution loops | 🟡 | ✅ |

**The value of GoSkill is not “more intelligence”, but “better execution discipline around goals”.**

---

## 🚀 Quick start

### Install

```bash
pip install -e .
```

### Decorator style

```python
from goskill import goskill

@goskill(
    goal="Migrate an Android project to HarmonyOS",
    criteria={
        "compile": "0 errors",
        "test": "100% pass",
        "performance": ">= 90%"
    },
    max_hours=48
)
def migrate():
    return {"done": True}

migrate()
```

### Class style

```python
from goskill import GoSkill

skill = GoSkill(
    goal="Analyze 1000 financial reports",
    criteria={
        "coverage": "100%",
        "accuracy": ">= 95%",
        "report": "complete"
    },
    max_hours=24,
)

result = skill.run(lambda: {"done": True})
print(result)
```

---

## Core ideas

### 1) Goal-driven
Instead of only passing a function, you describe the task as:
- **goal**: what should be achieved
- **criteria**: what counts as success
- **max_hours**: how long it is allowed to keep trying

### 2) Persistent attempts
If the criteria are not met, GoSkill does not assume one execution is enough.
It keeps going until:
- success
- timeout
- or manual stop

### 3) Trackable status
Built-in `status` lets you inspect:
- current goal
- attempt count
- elapsed runtime
- max runtime

---

## How it works

```text
Define goal + success criteria
        ↓
Run task function
        ↓
Check if result meets criteria
        ↓
Success → return result
Not enough → wait and retry
        ↓
Repeat until success or timeout
```

---

## Good fit / bad fit

### Good fit
- large refactors
- long-running analysis tasks
- automation with explicit acceptance criteria
- research-style iterative tasks
- workflows that need execution + validation + retry in one wrapper

### Bad fit
- simple one-shot Q&A
- tiny synchronous functions
- tasks with no meaningful acceptance criteria
- production-grade distributed orchestration systems

---

## Current project status

Right now GoSkill is best understood as:

- **an execution pattern prototype**
- **a lightweight Python helper**
- **an experimental wrapper for OpenClaw / agent workflows**

It is **not yet** a full long-running autonomous agent platform.

That clarity is a feature, not a weakness.
Better alignment = higher trust.

---

## Development

```bash
make install-dev
make test
make build
make version
```

---

## Related docs

- [README.md](README.md) — Chinese version
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution guide
- [CHANGELOG.md](CHANGELOG.md) — release notes
- [SECURITY.md](SECURITY.md) — security notes
- [RELEASE.md](RELEASE.md) — release process
- [Makefile](Makefile) — common dev commands
- [SKILL.md](SKILL.md) — OpenClaw Skill-oriented usage

---

## License

[Apache-2.0](LICENSE)

---

<div align="center">

**If you're building long-running, goal-driven workflows, give it a Star ⭐**

</div>
