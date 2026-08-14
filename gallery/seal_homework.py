"""PreToolUse gate: other models' homework is unreadable."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOW = {"decision": "allow"}
DENY_REASON = (
    "答卷密封：不能读、搜、复制其他模型的作业。"
    "只写自己的 models/<model>/。打包请运行 python gallery/pack.py。"
    "若做出来和别人像，视为品味一致。"
)


def deny(reason: str = DENY_REASON) -> int:
    print(json.dumps({"decision": "deny", "reason": reason}, ensure_ascii=False))
    return 0


def allow() -> int:
    print(json.dumps(ALLOW))
    return 0


def root() -> Path:
    env = Path(__file__).resolve().parents[1]
    return env


def session_claim_path(session_id: str) -> Path:
    folder = root() / ".grok" / "ui-lab-active"
    folder.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", session_id or "unknown")
    return folder / f"{safe}.txt"


def claimed_model(session_id: str) -> str:
    path = session_claim_path(session_id)
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def claim(session_id: str, model: str) -> None:
    session_claim_path(session_id).write_text(model, encoding="utf-8")


def norm(path: str, cwd: str) -> Path:
    raw = Path(path)
    if not raw.is_absolute():
        raw = Path(cwd or ".") / raw
    try:
        return raw.resolve()
    except OSError:
        return raw


def rel_to_root(path: Path) -> str:
    try:
        return path.resolve().relative_to(root()).as_posix()
    except Exception:
        return path.as_posix().replace("\\", "/")


def submission_from_rel(rel: str) -> str:
    match = re.match(r"models/([^/]+)/([^/]+)/([^/]+)/", rel)
    if not match:
        return ""
    parts = match.groups()
    if any(name.startswith(".") for name in parts):
        return ""
    return "/".join(parts)


def is_lifecycle_command(command: str) -> bool:
    compact = " ".join((command or "").split())
    return bool(
        re.search(r"python(?:3)?(?:\.exe)?\s+gallery/pack\.py\b", compact, re.I)
        or re.search(
            r"python(?:3)?(?:\.exe)?\s+-m\s+daedalus\s+(?:validate|build|starter)\b",
            compact,
            re.I,
        )
    )


def is_sealed_rel(rel: str, self_submission: str) -> bool:
    if rel.startswith(("archive/", "dist/")):
        return True
    if rel in {"gallery/data.js", "产品UI-综合展厅.html", "离线展厅.html"}:
        return True
    if rel.endswith("-展厅.html"):
        return True
    other = submission_from_rel(rel)
    if other and other != self_submission:
        return True
    return False


def collect_paths(tool: str, inp: dict, cwd: str) -> list[Path]:
    keys = (
        "target_file",
        "file_path",
        "path",
        "target_directory",
    )
    found: list[Path] = []
    for key in keys:
        value = inp.get(key)
        if isinstance(value, str) and value.strip():
            found.append(norm(value, cwd))
    command = inp.get("command")
    if isinstance(command, str):
        for token in re.findall(r"(?:models[/\\][^\s\"']+|[^\s\"']*展厅\.html|gallery[/\\]data\.js)", command):
            found.append(norm(token, cwd))
    return found


def command_copies_or_reads(command: str) -> bool:
    if not command:
        return False
    if is_lifecycle_command(command):
        return False
    lowered = command.lower()
    steal = (
        "copy-item",
        "copy ",
        "cp ",
        "xcopy",
        "robocopy",
        "get-content",
        "get-childitem",
        "gc ",
        "type ",
        "cat ",
        "more ",
        "findstr",
        "select-string",
        "rg ",
        "grep ",
    )
    if any(flag in lowered for flag in steal) and (
        any(name in lowered for name in ("models", "archive", "dist", "data.js"))
        or "展厅" in command
    ):
        return True
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return allow()

    tool = str(payload.get("toolName") or "")
    inp = payload.get("toolInput") or {}
    if not isinstance(inp, dict):
        inp = {}
    cwd = str(payload.get("cwd") or payload.get("workspaceRoot") or root())
    session_id = str(payload.get("sessionId") or "")
    self_submission = claimed_model(session_id)

    command = str(inp.get("command") or "")
    if is_lifecycle_command(command):
        return allow()

    if command_copies_or_reads(command):
        return deny()

    write_tools = {"search_replace", "write", "Write", "Edit", "MultiEdit"}
    paths = collect_paths(tool, inp, cwd)
    for path in paths:
        rel = rel_to_root(path)
        other = submission_from_rel(rel)
        if tool in write_tools and other:
            if not self_submission:
                claim(session_id, other)
                self_submission = other
            elif other != self_submission:
                return deny("答卷密封：这一轮已经认定你是 %s，不能写别人的答卷。" % self_submission)
        if is_sealed_rel(rel, self_submission):
            return deny()

    return allow()


if __name__ == "__main__":
    raise SystemExit(main())
