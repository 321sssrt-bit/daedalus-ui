"""Command-line adapter for the Daedalus lifecycle seam."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .lifecycle import build_repository, starter_repository, validate_repository


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m daedalus", description="Validate and package Daedalus")
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="validate catalog and current submissions")
    validate.add_argument("--root", type=Path, default=Path.cwd())
    build = commands.add_parser("build", help="validate, then atomically build galleries")
    build.add_argument("--root", type=Path, default=Path.cwd())
    build.add_argument("--output", type=Path, default=Path("dist"))
    starter = commands.add_parser("starter", help="validate, then create a sealed clean starter zip")
    starter.add_argument("--root", type=Path, default=Path.cwd())
    starter.add_argument("--output", type=Path, default=Path("dist/daedalus-starter.zip"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            result = validate_repository(args.root)
            receipt = result.receipt()
        elif args.command == "build":
            output = args.output if args.output.is_absolute() else args.root / args.output
            result, receipt = build_repository(args.root, output)
        else:
            output = args.output if args.output.is_absolute() else args.root / args.output
            result, receipt = starter_repository(args.root, output)
    except Exception as exc:  # keep automation failures machine-readable
        receipt = {
            "schemaVersion": 1,
            "operation": args.command,
            "ok": False,
            "catalogTasks": 0,
            "submissions": 0,
            "errors": [{"code": "operation-failed", "path": ".", "message": str(exc)}],
        }
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if result.ok else 1
