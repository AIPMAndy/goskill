# Contributing to GoSkill

Thanks for contributing.

GoSkill is still early, so the most valuable contributions are the ones that improve clarity and reliability.

## High-value contributions

- better execution semantics
- clearer criteria checking behavior
- stronger tests
- docs that reduce overclaiming and improve trust
- OpenClaw / agent workflow examples

## Development setup

```bash
pip install -e .[dev]
python -m pytest tests/ -q
python -m goskill.cli --version
```

## Guidelines

- keep PRs focused
- add tests when changing behavior
- prefer clear semantics over ambitious but vague abstractions
- avoid marketing claims the code cannot support yet
