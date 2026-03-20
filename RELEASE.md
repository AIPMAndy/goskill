# Release Guide

## Steps

1. Update version in:
- `goskill/__init__.py`
- `setup.py`
- `pyproject.toml`
- `CHANGELOG.md`

2. Run checks:

```bash
make test
make build
```

3. Commit and tag:

```bash
git add .
git commit -m "release: vX.Y.Z"
git tag vX.Y.Z
git push origin main --tags
```

4. GitHub Actions will create the release automatically.
