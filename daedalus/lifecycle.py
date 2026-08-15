"""One public lifecycle seam for validating and packaging Daedalus.

The module deliberately uses only Python's standard library.  Callers should use
``python -m daedalus`` rather than importing its private helpers.
"""

from __future__ import annotations

import base64
import html
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


TASK_IDS = [f"{number:03d}" for number in range(1, 51)]
PROTOTYPE_IDS = [f"{number:03d}" for number in range(41, 51)]
PROTOTYPE_VIEWPORTS = {
    "041": "desktop",
    "042": "mobile",
    "043": "mobile",
    "044": "mobile",
    "045": "desktop",
    "046": "desktop",
    "047": "desktop",
    "048": "mobile",
    "049": "mobile",
    "050": "desktop",
}
SAFE_COMPONENT = re.compile(r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$")
EXTERNAL_URL = re.compile(r"(?i)(?:https?:|ftp:|file:|//(?:[a-z0-9]|\[)|@import\s+)")
RESOURCE_ATTRIBUTE = re.compile(
    r"(?is)<(?:script|link|img|iframe|audio|video|source|object|embed)\b[^>]*\b(?:src|href|data)\s*=\s*['\"]([^'\"]+)['\"]"
)
CSS_RESOURCE = re.compile(r"(?is)url\(\s*['\"]?([^)'\"]+)")
ABSOLUTE_MACHINE_PATH = re.compile(
    r"(?i)(?:[a-z]:[\\/](?:users|documents and settings|program files|windows)[\\/]|/(?:home|users)/[^/\s]+/)"
)
VISUAL_SPEC_HEADINGS = (
    "规范元数据",
    "画布与区域布局",
    "设计令牌",
    "组件规格与状态",
    "响应式规则",
    "内容与数据",
    "动效与反馈",
    "复现验收清单",
)
PROTOTYPE_SPEC_HEADINGS = (
    "产品边界",
    "状态地图",
    "正常流程",
    "异常触发与恢复",
    "数据变化",
    "人工验收步骤",
)
INTENT_HEADINGS = ("意图元数据", "设计意图", "适用场景与目标用户", "非目标", "复刻提示词")
NON_NORMATIVE_SPEC_HEADINGS = ("一句话气质", "适合用在哪种产品", "不要做什么", "设计意图", "复刻提示词")


@dataclass
class Finding:
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message}


@dataclass
class Validation:
    root: Path
    findings: list[Finding] = field(default_factory=list)
    catalog: dict[str, Any] | None = None
    submissions: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings

    def error(self, code: str, path: Path | str, message: str) -> None:
        try:
            shown = Path(path).resolve().relative_to(self.root).as_posix()
        except (OSError, ValueError, TypeError):
            shown = str(path)
        self.findings.append(Finding(code, shown, message))

    def receipt(self, operation: str = "validate") -> dict[str, Any]:
        return {
            "schemaVersion": 1,
            "operation": operation,
            "ok": self.ok,
            "catalogTasks": len((self.catalog or {}).get("briefs", [])),
            "submissions": len(self.submissions),
            "errors": [item.as_dict() for item in self.findings],
        }


def _read_json(result: Validation, path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        result.error("missing-file", path, "缺少必需的 JSON 文件")
        return None
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        result.error("invalid-json", path, f"JSON 不是有效 UTF-8 或语法错误：{exc}")
        return None
    if not isinstance(value, dict):
        result.error("invalid-json-shape", path, "JSON 顶层必须是对象")
        return None
    return value


def _inside(base: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(base.resolve())
        return True
    except (OSError, ValueError):
        return False


def _safe_relative(value: Any, *, suffix: str | None = None) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "%" in value:
        return False
    posix = PurePosixPath(value)
    if posix.is_absolute() or any(part in ("", ".", "..") for part in posix.parts):
        return False
    return suffix is None or posix.suffix.lower() == suffix


def _catalog(result: Validation) -> None:
    path = result.root / "catalog" / "briefs.json"
    catalog = _read_json(result, path)
    if catalog is None:
        return
    result.catalog = catalog
    briefs = catalog.get("briefs")
    if catalog.get("schemaVersion", catalog.get("version")) != 3:
        result.error("catalog-version", path, "题库必须使用 schemaVersion/version 3")
    if catalog.get("count") != 50:
        result.error("catalog-count", path, "题库 count 必须为 50")
    if not isinstance(briefs, list):
        result.error("catalog-briefs", path, "briefs 必须是数组")
        return
    ids = [brief.get("id") for brief in briefs if isinstance(brief, dict)]
    if ids != TASK_IDS:
        result.error("catalog-order", path, "题目必须严格、唯一地按 001–050 排列")
    for index, brief in enumerate(briefs):
        if not isinstance(brief, dict):
            result.error("catalog-brief", path, f"第 {index + 1} 题必须是对象")
            continue
        task_id = brief.get("id", f"index-{index}")
        for key in ("id", "job", "title", "category", "scene", "viewport", "must_have"):
            if not brief.get(key):
                result.error("catalog-field", path, f"题目 {task_id} 缺少 {key}")
        if task_id in PROTOTYPE_VIEWPORTS:
            if brief.get("viewport") != PROTOTYPE_VIEWPORTS[task_id]:
                result.error("prototype-viewport", path, f"题目 {task_id} 的设备类型不符合决策记录")
            happy = brief.get("core_flow") or brief.get("happy_path") or brief.get("normal_flow")
            failure = brief.get("exception") or brief.get("failure_path") or brief.get("exception_flow")
            if not happy:
                result.error("prototype-core-flow", path, f"题目 {task_id} 缺少核心正常流程")
            if not failure:
                result.error("prototype-failure", path, f"题目 {task_id} 缺少可恢复异常流程")


def _identity(entry: dict[str, Any]) -> tuple[str, str, str] | None:
    values = (entry.get("harness"), entry.get("model"), entry.get("reasoningEffort"))
    if all(isinstance(value, str) and SAFE_COMPONENT.fullmatch(value) for value in values):
        return values  # type: ignore[return-value]
    return None


def _validate_html(result: Validation, path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        result.error("invalid-html-file", path, f"HTML 缺失或不是 UTF-8：{exc}")
        return
    lowered = text.lower()
    if "<meta" not in lowered or "charset=" not in lowered:
        result.error("html-charset", path, "HTML 必须声明字符编码")
    if not re.search(r"(?is)<meta\b[^>]*name\s*=\s*['\"]viewport['\"]", text):
        result.error("html-viewport", path, "HTML 必须声明 viewport")
    if "prefers-reduced-motion" not in lowered:
        result.error("html-reduced-motion", path, "HTML 必须处理 prefers-reduced-motion")
    match = EXTERNAL_URL.search(text)
    if match:
        result.error("html-external-resource", path, f"HTML 必须完全自包含，发现 {match.group(0)!r}")
    for resource in RESOURCE_ATTRIBUTE.findall(text) + CSS_RESOURCE.findall(text):
        normalized = resource.strip().lower()
        if normalized and not normalized.startswith(("data:", "#")):
            result.error("html-linked-resource", path, f"HTML 引用了外部文件：{resource!r}")
    ids = re.findall(r"(?is)\bid\s*=\s*['\"]([^'\"]+)['\"]", text)
    duplicates = sorted({value for value in ids if ids.count(value) > 1})
    if duplicates:
        result.error("html-duplicate-id", path, "HTML 含重复 id：" + ", ".join(duplicates))


def _section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
    )
    return match.group(1) if match else ""


def _table_data_rows(section: str) -> int:
    rows = [line for line in section.splitlines() if line.strip().startswith("|") and line.count("|") >= 3]
    return max(0, len(rows) - 2)


def _normalize_hex(value: str) -> str:
    digits = value.lstrip("#").lower()
    if len(digits) in (3, 4):
        digits = "".join(character * 2 for character in digits)
    return "#" + digits


def _validate_spec(result: Validation, path: Path, task_id: str, html_path: Path | None) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        result.error("invalid-spec-file", path, f"规范缺失或不是 UTF-8：{exc}")
        return
    required = VISUAL_SPEC_HEADINGS + (PROTOTYPE_SPEC_HEADINGS if task_id in PROTOTYPE_IDS else ())
    missing = [heading for heading in required if not re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text)]
    if missing:
        result.error("spec-headings", path, "规范缺少章节：" + "、".join(missing))
    if not re.search(r"(?m)^-\s*规范版本：\s*2\s*$", text):
        result.error("spec-version", path, "规范元数据必须声明规范版本：2")
    viewport_match = re.search(r"(?m)^-\s*主视口：\s*(\d+)\s*[×x]\s*(\d+)\s*px\s*$", text)
    if not viewport_match:
        result.error("spec-viewport", path, "规范元数据必须声明精确的像素主视口")
    else:
        briefs = (result.catalog or {}).get("briefs", [])
        brief = next((item for item in briefs if isinstance(item, dict) and item.get("id") == task_id), {})
        expected = (390, 844) if brief.get("viewport") == "mobile" else (1280, 800)
        actual = (int(viewport_match.group(1)), int(viewport_match.group(2)))
        if actual != expected:
            result.error("spec-viewport-mismatch", path, f"主视口必须与题库一致：{expected[0]} × {expected[1]} px")
    if html_path is not None:
        page_match = re.search(r"(?m)^-\s*对应页面：\s*`([^`]+)`\s*$", text)
        if not page_match or page_match.group(1) != html_path.name:
            result.error("spec-page-mismatch", path, f"对应页面必须精确填写 `{html_path.name}`")
    misplaced = [heading for heading in NON_NORMATIVE_SPEC_HEADINGS if re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text)]
    if misplaced:
        result.error("spec-non-normative", path, "以下内容应移入 .intent.md：" + "、".join(misplaced))
    if _table_data_rows(_section(text, "画布与区域布局")) < 3:
        result.error("spec-layout-rows", path, "画布与区域布局至少需要三个可测量区域")
    if _table_data_rows(_section(text, "组件规格与状态")) < 3:
        result.error("spec-component-rows", path, "组件规格与状态至少需要三个核心组件")
    colors = {_normalize_hex(value) for value in re.findall(r"(?i)#[0-9a-f]{3,8}\b", _section(text, "设计令牌"))}
    if len(colors) < 5:
        result.error("spec-colors", path, "设计令牌至少需要五个不同的十六进制色值")
    if html_path is not None:
        try:
            html_text = html_path.read_text(encoding="utf-8")
        except (FileNotFoundError, UnicodeDecodeError):
            html_text = ""
        html_colors = {_normalize_hex(value) for value in re.findall(r"(?i)#[0-9a-f]{3,8}\b", html_text)}
        absent = sorted(colors - html_colors)
        if absent:
            result.error("spec-color-mismatch", path, "规范色值未出现在 HTML：" + "、".join(absent))
    measurements = re.findall(r"(?i)\b\d+(?:\.\d+)?\s*(?:px|rem|em|vw|vh|fr|%|ms|s)\b", text)
    if len(measurements) < 8:
        result.error("spec-measurements", path, "复现规范至少需要八个带单位的精确值")
    if len(re.findall(r"(?m)^- \[ \] ", _section(text, "复现验收清单"))) < 5:
        result.error("spec-checklist", path, "复现验收清单至少需要五个未勾选的可观察检查项")


def _validate_intent(result: Validation, path: Path, spec_path: Path | None) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        result.error("invalid-intent-file", path, f"设计意图缺失或不是 UTF-8：{exc}")
        return
    missing = [heading for heading in INTENT_HEADINGS if not re.search(rf"(?m)^##\s+{re.escape(heading)}\s*$", text)]
    if missing:
        result.error("intent-headings", path, "设计意图缺少章节：" + "、".join(missing))
    if not re.search(r"(?m)^-\s*意图版本：\s*1\s*$", text):
        result.error("intent-version", path, "设计意图元数据必须声明意图版本：1")
    if spec_path is not None:
        spec_match = re.search(r"(?m)^-\s*对应规范：\s*`([^`]+)`\s*$", text)
        if not spec_match or spec_match.group(1) != spec_path.name:
            result.error("intent-spec-mismatch", path, f"对应规范必须精确填写 `{spec_path.name}`")


def _declared_path(result: Validation, folder: Path, value: Any, suffix: str, label: str) -> Path | None:
    if not _safe_relative(value, suffix=suffix):
        result.error("unsafe-declared-path", folder, f"{label} 必须是目录内的安全 {suffix} 相对路径")
        return None
    candidate = folder / PurePosixPath(value)
    if not _inside(folder, candidate):
        result.error("path-escape", candidate, f"{label} 越出答卷目录")
        return None
    return candidate


def _receipt(result: Validation, folder: Path, manifest: dict[str, Any], ident: tuple[str, str, str]) -> None:
    receipt_name = manifest.get("runReceipt", "run-receipt.json")
    receipt_path = _declared_path(result, folder, receipt_name, ".json", "runReceipt")
    if receipt_path is None:
        return
    receipt = _read_json(result, receipt_path)
    if receipt is None:
        return
    if receipt.get("schemaVersion") != 1:
        result.error("receipt-version", receipt_path, "run receipt 必须使用 schemaVersion 1")
    main = receipt.get("mainAgent")
    if not isinstance(main, dict):
        result.error("receipt-main-agent", receipt_path, "run receipt 缺少 mainAgent")
        return
    if main.get("model") != ident[1] or main.get("reasoningEffort") != ident[2]:
        result.error("receipt-identity", receipt_path, "mainAgent 的模型或思考档位与答卷身份不一致")
    subagents = receipt.get("subagents", [])
    if not isinstance(subagents, list):
        result.error("receipt-subagents", receipt_path, "subagents 必须是数组")
        return
    for index, agent in enumerate(subagents):
        if not isinstance(agent, dict) or agent.get("model") != ident[1] or agent.get("reasoningEffort") != ident[2]:
            result.error("receipt-subagent-mismatch", receipt_path, f"子 Agent {index + 1} 与主 Agent 模型或思考档位不同")


def _submission(result: Validation, entry: dict[str, Any], index_path: Path) -> None:
    ident = _identity(entry)
    if ident is None:
        result.error("submission-identity", index_path, "harness/model/reasoningEffort 必须是安全的小写路径字段")
        return
    expected = PurePosixPath("models", *ident).as_posix()
    if entry.get("path") != expected:
        result.error("submission-path", index_path, f"答卷路径必须与身份一致：{expected}")
        return
    folder = result.root.joinpath(*PurePosixPath(expected).parts)
    if not _inside(result.root / "models", folder):
        result.error("submission-path-escape", folder, "答卷路径越出 models")
        return
    manifest_path = folder / "model.json"
    if not _inside(folder, manifest_path):
        result.error("manifest-path-escape", manifest_path, "model.json 不能链接到答卷目录外")
        return
    manifest = _read_json(result, manifest_path)
    if manifest is None:
        return
    if manifest.get("schemaVersion") != 4:
        result.error("manifest-version", manifest_path, "model.json 必须使用 schemaVersion 4")
    if manifest.get("specVersion") != 2:
        result.error("manifest-spec-version", manifest_path, "model.json 必须声明 specVersion 2")
    if _identity(manifest) != ident:
        result.error("manifest-identity", manifest_path, "model.json 身份必须与登记和目录一致")
    if not isinstance(entry.get("displayName"), str) or not entry["displayName"].strip():
        result.error("submission-display-name", index_path, "登记必须包含非空 displayName")
    status = manifest.get("status")
    if status not in ("complete", "forfeited"):
        result.error("manifest-status", manifest_path, "status 只能是 complete 或 forfeited")
    if status == "forfeited":
        forfeiture = manifest.get("forfeit")
        if not isinstance(forfeiture, dict) or forfeiture.get("phrase") != "我是鸡" or not str(forfeiture.get("reason", "")).strip():
            result.error("forfeit-disclosure", manifest_path, "弃权必须包含 phrase=我是鸡 和非空 reason")
    pieces = manifest.get("pieces")
    if not isinstance(pieces, list):
        result.error("manifest-pieces", manifest_path, "pieces 必须是数组")
        return
    ids = [piece.get("id") for piece in pieces if isinstance(piece, dict)]
    if len(ids) != len(set(ids)):
        result.error("duplicate-piece-id", manifest_path, "pieces 含重复题号")
    if status == "complete" and ids != TASK_IDS:
        result.error("complete-piece-set", manifest_path, "完成答卷必须严格含 001–050")
    if status == "forfeited" and any(task_id not in TASK_IDS for task_id in ids):
        result.error("forfeit-piece-set", manifest_path, "弃权答卷含题库外题号")
    slugs: list[str] = []
    declared_files: list[str] = []
    for piece in pieces:
        if not isinstance(piece, dict):
            result.error("invalid-piece", manifest_path, "piece 必须是对象")
            continue
        task_id = piece.get("id")
        if piece.get("status") != "complete":
            result.error("piece-status", manifest_path, f"已列出的题目 {task_id} status 必须为 complete")
        slug = piece.get("slug")
        if not isinstance(slug, str) or not SAFE_COMPONENT.fullmatch(slug):
            result.error("piece-slug", manifest_path, f"题目 {task_id} slug 不安全")
        else:
            slugs.append(slug)
            expected_html = f"{task_id}-{slug}.html"
            expected_spec = f"{task_id}-{slug}.spec.md"
            expected_intent = f"{task_id}-{slug}.intent.md"
            if piece.get("file") != expected_html or piece.get("spec") != expected_spec or piece.get("intent") != expected_intent:
                result.error("piece-filename", manifest_path, f"题目 {task_id} 文件名必须由题号和 slug 唯一确定")
        if isinstance(piece.get("file"), str):
            declared_files.append(piece["file"])
        if isinstance(piece.get("spec"), str):
            declared_files.append(piece["spec"])
        if isinstance(piece.get("intent"), str):
            declared_files.append(piece["intent"])
        html_path = _declared_path(result, folder, piece.get("file"), ".html", f"题目 {task_id} file")
        spec_path = _declared_path(result, folder, piece.get("spec"), ".md", f"题目 {task_id} spec")
        intent_path = _declared_path(result, folder, piece.get("intent"), ".md", f"题目 {task_id} intent")
        if html_path is not None:
            _validate_html(result, html_path)
        if spec_path is not None and isinstance(task_id, str):
            _validate_spec(result, spec_path, task_id, html_path)
        if intent_path is not None:
            _validate_intent(result, intent_path, spec_path)
    if len(slugs) != len(set(slugs)):
        result.error("duplicate-piece-slug", manifest_path, "pieces 含重复 slug")
    if len(declared_files) != len(set(declared_files)):
        result.error("duplicate-piece-file", manifest_path, "多个题目不能复用同一个交付文件")
    _receipt(result, folder, manifest, ident)
    result.submissions.append({"entry": entry, "manifest": manifest, "folder": folder})


def validate_repository(root: Path) -> Validation:
    root = root.resolve()
    result = Validation(root)
    _catalog(result)
    index_path = root / "models" / "_index.json"
    index = _read_json(result, index_path)
    if index is None:
        return result
    if index.get("schemaVersion") != 3:
        result.error("registry-version", index_path, "登记表必须使用 schemaVersion 3")
    entries = index.get("submissions")
    if not isinstance(entries, list):
        result.error("registry-submissions", index_path, "submissions 必须是数组")
        return result
    identities: set[tuple[str, str, str]] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            result.error("registry-entry", index_path, "每个 submission 必须是对象")
            continue
        ident = _identity(entry)
        if ident in identities:
            result.error("duplicate-submission", index_path, f"重复答卷身份：{ident}")
            continue
        if ident:
            identities.add(ident)
        _submission(result, entry, index_path)
    return result


def _json_for_script(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")


GALLERY_CSS = """
:root{color-scheme:light;--paper:#f4efe3;--ink:#201d18;--muted:#736b5f;--line:#d9d0c0;--accent:#a12a2f}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,"Microsoft YaHei",sans-serif}
[hidden]{display:none!important}
header,main{width:min(1440px,100%);margin:auto;padding:24px}h1{margin:.15em 0}.kicker{color:var(--accent);letter-spacing:.16em;text-transform:uppercase}
.toolbar,.mode-switch,.submission-head,.section-head,.compare-head{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.toolbar{margin-top:18px}.toolbar label{display:flex;align-items:center;gap:7px}.mode-switch{padding:3px;border:1px solid var(--line);border-radius:999px;background:#ebe4d8}.mode-switch button{border:0;background:transparent}.mode-switch button[aria-pressed="true"],button.export{background:var(--ink);border-color:var(--ink);color:#fff}.export{margin-left:auto}
.identity{color:var(--muted)}button,select,a.open{font:inherit;border:1px solid var(--line);border-radius:999px;padding:6px 12px;background:#fff;color:inherit;text-decoration:none;cursor:pointer}button:focus-visible,select:focus-visible,a.open:focus-visible{outline:3px solid #a12a2f44;outline-offset:2px}
.submission{margin:18px 0 58px}.submission-head{justify-content:space-between;border-bottom:1px solid var(--line);padding-bottom:12px}.submission-head h2{margin:0;font-size:20px}.notice{border:2px solid var(--accent);padding:12px 16px;border-radius:12px;margin:14px 0;background:#fff}.category{margin-top:30px;scroll-margin-top:20px}.section-head{justify-content:space-between;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--line)}.section-head h3{margin:0;font-size:22px}.range{color:var(--accent);font:700 12px/1 ui-monospace,Consolas,monospace;letter-spacing:.08em}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
article{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}.preview{height:230px;background:#e5ddce}.preview iframe{width:1280px;height:800px;border:0;transform:scale(.25);transform-origin:0 0;pointer-events:none}
.meta{padding:12px}.meta h2{margin:3px 0;font-size:17px}.meta p{margin:5px 0;color:var(--muted)}.actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.empty{padding:60px 20px;text-align:center;color:var(--muted)}
.compare-head{justify-content:space-between;margin:4px 0 18px}.compare-head h2{margin:0}.compare-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(430px,100%),1fr));gap:18px}.compare-card .preview{height:340px}.compare-card .preview iframe{transform:scale(.34);pointer-events:auto}.compare-card .identity{padding:11px 12px 0}.missing{min-height:340px;display:grid;place-items:center;padding:32px;text-align:center;color:var(--muted);background:#ebe4d8}.count-note{color:var(--muted);margin:0}.badge{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:3px 8px;font-size:12px;color:var(--muted)}
body.reader-open{overflow:hidden}.reader-overlay{position:fixed;inset:0;z-index:50;display:grid;grid-template-rows:minmax(0,1fr);justify-items:end;overflow:hidden;background:#201d18b8;backdrop-filter:blur(3px)}.reader-panel{width:min(760px,calc(100% - 24px));height:100dvh;min-height:0;overflow:hidden;display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;background:#fffdf7;border-left:1px solid var(--line);box-shadow:-20px 0 60px #0003}.reader-head{display:flex;justify-content:space-between;align-items:start;gap:18px;padding:24px 26px 18px;border-bottom:1px solid var(--line)}.reader-head h2{margin:4px 0 0;font-size:24px}.reader-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.reader-kind{color:var(--accent);font:700 12px/1.2 ui-monospace,Consolas,monospace;letter-spacing:.08em}.reader-note{margin:0;padding:14px 26px;color:var(--muted);background:#f4efe3;border-bottom:1px solid var(--line)}.reader-content{min-height:0;margin:0;padding:24px 26px 60px;overflow-y:scroll;overflow-x:auto;scrollbar-gutter:stable;overscroll-behavior:contain;touch-action:pan-y;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.72 ui-monospace,Consolas,"Microsoft YaHei",monospace;scrollbar-width:auto;scrollbar-color:var(--accent) #e7dfd1}.reader-content::-webkit-scrollbar{width:13px;height:13px}.reader-content::-webkit-scrollbar-track{background:#e7dfd1}.reader-content::-webkit-scrollbar-thumb{background:var(--accent);border:3px solid #e7dfd1;border-radius:999px}.reader-content:focus-visible{outline:3px solid #a12a2f66;outline-offset:-3px}.reader-foot{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 18px;border-top:1px solid var(--line);background:#f4efe3}.reader-progress{color:var(--muted);font:700 12px/1.2 ui-monospace,Consolas,monospace}.reader-close{flex:none;background:var(--ink);color:#fff;border-color:var(--ink)}
@media(max-width:720px){header,main{padding:18px}.export{margin-left:0;width:100%}.toolbar{align-items:stretch}.toolbar>label,.mode-switch{width:100%}.toolbar select{flex:1}.mode-switch button{flex:1}.compare-card .preview{height:250px}.compare-card .preview iframe{transform:scale(.27)}.reader-panel{width:100%;height:100dvh}.reader-head{padding:18px;align-items:stretch;flex-direction:column}.reader-actions{justify-content:flex-start}.reader-note,.reader-content{padding-left:18px;padding-right:18px}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;animation:none!important;transition:none!important}}
"""


GALLERY_JS = r"""
const DATA=window.DAEDALUS_DATA;
const app=document.querySelector("main");
const answerSelect=document.querySelector("#answer-filter");
const prototypeSelect=document.querySelector("#prototype-filter");
const answerPicker=document.querySelector("#answer-picker");
const prototypePicker=document.querySelector("#prototype-picker");
const browseButton=document.querySelector("#browse-mode");
const compareButton=document.querySelector("#compare-mode");
const exportButton=document.querySelector("#export-specs");
const readerOverlay=document.querySelector("#reader-overlay");
const readerPanel=document.querySelector(".reader-panel");
const readerKind=document.querySelector("#reader-kind");
const readerTitle=document.querySelector("#reader-title");
const readerNote=document.querySelector("#reader-note");
const readerContent=document.querySelector("#reader-content");
const readerExport=document.querySelector("#reader-export");
const readerProgress=document.querySelector("#reader-progress");
const readerTop=document.querySelector("#reader-top");
const readerClose=document.querySelector("#reader-close");
const pageHeader=document.querySelector("body>header");
let mode="browse";
let readerOpener=null;
function node(name,text,cls){const n=document.createElement(name);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n}
function escapeHtml(value){return String(value).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;")}
function chosenRows(){const chosen=answerSelect?answerSelect.value:"";return chosen?DATA.submissions.filter(item=>item.key===chosen):DATA.submissions}
function updateReaderProgress(){const maximum=readerContent.scrollHeight-readerContent.clientHeight;const percent=maximum<=0?100:Math.round(readerContent.scrollTop/maximum*100);readerProgress.textContent=`阅读进度 ${percent}%`;readerProgress.setAttribute("aria-valuenow",String(percent))}
function scrollReaderByKeyboard(event){let top=null;const page=Math.max(80,Math.round(readerContent.clientHeight*.82));if(event.key==="PageDown")top=readerContent.scrollTop+page;else if(event.key==="PageUp")top=readerContent.scrollTop-page;else if(event.key==="ArrowDown")top=readerContent.scrollTop+48;else if(event.key==="ArrowUp")top=readerContent.scrollTop-48;else if(event.key==="Home")top=0;else if(event.key==="End")top=readerContent.scrollHeight;if(top===null)return;event.preventDefault();readerContent.scrollTo({top,behavior:"auto"})}
function showReader(piece,kind,opener){const normative=kind==="spec";readerOpener=opener;readerKind.textContent=normative?"复现规范 · 规范性":"设计意图 · 非规范性";readerTitle.textContent=`${piece.id} ${piece.title}`;readerNote.textContent=normative?"用于复现和验收：布局、令牌、组件状态、响应式与核心流程。":"用于理解取舍：适用场景、非目标与辅助复刻提示词；不替代正式规范。";readerExport.textContent=normative?"导出此规范":"导出此意图";readerExport.href=normative?piece.specUrl:piece.intentUrl;readerExport.download=`${piece.id}-${piece.slug}.${normative?"spec.md":"intent.md"}`;readerContent.textContent=normative?piece.spec:piece.intent;readerContent.setAttribute("aria-label",`${piece.id} ${piece.title} ${normative?"复现规范正文":"设计意图正文"}`);readerOverlay.hidden=false;document.body.classList.add("reader-open");pageHeader.inert=true;app.inert=true;readerContent.scrollTop=0;updateReaderProgress();readerContent.focus()}
function closeReader(){if(readerOverlay.hidden)return;readerOverlay.hidden=true;document.body.classList.remove("reader-open");pageHeader.inert=false;app.inert=false;const opener=readerOpener;readerOpener=null;opener?.focus()}
function cardFor(piece,compare=false){const card=node("article",undefined,compare?"compare-card":"");const preview=node("div",undefined,"preview");const frame=node("iframe");frame.setAttribute("sandbox","allow-scripts");frame.title=`${piece.id} ${piece.title}`;frame.srcdoc=piece.html;preview.append(frame);card.append(preview);const meta=node("div",undefined,"meta");meta.append(node("div",piece.id),node("h2",piece.title),node("p",piece.scene));const actions=node("div",undefined,"actions");const open=node("a","独立打开","open");open.href=piece.url;open.target="_blank";open.rel="noopener noreferrer";actions.append(open);const spec=node("button","查看规范");spec.type="button";spec.onclick=()=>showReader(piece,"spec",spec);actions.append(spec);const intent=node("button","设计意图");intent.type="button";intent.onclick=()=>showReader(piece,"intent",intent);actions.append(intent);const archive=node("a","导出方案","open");archive.href=piece.archiveUrl;archive.download=`${piece.id}-${piece.slug}-方案档案.html`;actions.append(archive);meta.append(actions);card.append(meta);return card}
function renderBrowse(){const rows=chosenRows();if(!rows.length){app.append(node("div","还没有符合新版规则的答卷。","empty"));return}for(const sub of rows){const submission=node("section",undefined,"submission");const head=node("div",undefined,"submission-head");head.append(node("h2",sub.displayName),node("div",`${sub.harness} / ${sub.model} / ${sub.reasoningEffort}`,"identity"));submission.append(head);if(sub.status==="forfeited")submission.append(node("div",`我是鸡 — ${sub.forfeitReason}`,"notice"));for(const category of DATA.categories){const pieces=sub.pieces.filter(piece=>piece.category===category.id);if(!pieces.length)continue;const block=node("section",undefined,"category");block.id=`${sub.key}-${category.id}`;const sectionHead=node("div",undefined,"section-head");sectionHead.append(node("h3",category.label),node("span",`${category.range[0]}–${category.range[1]}`,"range"));block.append(sectionHead);const grid=node("div",undefined,"grid");for(const piece of pieces)grid.append(cardFor(piece));block.append(grid);submission.append(block)}app.append(submission)}}
function renderCompare(){const taskId=prototypeSelect?.value||DATA.prototypeTasks[0]?.id;if(!taskId){app.append(node("div","题库里没有可对比的产品原型题。","empty"));return}const task=DATA.prototypeTasks.find(item=>item.id===taskId);const head=node("div",undefined,"compare-head");const title=node("div");title.append(node("span",task.id,"range"),node("h2",task.title),node("p",task.scene,"count-note"));head.append(title,node("p",`${DATA.submissions.length} 份登记答卷`,"count-note"));app.append(head);const grid=node("div",undefined,"compare-grid");for(const sub of DATA.submissions){const piece=sub.pieces.find(item=>item.id===taskId);const card=node("article",undefined,"compare-card");card.append(node("div",sub.displayName,"identity"));if(piece){const rendered=cardFor(piece,true);for(const child of Array.from(rendered.children))card.append(child)}else{const reason=sub.status==="forfeited"?`已弃权：${sub.forfeitReason}`:"尚未提交这一题";card.append(node("div",reason,"missing"))}grid.append(card)}app.append(grid);if(DATA.submissions.length<2)app.append(node("p","当前只有一份完整答卷；新的答卷通过验证后会自动加入同题并排对比。","notice"))}
function handbook(title,entries){const sections=entries.map(entry=>`<section><h2>${escapeHtml(entry.heading)}</h2><pre>${escapeHtml(entry.spec)}</pre></section>`).join("\n");return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><style>body{margin:0;background:#f4efe3;color:#201d18;font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif}main{width:min(900px,calc(100% - 32px));margin:auto;padding:40px 0 80px}h1{font-size:32px}p{color:#736b5f}section{background:#fff;border:1px solid #d9d0c0;border-radius:14px;padding:20px;margin:14px 0}h2{font-size:18px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.65 ui-monospace,Consolas,monospace}</style></head><body><main><h1>${escapeHtml(title)}</h1><p>由 Daedalus 展厅一键导出，可离线阅读。</p>${sections}</main></body></html>`}
function download(filename,text,mime){const blob=new Blob([text],{type:`${mime};charset=utf-8`});const url=URL.createObjectURL(blob);const link=node("a");link.href=url;link.download=filename;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),2000)}
function exportSpecs(){let entries=[];let title="";let filename="";if(mode==="compare"){const taskId=prototypeSelect.value;const task=DATA.prototypeTasks.find(item=>item.id===taskId);for(const sub of DATA.submissions){const piece=sub.pieces.find(item=>item.id===taskId);if(piece)entries.push({heading:`${taskId} ${piece.title} · ${sub.displayName}`,spec:piece.spec})}title=`${taskId} ${task?.title||"产品原型"} · 同题规范对比`;filename=`Daedalus-${taskId}-同题规范对比.html`}else{const rows=chosenRows();for(const sub of rows){for(const piece of sub.pieces)entries.push({heading:`${piece.id} ${piece.title}${rows.length>1?` · ${sub.displayName}`:""}`,spec:piece.spec})}title=rows.length===1?`${rows[0].displayName} · 50 题制作规范`:"Daedalus · 全部答卷制作规范";filename=rows.length===1?`${rows[0].key}-50题规范.html`:"Daedalus-全部答卷规范.html"}if(!entries.length){const old=exportButton.textContent;exportButton.textContent="没有可导出的规范";setTimeout(()=>exportButton.textContent=old,1600);return}download(filename,handbook(title,entries),"text/html")}
function render(){app.replaceChildren();if(mode==="compare")renderCompare();else renderBrowse();exportButton.textContent=mode==="compare"?"导出本题对比规范":"一键导出规范"}
function setMode(next){mode=next;browseButton.setAttribute("aria-pressed",String(next==="browse"));compareButton.setAttribute("aria-pressed",String(next==="compare"));answerPicker.hidden=next!=="browse";prototypePicker.hidden=next!=="compare";render()}
answerSelect?.addEventListener("change",render);prototypeSelect?.addEventListener("change",render);browseButton.addEventListener("click",()=>setMode("browse"));compareButton.addEventListener("click",()=>setMode("compare"));exportButton.addEventListener("click",exportSpecs);readerTop.addEventListener("click",()=>readerContent.scrollTo({top:0,behavior:"auto"}));readerContent.addEventListener("scroll",updateReaderProgress,{passive:true});readerPanel.addEventListener("keydown",scrollReaderByKeyboard);readerClose.addEventListener("click",closeReader);readerOverlay.addEventListener("click",event=>{if(event.target===readerOverlay)closeReader()});document.addEventListener("keydown",event=>{if(event.key==="Escape")closeReader()});render();
"""


def _gallery_document(payload: dict[str, Any], *, locked: bool = False) -> str:
    options = "".join(
        f'<option value="{html.escape(item["key"], quote=True)}">{html.escape(item["displayName"])}</option>'
        for item in payload["submissions"]
    )
    chooser = "" if locked else f'<label id="answer-picker">答卷 <select id="answer-filter"><option value="">全部</option>{options}</select></label>'
    prototype_options = "".join(
        f'<option value="{html.escape(item["id"], quote=True)}">{html.escape(item["id"])} · {html.escape(item["title"])}</option>'
        for item in payload["prototypeTasks"]
    )
    if locked:
        chooser = '<label id="answer-picker" hidden><select id="answer-filter"><option value="">当前答卷</option></select></label>'
    prototype_picker = f'<label id="prototype-picker" hidden>产品原型题 <select id="prototype-filter">{prototype_options}</select></label>'
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Daedalus · Product UI Model Gallery</title><style>{GALLERY_CSS}</style></head><body><header><div class="kicker">Product UI Model Gallery</div><h1>Daedalus</h1><p>50 道产品 UI 题的公开答卷展厅</p><div class="toolbar">{chooser}{prototype_picker}<div class="mode-switch" role="group" aria-label="展厅模式"><button id="browse-mode" type="button" aria-pressed="true">分区浏览</button><button id="compare-mode" type="button" aria-pressed="false">对比 041–050</button></div><button id="export-specs" class="export" type="button">一键导出规范</button></div></header><main></main><div id="reader-overlay" class="reader-overlay" hidden><section class="reader-panel" role="dialog" aria-modal="true" aria-labelledby="reader-title" aria-describedby="reader-note"><div class="reader-head"><div><div id="reader-kind" class="reader-kind"></div><h2 id="reader-title"></h2></div><div class="reader-actions"><a id="reader-export" class="open" href="#" download>导出此规范</a><button id="reader-close" class="reader-close" type="button">关闭</button></div></div><p id="reader-note" class="reader-note"></p><pre id="reader-content" class="reader-content" tabindex="0"></pre><div class="reader-foot"><span id="reader-progress" class="reader-progress" role="progressbar" aria-label="阅读进度" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">阅读进度 0%</span><button id="reader-top" type="button">回到顶部</button></div></section></div><script>window.DAEDALUS_DATA={_json_for_script(payload)};</script><script>{GALLERY_JS}</script></body></html>"""


def _piece_archive_document(
    *,
    piece: dict[str, Any],
    brief: dict[str, Any],
    submission: dict[str, Any],
    source_html: str,
    source_spec: str,
    source_intent: str,
) -> str:
    answer_name = f'{piece["id"]}-{piece["slug"]}.html'
    title = piece.get("title") or brief["title"]
    identity = (
        f'{submission.get("displayName") or submission["model"]} · '
        f'{submission["harness"]} / {submission["model"]} / {submission["reasoningEffort"]}'
    )
    encoded_html = base64.b64encode(source_html.encode("utf-8")).decode("ascii")
    raw_download = f"data:text/html;base64,{encoded_html}"
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(piece["id"])} {html.escape(title)} · 方案档案</title><style>:root{{--paper:#f4efe3;--ink:#201d18;--muted:#736b5f;--line:#d9d0c0;--accent:#a12a2f}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif}}main{{width:min(1100px,calc(100% - 32px));margin:auto;padding:36px 0 80px}}.identity,.note{{color:var(--muted)}}.actions{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}a{{display:inline-block;border:1px solid var(--ink);border-radius:999px;padding:8px 14px;background:var(--ink);color:#fff;text-decoration:none}}.preview,.document{{background:#fff;border:1px solid var(--line);border-radius:14px;margin-top:18px;overflow:hidden}}.preview-head,.document{{padding:20px}}.preview-head{{border-bottom:1px solid var(--line)}}.preview iframe{{display:block;width:100%;height:min(720px,70vh);border:0}}h1{{margin-bottom:4px}}h2{{margin:0 0 8px;font-size:20px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.7 ui-monospace,Consolas,"Microsoft YaHei",monospace}}@media(max-width:640px){{.preview iframe{{height:68vh}}}}</style></head><body><main><div class="identity">{html.escape(identity)}</div><h1>{html.escape(piece["id"])} {html.escape(title)}</h1><p class="note">{html.escape(brief["scene"])}</p><div class="actions"><a href="{raw_download}" download="{html.escape(answer_name, quote=True)}">导出原始 H5（完整运行）</a></div><section class="preview"><div class="preview-head"><h2>安全预览</h2><div class="note">预览限制存储、弹窗和跨页面能力；需要完整复现时，请导出上方原始 H5 后独立打开。</div></div><iframe sandbox="allow-scripts" title="{html.escape(title, quote=True)}" srcdoc="{html.escape(source_html, quote=True)}"></iframe></section><section class="document"><h2>复现规范</h2><pre>{html.escape(source_spec)}</pre></section><section class="document"><h2>设计意图</h2><pre>{html.escape(source_intent)}</pre></section></main></body></html>"""


def _build_payload(validation: Validation, site: Path) -> dict[str, Any]:
    catalog = validation.catalog or {}
    briefs = catalog.get("briefs", [])
    catalog_by_id = {item["id"]: item for item in briefs}
    configured_categories = catalog.get("categories")
    if isinstance(configured_categories, list) and configured_categories:
        categories = [
            {"id": item["id"], "label": item["label"], "range": item["range"]}
            for item in configured_categories
            if isinstance(item, dict) and item.get("id") and item.get("label") and isinstance(item.get("range"), list) and len(item["range"]) == 2
        ]
    else:
        categories = []
        for brief in briefs:
            category_id = brief["category"]
            found = next((item for item in categories if item["id"] == category_id), None)
            if found:
                found["range"][1] = brief["id"]
            else:
                categories.append({"id": category_id, "label": category_id, "range": [brief["id"], brief["id"]]})
    rows = []
    for item in validation.submissions:
        entry, manifest, folder = item["entry"], item["manifest"], item["folder"]
        key = "--".join((entry["harness"], entry["model"], entry["reasoningEffort"]))
        answer_dir = site / "answers" / key
        answer_dir.mkdir(parents=True, exist_ok=True)
        pieces = []
        for piece in manifest["pieces"]:
            source_html = folder / PurePosixPath(piece["file"])
            source_spec = folder / PurePosixPath(piece["spec"])
            source_intent = folder / PurePosixPath(piece["intent"])
            target_name = f'{piece["id"]}-{piece["slug"]}.html'
            target_spec_name = f'{piece["id"]}-{piece["slug"]}.spec.md'
            target_intent_name = f'{piece["id"]}-{piece["slug"]}.intent.md'
            target_archive_name = f'{piece["id"]}-{piece["slug"]}.archive.html'
            html_text = source_html.read_text(encoding="utf-8")
            spec_text = source_spec.read_text(encoding="utf-8")
            intent_text = source_intent.read_text(encoding="utf-8")
            shutil.copyfile(source_html, answer_dir / target_name)
            shutil.copyfile(source_spec, answer_dir / target_spec_name)
            shutil.copyfile(source_intent, answer_dir / target_intent_name)
            brief = catalog_by_id[piece["id"]]
            archive_html = _piece_archive_document(
                piece=piece,
                brief=brief,
                submission={**entry, "displayName": entry.get("displayName") or manifest.get("displayName")},
                source_html=html_text,
                source_spec=spec_text,
                source_intent=intent_text,
            )
            (answer_dir / target_archive_name).write_text(archive_html, encoding="utf-8")
            pieces.append(
                {
                    "id": piece["id"],
                    "slug": piece["slug"],
                    "title": piece.get("title") or brief["title"],
                    "scene": brief["scene"],
                    "category": brief["category"],
                    "html": html_text,
                    "spec": spec_text,
                    "intent": intent_text,
                    "url": f"answers/{key}/{target_name}",
                    "specUrl": f"answers/{key}/{target_spec_name}",
                    "intentUrl": f"answers/{key}/{target_intent_name}",
                    "archiveUrl": f"answers/{key}/{target_archive_name}",
                }
            )
        rows.append(
            {
                "key": key,
                "harness": entry["harness"],
                "model": entry["model"],
                "reasoningEffort": entry["reasoningEffort"],
                "displayName": entry.get("displayName") or manifest.get("displayName") or key,
                "status": manifest["status"],
                "forfeitReason": (manifest.get("forfeit") or {}).get("reason", ""),
                "pieces": pieces,
            }
        )
    prototype_tasks = [
        {"id": brief["id"], "title": brief["title"], "scene": brief["scene"]}
        for brief in briefs
        if brief["id"] in PROTOTYPE_IDS
    ]
    return {"schemaVersion": 1, "catalogCount": 50, "categories": categories, "prototypeTasks": prototype_tasks, "submissions": rows}


def _zip_tree(source: Path, destination: Path, *, prefix: str = "") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file() and item != destination):
            name = PurePosixPath(prefix, path.relative_to(source).as_posix()).as_posix()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def _enable_windows_acl_inheritance(path: Path) -> None:
    if os.name != "nt":
        return
    completed = subprocess.run(
        ["icacls", str(path), "/inheritance:e"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).decode(errors="replace").strip()
        raise PermissionError(f"unable to enable inherited ACLs for {path}: {detail}")


def _atomic_replace(staged: Path, output: Path) -> None:
    def synchronize_tree(source: Path, target: Path) -> None:
        """Mirror a complete generated tree without renaming live directories."""
        source_dirs = {path.relative_to(source) for path in source.rglob("*") if path.is_dir()}
        source_files = {path.relative_to(source) for path in source.rglob("*") if path.is_file()}
        target.mkdir(parents=True, exist_ok=True)
        for relative in sorted(source_dirs, key=lambda item: len(item.parts)):
            (target / relative).mkdir(parents=True, exist_ok=True)
        for relative in sorted(source_files):
            shutil.copy2(source / relative, target / relative)
        for path in sorted((item for item in target.rglob("*") if item.is_file()), reverse=True):
            if path.relative_to(target) not in source_files:
                path.unlink()
        for path in sorted((item for item in target.rglob("*") if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
            if path.relative_to(target) not in source_dirs:
                shutil.rmtree(path)

    backup = output.with_name(output.name + ".previous")
    if backup.exists():
        try:
            shutil.rmtree(backup)
        except OSError:
            # A stale OneDrive-managed backup must not block a new validated
            # build.  Use a unique sibling for the normal rename path; the
            # live-directory fallback below keeps its backup in system temp.
            backup = output.with_name(f"{output.name}.previous-{os.getpid()}")
    if output.exists():
        try:
            output.replace(backup)
        except PermissionError:
            # An active local preview or OneDrive can reject renaming the
            # output directory while still allowing its generated children to
            # be replaced.  Preserve a complete backup first, then synchronize
            # the already-complete staged tree into the existing directory.
            temporary_backup_root = Path(tempfile.mkdtemp(prefix=".daedalus-backup-"))
            copy_backup = temporary_backup_root / "output"
            shutil.copytree(output, copy_backup)
            try:
                _enable_windows_acl_inheritance(output)
                synchronize_tree(staged, output)
            except Exception:
                synchronize_tree(copy_backup, output)
                raise
            shutil.rmtree(staged)
            shutil.rmtree(temporary_backup_root, ignore_errors=True)
            return
    try:
        staged.replace(output)
    except PermissionError:
        # Some Windows/OneDrive filesystems allow creating the staged tree but
        # reject a directory rename with WinError 5.  Copy only from the fully
        # prepared tree and remove a partial destination on any failure.  The
        # build receipt is already inside ``staged`` and therefore still lands
        # last as part of a complete tree, never before validation.
        if output.exists():
            shutil.rmtree(output)
        try:
            shutil.copytree(staged, output)
        except Exception:
            if output.exists():
                shutil.rmtree(output)
            if backup.exists():
                backup.replace(output)
            raise
        shutil.rmtree(staged)
    except Exception:
        if backup.exists() and not output.exists():
            backup.replace(output)
        raise
    try:
        _enable_windows_acl_inheritance(output)
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        if backup.exists():
            backup.replace(output)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def _make_build_stage(parent: Path) -> Path:
    """Create an adjacent staging directory that inherits the parent's ACL.

    ``tempfile.mkdtemp`` creates directories with mode ``0o700``.  On Windows
    that becomes a protected, creator-only ACL which survives the final atomic
    rename to ``dist`` and locks out later processes running as another user.
    A normal atomic ``mkdir`` keeps the random-name guarantee while allowing
    the output directory to inherit the repository's intended permissions.
    """
    if os.name != "nt":
        return Path(tempfile.mkdtemp(prefix=".daedalus-build-", dir=parent))
    for _ in range(100):
        stage = parent / f".daedalus-build-{secrets.token_hex(8)}"
        try:
            stage.mkdir()
        except FileExistsError:
            continue
        return stage
    raise FileExistsError("unable to create a unique Daedalus build directory")


def build_repository(root: Path, output: Path) -> tuple[Validation, dict[str, Any]]:
    validation = validate_repository(root)
    receipt = validation.receipt("build")
    if not validation.ok:
        return validation, receipt
    output = output.resolve()
    root = root.resolve()
    protected = [root / name for name in ("catalog", "models", "daedalus", "gallery", "docs")]
    if output == root or any(output == item or _inside(item, output) for item in protected):
        validation.error("unsafe-output", output, "build 输出不能覆盖仓库根目录或源代码目录")
        return validation, validation.receipt("build")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = _make_build_stage(output.parent)
    try:
        site = stage / "site"
        site.mkdir()
        payload = _build_payload(validation, site)
        (site / "index.html").write_text(_gallery_document(payload), encoding="utf-8")
        for submission in payload["submissions"]:
            solo_dir = site / "submissions" / submission["key"]
            solo_dir.mkdir(parents=True)
            solo_submission = dict(submission)
            solo_submission["pieces"] = [
                dict(
                    piece,
                    url="../../" + piece["url"],
                    specUrl="../../" + piece["specUrl"],
                    intentUrl="../../" + piece["intentUrl"],
                    archiveUrl="../../" + piece["archiveUrl"],
                )
                for piece in submission["pieces"]
            ]
            solo_payload = {
                "schemaVersion": 1,
                "catalogCount": 50,
                "categories": payload["categories"],
                "prototypeTasks": payload["prototypeTasks"],
                "submissions": [solo_submission],
            }
            solo_html = _gallery_document(solo_payload, locked=True)
            (solo_dir / "index.html").write_text(solo_html, encoding="utf-8")
        _zip_tree(site, stage / "daedalus-offline-gallery.zip", prefix="daedalus-gallery")
        receipt.update(
            {
                "site": "site/index.html",
                "offlineBundle": "daedalus-offline-gallery.zip",
                "standaloneGalleries": len(payload["submissions"]),
            }
        )
        (stage / "build-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _atomic_replace(stage, output)
    except Exception:
        if stage.exists():
            shutil.rmtree(stage)
        raise
    return validation, receipt


def _starter_files(root: Path) -> Iterable[tuple[Path, str]]:
    singles = ("AGENTS.md", "README.md", "LICENSE", ".gitignore")
    for name in singles:
        path = root / name
        if path.is_file():
            yield path, name
    for base_name in ("catalog", "daedalus"):
        base = root / base_name
        if not base.exists():
            continue
        for path in sorted(item for item in base.rglob("*") if item.is_file()):
            relative = path.relative_to(root).as_posix()
            if "__pycache__" not in path.parts and not relative.endswith((".pyc", ".pyo")) and "/tests/" not in f"/{relative}/":
                yield path, relative
    for path in sorted((root / "docs" / "adr").glob("*.md")) if (root / "docs" / "adr").exists() else ():
        yield path, path.relative_to(root).as_posix()
    packer = root / "gallery" / "pack.py"
    if packer.is_file():
        yield packer, "gallery/pack.py"


def starter_repository(root: Path, output: Path) -> tuple[Validation, dict[str, Any]]:
    validation = validate_repository(root)
    receipt = validation.receipt("starter")
    if not validation.ok:
        return validation, receipt
    output = output.resolve()
    root = root.resolve()
    if output.suffix.lower() != ".zip":
        validation.error("starter-extension", output, "starter 输出必须是 .zip 文件")
        return validation, validation.receipt("starter")
    protected = [root / name for name in ("catalog", "models", "daedalus", "gallery", "docs")]
    if output == root or any(output == item or _inside(item, output) for item in protected):
        validation.error("unsafe-output", output, "starter 输出不能覆盖源代码目录")
        return validation, validation.receipt("starter")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=".daedalus-starter-", suffix=".zip", dir=output.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            entries = list(_starter_files(root))
            empty_registry = b'{\n  "schemaVersion": 3,\n  "submissions": []\n}\n'
            for source, name in entries:
                data = source.read_bytes()
                try:
                    decoded = data.decode("utf-8")
                except UnicodeDecodeError:
                    decoded = ""
                if decoded and ABSOLUTE_MACHINE_PATH.search(decoded):
                    raise ValueError(f"clean starter contains an absolute machine path: {name}")
                info = zipfile.ZipInfo(PurePosixPath("daedalus-starter", name).as_posix(), (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, data)
            info = zipfile.ZipInfo("daedalus-starter/models/_index.json", (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, empty_registry)
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    receipt.update({"starter": str(output), "files": len(list(_starter_files(root))) + 1})
    return validation, receipt
