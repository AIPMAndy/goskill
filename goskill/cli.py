"""CLI entrypoint for GoSkill."""

from __future__ import annotations

import argparse
from goskill import __version__


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GoSkill - goal-driven long-running task helper"
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    args = parser.parse_args()

    if args.version:
        print(f"goskill {__version__}")
        return

    print("GoSkill is a Python library. Start with:")
    print("  from goskill import GoSkill, goskill")
    print("  see README.md for examples")


if __name__ == "__main__":
    main()
