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


FAVICON_LINK = """<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23242424'/%3E%3Ctext x='32' y='44' font-family='system-ui' font-size='36' font-weight='700' text-anchor='middle' fill='%23f5f5f3'%3ED%3C/text%3E%3C/svg%3E">"""

GALLERY_CSS = """
:root{color-scheme:light;--paper:#f5f5f3;--ink:#242424;--muted:#71716b;--line:#deded8;--accent:#a12a2f;--dock-height:53px;--header-height:49px}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:13px/1.4 system-ui,"Microsoft YaHei",sans-serif;overflow:hidden}
[hidden]{display:none!important}
.project-header{position:relative;z-index:30;display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:12px;padding:6px 12px;border-bottom:1px solid var(--line)}.workspace-heading,.compare-title{display:flex;align-items:center;gap:8px;min-width:0}.workspace-heading .compare-title{flex:1}.workspace-heading h1{margin:0;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.project-info summary{font-weight:750;font-size:17px;letter-spacing:-.04em}.project-description{position:absolute;top:100%;left:8px;width:min(460px,calc(100vw - 16px));padding:16px;border:1px solid var(--line);border-radius:8px;background:#fff;box-shadow:0 8px 28px #0002}.project-description p{margin:8px 0;color:var(--muted)}
.toolbar{position:fixed;inset:auto 0 0;z-index:25;display:grid;grid-template-columns:auto minmax(140px,.8fr) minmax(300px,1.6fr) auto;align-items:center;gap:10px;padding:8px 12px max(8px,env(safe-area-inset-bottom));border-top:1px solid var(--line);background:#fff;max-height:45dvh;overflow:auto}.toolbar label{display:flex;align-items:center;gap:6px;min-width:0;font-size:11px;color:var(--muted);white-space:nowrap}.toolbar select{min-width:0;max-width:100%;font-size:12px;color:var(--ink)}.mode-switch,.dock-actions{display:flex;align-items:center;gap:4px}.mode-switch button{border-color:transparent;background:transparent;font-size:11px;padding-inline:9px;white-space:nowrap}.mode-switch button[aria-pressed="true"],button.export{background:var(--ink);border-color:var(--ink);color:#fff}.dock-actions{grid-column:4}.dock-actions button{font-size:11px;white-space:nowrap}
button,select,a.open,summary{font:inherit;line-height:20px;min-height:36px;border:1px solid var(--line);border-radius:6px;padding:7px 10px;background:#fff;color:inherit;text-decoration:none;cursor:pointer}button,a.open,summary{display:inline-flex;align-items:center;justify-content:center}summary{list-style:none}summary::-webkit-details-marker{display:none}button:focus-visible,select:focus-visible,a.open:focus-visible,summary:focus-visible{outline:3px solid #a12a2f88;outline-offset:2px}button:disabled{opacity:.45;cursor:default}.project-info summary{border:0;background:transparent;padding-inline:0}
.filters{display:flex;gap:10px;min-width:0}.filters label{flex:1}.filters select{flex:1;width:0}#browse-filters{grid-column:2/4}.pair-picker{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:6px;min-width:0}.pair-picker select{flex:1;width:0}#swap-pair{font-size:16px;padding-inline:8px}.browse-note{font-size:12px}.reader-open .page-top{visibility:hidden}main{height:calc(100dvh - var(--header-height) - var(--dock-height));min-height:0;padding:8px;display:flex;flex-direction:column;gap:8px;overflow:auto;overscroll-behavior:contain}
.notice{flex:none;border:1px solid var(--accent);padding:8px 12px;border-radius:6px;background:#fff}.range{color:var(--accent);font:700 11px/1 ui-monospace,Consolas,monospace;letter-spacing:.04em;flex:none}
article{position:relative;min-width:0;min-height:0;border:1px solid var(--line);border-radius:6px;background:#fff}.preview{position:relative;flex:1;min-height:0;width:100%;overflow:hidden;background:#e9e9e5;border-radius:5px}.preview iframe{position:absolute;width:1280px;height:800px;border:0;transform:scale(.25);transform-origin:0 0;pointer-events:none;opacity:0;transition:opacity .18s ease}.preview.ready iframe{opacity:1}.preview.loading::after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(100deg,#e9e9e5 20%,#f4f4f1 42%,#e9e9e5 64%);background-size:200% 100%;animation:preview-shimmer 1.2s linear infinite;pointer-events:none}.preview.failed::after{content:"预览加载失败，请用「独立打开」";position:absolute;inset:0;z-index:2;display:grid;place-items:center;padding:24px;text-align:center;color:var(--muted);background:#e9e9e5;font-size:12px}@keyframes preview-shimmer{to{background-position:-200% 0}}
.view-tools{display:flex;align-items:center;gap:6px;flex:none}.piece-tools{position:relative;flex:none}.piece-tools summary{font-size:12px;min-height:28px;line-height:18px;padding:4px 8px}.piece-tools .meta{position:absolute;right:0;top:calc(100% + 6px);z-index:40;width:270px;max-width:calc(100vw - 24px);padding:8px;border:1px solid var(--line);border-radius:8px;background:#fff;box-shadow:0 8px 28px #0002}.meta>div:not(.actions),.meta>h2,.meta>p{display:none}.actions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}.actions>*{min-height:36px;font-size:12px}.empty{padding:40px 16px;text-align:center;color:var(--muted)}
.current-submission{min-width:0;max-width:38%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--muted);font-size:11px}.meta>.piece-owner{display:block;margin:8px 0 0;padding-top:8px;border-top:1px solid var(--line);overflow-wrap:anywhere;color:var(--muted);font-size:11px}
.compare-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:minmax(0,1fr);gap:8px;flex:1;min-height:0}.compare-card{display:flex;flex-direction:column;min-height:0}.compare-card .preview iframe{pointer-events:auto}.compare-card .identity{display:flex;align-items:center;gap:6px;flex:none;height:36px;padding:3px 6px;border-bottom:1px solid var(--line);font-size:12px;color:var(--muted)}.identity-name{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.missing{flex:1;min-height:120px;display:grid;place-items:center;padding:24px;text-align:center;color:var(--muted)}.single-card{flex:1;min-height:0}.expand-view{font-size:12px;min-height:28px;line-height:18px;padding:4px 8px}
.question-pager{display:flex;align-items:center;gap:6px}.question-pager button{font-size:12px;white-space:nowrap}.question-pager span{min-width:52px;text-align:center;color:var(--muted);font:11px/1.4 ui-monospace,Consolas,monospace}.leave-fullscreen{display:none;position:absolute;right:8px;top:8px;z-index:45}.compare-card:fullscreen{width:100%;height:100%;border:0;border-radius:0;padding:0;background:var(--paper)}.compare-card:fullscreen>.leave-fullscreen{display:inline-flex}.compare-card:fullscreen .identity{display:none}
body.reader-open{overflow:hidden}.reader-overlay{position:fixed;inset:0;z-index:50;display:grid;grid-template-rows:minmax(0,1fr);justify-items:end;overflow:hidden;background:#201d18b8;backdrop-filter:blur(3px)}.reader-panel{width:min(760px,calc(100% - 24px));height:100dvh;min-height:0;overflow:hidden;display:grid;grid-template-rows:auto auto minmax(0,1fr) auto;background:#fffdf7;border-left:1px solid var(--line);box-shadow:-20px 0 60px #0003}.reader-head{display:flex;justify-content:space-between;align-items:start;gap:18px;padding:24px 26px 18px;border-bottom:1px solid var(--line)}.reader-head h2{margin:4px 0 0;font-size:24px}.reader-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.reader-kind{color:var(--accent);font:700 12px/1.2 ui-monospace,Consolas,monospace;letter-spacing:.08em}.reader-note{margin:0;padding:14px 26px;color:var(--muted);background:#f4efe3;border-bottom:1px solid var(--line)}.reader-content{min-height:0;margin:0;padding:24px 26px 60px;overflow-y:scroll;overflow-x:auto;scrollbar-gutter:stable;overscroll-behavior:contain;touch-action:pan-y;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.72 ui-monospace,Consolas,"Microsoft YaHei",monospace;scrollbar-width:auto;scrollbar-color:var(--accent) #e7dfd1}.reader-content::-webkit-scrollbar{width:13px;height:13px}.reader-content::-webkit-scrollbar-track{background:#e7dfd1}.reader-content::-webkit-scrollbar-thumb{background:var(--accent);border:3px solid #e7dfd1;border-radius:999px}.reader-content:focus-visible{outline:3px solid #a12a2f66;outline-offset:-3px}.reader-foot{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 18px;border-top:1px solid var(--line);background:#f4efe3}.reader-progress{color:var(--muted);font:700 12px/1.2 ui-monospace,Consolas,monospace}.reader-close{flex:none;background:var(--ink);color:#fff;border-color:var(--ink)}
@media(max-width:1000px){:root{--dock-height:95px}.toolbar{grid-template-columns:auto minmax(140px,1fr) auto;gap:6px 10px}.dock-actions{grid-column:3;grid-row:1}#browse-filters{grid-column:2}.pair-picker{grid-column:1/-1;grid-row:2}}
@media(max-width:720px){:root{--dock-height:145px;--header-height:53px}.project-header{gap:6px;padding:6px 8px}.project-info summary{font-size:0;width:24px}.project-info summary::after{content:'D';font-size:18px}.workspace-heading{gap:4px}.workspace-heading h1{font-size:13px}.workspace-heading .expand-view{display:none}.workspace-heading .piece-tools summary{padding-inline:5px}.question-pager{gap:4px}.question-pager button{font-size:0;padding:8px;min-width:32px}.question-pager button::after{font-size:16px}#previous-question::after{content:'←'}#next-question::after{content:'→'}.question-pager span{min-width:40px;font-size:10px}main{padding:6px;gap:6px}.compare-grid{display:flex;flex-direction:column;min-height:566px;gap:6px}.compare-card{flex:1;min-height:280px}.single-card{min-height:260px}.toolbar{grid-template-columns:minmax(0,1fr) auto;padding:6px 8px max(6px,env(safe-area-inset-bottom));gap:6px}.mode-switch{gap:0}.mode-switch button{flex:1;padding-inline:6px;font-size:10px}.dock-actions{grid-column:2;gap:4px}.dock-actions button{font-size:10px;padding-inline:7px}.dock-actions .export{max-width:110px;white-space:normal;line-height:16px}.page-top{font-size:0!important;min-width:30px}.page-top::after{content:'↑';font-size:16px}#browse-filters,#prototype-picker{grid-column:1/-1;grid-row:2}.pair-picker{grid-column:1/-1;grid-row:3;gap:6px}.toolbar select{font-size:16px}.filters{gap:8px}.reader-panel{width:100%;height:100dvh}.reader-head{padding:18px;align-items:stretch;flex-direction:column}.reader-head h2{font-size:20px;overflow-wrap:anywhere}.reader-actions{justify-content:flex-start}.reader-note,.reader-content{padding-left:18px;padding-right:18px}.reader-foot{padding-bottom:max(10px,env(safe-area-inset-bottom))}}
@media(max-width:720px){.workspace-heading .piece-tools .meta{position:fixed;top:calc(var(--header-height) + 4px);left:8px;right:8px;width:auto;max-width:none}}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;animation:none!important;transition:none!important}}
"""


GALLERY_JS = r"""
const DATA=window.DAEDALUS_DATA;
const app=document.querySelector("main");
const answerSelect=document.querySelector("#answer-filter");
const prototypeSelect=document.querySelector("#prototype-filter");
const answerPicker=document.querySelector("#answer-picker");
const prototypePicker=document.querySelector("#prototype-picker");
const categorySelect=document.querySelector("#category-filter");
const browseFilters=document.querySelector("#browse-filters");
const pairPicker=document.querySelector("#pair-picker");
const leftSelect=document.querySelector("#compare-left");
const rightSelect=document.querySelector("#compare-right");
const swapButton=document.querySelector("#swap-pair");
const browseNote=document.querySelector("#browse-note");
const pageTop=document.querySelector("#page-top");
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
const controlDock=document.querySelector(".toolbar");
const workspaceHeading=document.querySelector("#workspace-heading");
const questionPager=document.querySelector("#question-pager");
const previousQuestion=document.querySelector("#previous-question");
const nextQuestion=document.querySelector("#next-question");
const questionProgress=document.querySelector("#question-progress");
let mode="browse";
let browseIndex=0;
let readerOpener=null;
let readerToken=0;
const textCache=new Map();
const jsonCache=new Map();
const prefetchedDocs=new Set();
async function loadText(url){if(!textCache.has(url))textCache.set(url,fetch(url).then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.text()}).catch(error=>{textCache.delete(url);throw error}));return textCache.get(url)}
async function loadJson(url){if(!jsonCache.has(url))jsonCache.set(url,fetch(url).then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.json()}).catch(error=>{jsonCache.delete(url);throw error}));return jsonCache.get(url)}
function prefetchDocument(url){if(!url||prefetchedDocs.has(url))return;prefetchedDocs.add(url);const frame=node("iframe");frame.setAttribute("sandbox","allow-scripts");frame.setAttribute("aria-hidden","true");frame.tabIndex=-1;frame.style.cssText="position:fixed;left:-10000px;top:0;width:320px;height:200px;pointer-events:none";const clean=()=>frame.remove();frame.addEventListener("load",()=>{frame.addEventListener("load",()=>setTimeout(clean,0),{once:true});frame.src=url},{once:true});frame.addEventListener("error",()=>{prefetchedDocs.delete(url);clean()},{once:true});document.body.append(frame);frame.src="about:blank";setTimeout(clean,8000)}
function prefetchReader(piece){if(!piece)return;loadText(piece.specUrl).catch(()=>{});loadText(piece.intentUrl).catch(()=>{})}
const whenIdle=window.requestIdleCallback?fn=>window.requestIdleCallback(fn,{timeout:1500}):fn=>setTimeout(fn,200);
function renderReaderText(text){readerContent.textContent=text;readerContent.scrollTop=0;updateReaderProgress()}
const dockSizer=new ResizeObserver(()=>{document.documentElement.style.setProperty("--dock-height",`${controlDock.getBoundingClientRect().height}px`);document.documentElement.style.setProperty("--header-height",`${pageHeader.getBoundingClientRect().height}px`)});
dockSizer.observe(controlDock);dockSizer.observe(pageHeader);
const previewSizer=new ResizeObserver(entries=>{for(const entry of entries){const scale=Math.min(entry.contentRect.width/1280,entry.contentRect.height/800),frame=entry.target.firstElementChild;frame.style.transform=`scale(${scale})`;frame.style.left=`${(entry.contentRect.width-1280*scale)/2}px`;frame.style.top=`${(entry.contentRect.height-800*scale)/2}px`}});
function node(name,text,cls){const n=document.createElement(name);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n}
function escapeHtml(value){return String(value).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\"/g,"&quot;")}
function chosenRows(){const chosen=answerSelect?answerSelect.value:"";return chosen?DATA.submissions.filter(item=>item.key===chosen):DATA.submissions}
function compareRows(){return [leftSelect.value,rightSelect.value].filter((key,index,keys)=>key&&keys.indexOf(key)===index).map(key=>DATA.submissions.find(item=>item.key===key)).filter(Boolean)}
function syncPair(changed=leftSelect){if(leftSelect.value&&leftSelect.value===rightSelect.value){const other=changed===leftSelect?rightSelect:leftSelect;other.value=DATA.submissions.find(item=>item.key!==changed.value)?.key||""}for(const option of leftSelect.options)option.disabled=!!rightSelect.value&&option.value===rightSelect.value;for(const option of rightSelect.options)option.disabled=!!leftSelect.value&&option.value===leftSelect.value;leftSelect.disabled=!DATA.submissions.length;rightSelect.disabled=DATA.submissions.length<2;swapButton.disabled=DATA.submissions.length<2}
function browsePieces(sub){return sub.pieces.filter(piece=>!categorySelect.value||piece.category===categorySelect.value)}
function browseEntries(){return chosenRows().flatMap(sub=>browsePieces(sub).sort((a,b)=>a.id.localeCompare(b.id)).map(piece=>({sub,piece})))}
function forfeitNotice(sub){return node("div",`${sub.displayName} · 我是鸡 — ${sub.forfeitReason} · 已完成 ${sub.pieces.length} / 50 题`,"notice")}
function updateQuestionNavigation(index,total){previousQuestion.disabled=index<=0||!total;nextQuestion.disabled=index>=total-1||!total;questionProgress.textContent=total?`${index+1} / ${total}`:"0 / 0";questionPager.hidden=false}
function stepQuestion(offset){if(mode==="compare"){const index=DATA.prototypeTasks.findIndex(task=>task.id===prototypeSelect.value),task=DATA.prototypeTasks[index+offset];if(!task)return;prototypeSelect.value=task.id}else{const index=browseIndex+offset;if(index<0||index>=browseEntries().length)return;browseIndex=index}render();window.scrollTo({top:0,behavior:"auto"});const button=offset>0?nextQuestion:previousQuestion;(button.disabled?(offset>0?previousQuestion:nextQuestion):button).focus({preventScroll:true})}
function updateReaderProgress(){const maximum=readerContent.scrollHeight-readerContent.clientHeight;const percent=maximum<=0?100:Math.round(readerContent.scrollTop/maximum*100);readerProgress.textContent=`阅读进度 ${percent}%`;readerProgress.setAttribute("aria-valuenow",String(percent))}
function scrollReaderByKeyboard(event){let top=null;const page=Math.max(80,Math.round(readerContent.clientHeight*.82));if(event.key==="PageDown")top=readerContent.scrollTop+page;else if(event.key==="PageUp")top=readerContent.scrollTop-page;else if(event.key==="ArrowDown")top=readerContent.scrollTop+48;else if(event.key==="ArrowUp")top=readerContent.scrollTop-48;else if(event.key==="Home")top=0;else if(event.key==="End")top=readerContent.scrollHeight;if(top===null)return;event.preventDefault();readerContent.scrollTo({top,behavior:"auto"})}
async function showReader(piece,kind,opener){const token=++readerToken;const normative=kind==="spec",menu=opener.closest?.("details");readerOpener=menu?menu.querySelector("summary"):opener;if(menu)menu.open=false;readerKind.textContent=normative?"复现规范 · 规范性":"设计意图 · 非规范性";readerTitle.textContent=`${piece.id} ${piece.title}`;readerNote.textContent=normative?"用于复现和验收：布局、令牌、组件状态、响应式与核心流程。":"用于理解取舍：适用场景、非目标与辅助复刻提示词；不替代正式规范。";readerExport.textContent=normative?"导出此规范":"导出此意图";readerExport.href=normative?piece.specUrl:piece.intentUrl;readerExport.download=`${piece.id}-${piece.slug}.${normative?"spec.md":"intent.md"}`;readerContent.setAttribute("aria-label",`${piece.id} ${piece.title} ${normative?"复现规范正文":"设计意图正文"}`);readerOverlay.hidden=false;document.body.classList.add("reader-open");pageHeader.inert=true;controlDock.inert=true;app.inert=true;pageTop.inert=true;readerContent.focus();const inline=normative?piece.spec:piece.intent;if(inline!==undefined){renderReaderText(inline);return}renderReaderText("载入中…");try{const text=await loadText(normative?piece.specUrl:piece.intentUrl);if(token===readerToken)renderReaderText(text)}catch(error){if(token===readerToken)renderReaderText("规范载入失败：请用右上角“导出此规范”直接下载，或关闭后重试。")}}
function closeReader(){if(readerOverlay.hidden)return;readerToken++;readerOverlay.hidden=true;document.body.classList.remove("reader-open");pageHeader.inert=false;controlDock.inert=false;app.inert=false;pageTop.inert=false;const opener=readerOpener;readerOpener=null;opener?.focus()}
function startPreview(card){const frame=card.__frame;if(!frame||frame.src)return;if(card.__src)frame.src=card.__src}
function cardFor(piece,compare=false){const card=node("article",undefined,compare?"compare-card":"");const preview=node("div",undefined,"preview loading");preview.setAttribute("aria-busy","true");const frame=node("iframe");frame.setAttribute("sandbox","allow-scripts");frame.loading=compare?"eager":"lazy";frame.tabIndex=compare?0:-1;frame.title=`${piece.id} ${piece.title}`;frame.addEventListener("load",()=>{preview.classList.remove("loading");preview.classList.add("ready");preview.removeAttribute("aria-busy")});frame.addEventListener("error",()=>{preview.classList.remove("loading");preview.classList.add("failed");preview.removeAttribute("aria-busy")});preview.append(frame);previewSizer.observe(preview);card.append(preview);const meta=node("div",undefined,"meta");meta.append(node("div",piece.id),node("h2",piece.title),node("p",piece.scene));const actions=node("div",undefined,"actions");const open=node("a","独立打开","open");open.href=piece.url;open.target="_blank";open.rel="noopener noreferrer";actions.append(open);const spec=node("button","查看规范");spec.type="button";spec.onclick=()=>showReader(piece,"spec",spec);actions.append(spec);const intent=node("button","设计意图");intent.type="button";intent.onclick=()=>showReader(piece,"intent",intent);actions.append(intent);const archive=node("a","导出方案","open");archive.href=piece.archiveUrl;archive.download=`${piece.id}-${piece.slug}-方案档案.html`;actions.append(archive);meta.append(actions);card.append(meta);card.__frame=frame;card.__src=piece.url;return card}
function viewTools(card,meta){const tools=node("div",undefined,"view-tools"),menu=node("details",undefined,"piece-tools"),summary=node("summary","资料 ▾"),expand=node("button","放大","expand-view"),exit=node("button","退出全屏 · Esc","leave-fullscreen");menu.append(summary,meta);expand.type=exit.type="button";expand.hidden=typeof card.requestFullscreen!=="function";expand.setAttribute("aria-label","全屏放大当前作品");expand.onclick=()=>card.requestFullscreen().catch(()=>{expand.textContent="全屏未获允许"});exit.onclick=()=>document.exitFullscreen();card.append(exit);tools.append(expand,menu);return tools}
function renderBrowse(){
  const entries=browseEntries();
  browseIndex=Math.min(browseIndex,Math.max(0,entries.length-1));
  updateQuestionNavigation(browseIndex,entries.length);
  if(!entries.length){workspaceHeading.append(node("h1","逐题浏览"));for(const sub of chosenRows())if(sub.status==="forfeited")app.append(forfeitNotice(sub));app.append(node("div",chosenRows().length?"当前分区暂无作品，可切换答卷或分区查看。":"还没有符合新版规则的答卷。","empty"));return}
  const {sub,piece}=entries[browseIndex],title=node("div",undefined,"compare-title"),identity=`${sub.harness} / ${sub.model} / ${sub.reasoningEffort}`,owner=node("span",sub.displayName,"current-submission");
  owner.title=`${sub.displayName} · ${identity}`;title.title=piece.scene;title.append(node("span",piece.id,"range"),node("h1",piece.title),owner);workspaceHeading.append(title);
  for(const missing of chosenRows())if(missing.status==="forfeited"&&!browsePieces(missing).length)app.append(forfeitNotice(missing));
  if(sub.status==="forfeited")app.append(forfeitNotice(sub));
  const card=cardFor(piece,true),meta=card.children[1];card.className="compare-card single-card";meta.append(node("p",`${sub.displayName} · ${identity}`,"piece-owner"));workspaceHeading.append(viewTools(card,meta));app.append(card);
  startPreview(card);
  whenIdle(()=>{prefetchDocument(entries[browseIndex+1]?.piece.url);prefetchDocument(entries[browseIndex-1]?.piece.url);prefetchReader(piece)});
}
function renderCompare(){
  const taskId=prototypeSelect?.value||DATA.prototypeTasks[0]?.id;
  if(!taskId){updateQuestionNavigation(0,0);workspaceHeading.append(node("h1","原型对比"));app.append(node("div","题库里没有可对比的产品原型题。","empty"));return}
  const task=DATA.prototypeTasks.find(item=>item.id===taskId),rows=compareRows();
  const title=node("div",undefined,"compare-title");
  updateQuestionNavigation(DATA.prototypeTasks.findIndex(item=>item.id===taskId),DATA.prototypeTasks.length);
  title.title=task.scene;title.append(node("span",task.id,"range"),node("h1",task.title));workspaceHeading.append(title);
  const grid=node("div",undefined,"compare-grid"),cards=[];
  for(const [index,sub] of rows.entries()){
    const piece=sub.pieces.find(item=>item.id===taskId),card=node("article",undefined,"compare-card");
    const identity=node("div",undefined,"identity"),name=node("span",`${index===0?"A":"B"} · ${sub.displayName}`,"identity-name");name.title=sub.displayName;identity.append(name);card.append(identity);
    if(piece){const rendered=cardFor(piece,true),preview=rendered.children[0],meta=rendered.children[1];card.__frame=rendered.__frame;card.__src=rendered.__src;card.append(preview);identity.append(viewTools(card,meta))}
    else{const reason=sub.status==="forfeited"?`已弃权：${sub.forfeitReason}`:"尚未提交这一题";card.append(node("div",reason,"missing"))}
    grid.append(card);cards.push(card);
  }
  app.append(grid);
  for(const card of cards)startPreview(card);
  for(const sub of rows){const piece=sub.pieces.find(item=>item.id===taskId);if(piece)whenIdle(()=>prefetchReader(piece))}
  if(rows.length<2)app.append(node("p",rows.length?"当前只有一份登记答卷，至少两份才能进行 Battle 对比。":"暂无登记答卷，至少两份才能进行 Battle 对比。","notice"));
}
function handbook(title,entries){const sections=entries.map(entry=>`<section><h2>${escapeHtml(entry.heading)}</h2><pre>${escapeHtml(entry.spec)}</pre></section>`).join("\n");return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escapeHtml(title)}</title><style>body{margin:0;background:#f4efe3;color:#201d18;font:15px/1.6 system-ui,"Microsoft YaHei",sans-serif}main{width:min(900px,calc(100% - 32px));margin:auto;padding:40px 0 80px}h1{font-size:32px}p{color:#736b5f}section{background:#fff;border:1px solid #d9d0c0;border-radius:14px;padding:20px;margin:14px 0}h2{font-size:18px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.65 ui-monospace,Consolas,monospace}</style></head><body><main><h1>${escapeHtml(title)}</h1><p>由 Daedalus 展厅一键导出，可离线阅读。</p>${sections}</main></body></html>`}
function download(filename,text,mime){const blob=new Blob([text],{type:`${mime};charset=utf-8`});const url=URL.createObjectURL(blob);const link=node("a");link.href=url;link.download=filename;document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),2000)}
async function exportSpecs(){let entries=[];let rows=[];let title="";let filename="";if(mode==="compare"){const taskId=prototypeSelect.value;const task=DATA.prototypeTasks.find(item=>item.id===taskId);rows=compareRows();for(const sub of rows){const piece=sub.pieces.find(item=>item.id===taskId);if(piece)entries.push({sub,piece,heading:`${taskId} ${piece.title} · ${sub.displayName}`})}title=`${taskId} ${task?.title||"产品原型"} · 同题规范对比`;filename=`Daedalus-${taskId}-同题规范对比.html`}else{rows=chosenRows();for(const sub of rows){for(const piece of browsePieces(sub))entries.push({sub,piece,heading:`${piece.id} ${piece.title}${rows.length>1?` · ${sub.displayName}`:""}`})}const scope=DATA.categories.find(item=>item.id===categorySelect.value)?.label||"50 题";title=rows.length===1?`${rows[0].displayName} · ${scope}制作规范`:`Daedalus · 全部答卷 · ${scope}制作规范`;filename=`Daedalus-${rows.length===1?rows[0].key:"全部答卷"}-${categorySelect.value||"50题"}规范.html`}if(!entries.length){const old=exportButton.textContent;exportButton.textContent="没有可导出的规范";setTimeout(()=>exportButton.textContent=old,1600);return}const allInline=entries.every(entry=>entry.piece.spec!==undefined);if(allInline){download(filename,handbook(title,entries.map(entry=>({heading:entry.heading,spec:entry.piece.spec}))),"text/html");return}const previous=exportButton.textContent;exportButton.disabled=true;exportButton.textContent="正在整理规范…";try{const bundles=new Map();const keys=[...new Set(rows.map(row=>row.key))];await Promise.all(keys.map(async key=>{const row=rows.find(item=>item.key===key);try{bundles.set(key,row.bundleUrl?await loadJson(row.bundleUrl):{})}catch(error){bundles.set(key,{})}}));const sections=await Promise.all(entries.map(async entry=>{let spec=entry.piece.spec??bundles.get(entry.sub.key)?.[entry.piece.id];if(spec===undefined)spec=await loadText(entry.piece.specUrl);return{heading:entry.heading,spec}}));download(filename,handbook(title,sections),"text/html")}catch(error){exportButton.textContent="导出失败，请重试";setTimeout(()=>{exportButton.textContent=previous},1600);return}finally{exportButton.disabled=false}exportButton.textContent=previous}
function render(){previewSizer.disconnect();app.replaceChildren();app.scrollTop=0;workspaceHeading.replaceChildren();if(mode==="compare")renderCompare();else renderBrowse();exportButton.textContent=mode==="compare"?"导出本题对比规范":categorySelect.value?"导出当前分区规范":"一键导出规范";browseNote.hidden=mode!=="browse";browseNote.textContent=`共 ${DATA.submissions.length} 份答卷 · 当前范围 ${chosenRows().length} 份答卷、${browseEntries().length} 件作品 · 每次展示一题，可直接操作。`}
function setMode(next){mode=next;browseButton.setAttribute("aria-pressed",String(next==="browse"));compareButton.setAttribute("aria-pressed",String(next==="compare"));browseFilters.hidden=next!=="browse";prototypePicker.hidden=next!=="compare";pairPicker.hidden=next!=="compare";render()}
if(answerSelect&&!answerPicker.hidden&&DATA.submissions.length)answerSelect.value=DATA.submissions[0].key;
leftSelect.value=DATA.submissions[0]?.key||"";rightSelect.value=DATA.submissions[1]?.key||"";syncPair();
for(const select of [answerSelect,categorySelect])select?.addEventListener("change",()=>{browseIndex=0;render();window.scrollTo({top:0,behavior:"auto"})});prototypeSelect.addEventListener("change",render);
previousQuestion.addEventListener("click",()=>stepQuestion(-1));nextQuestion.addEventListener("click",()=>stepQuestion(1));
for(const select of [leftSelect,rightSelect])select.addEventListener("change",()=>{syncPair(select);render()});
swapButton.addEventListener("click",()=>{[leftSelect.value,rightSelect.value]=[rightSelect.value,leftSelect.value];syncPair();render()});
pageTop.addEventListener("click",()=>{window.scrollTo({top:0,behavior:"auto"});app.scrollTo({top:0,behavior:"auto"});browseButton.focus({preventScroll:true})});
document.addEventListener("click",event=>{for(const menu of document.querySelectorAll("details[open]"))if(!menu.contains(event.target))menu.open=false});
document.addEventListener("keydown",event=>{if(event.key==="Escape"&&readerOverlay.hidden)for(const menu of document.querySelectorAll("details[open]")){menu.open=false;menu.querySelector("summary").focus()}});
browseButton.addEventListener("click",()=>setMode("browse"));compareButton.addEventListener("click",()=>setMode("compare"));exportButton.addEventListener("click",exportSpecs);readerTop.addEventListener("click",()=>readerContent.scrollTo({top:0,behavior:"auto"}));readerContent.addEventListener("scroll",updateReaderProgress,{passive:true});readerPanel.addEventListener("keydown",scrollReaderByKeyboard);readerClose.addEventListener("click",closeReader);readerOverlay.addEventListener("click",event=>{if(event.target===readerOverlay)closeReader()});document.addEventListener("keydown",event=>{if(event.key==="Escape")closeReader()});render();
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
    category_options = "".join(
        f'<option value="{html.escape(item["id"], quote=True)}">{html.escape(item["label"])} · {item["range"][0]}–{item["range"][1]}</option>'
        for item in payload["categories"]
    )
    left_options = options or '<option value="">暂无答卷</option>'
    right_options = options if len(payload["submissions"]) > 1 else '<option value="">暂无其他答卷</option>'
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Daedalus · Product UI Model Gallery</title>{FAVICON_LINK}<style>{GALLERY_CSS}</style></head><body>
<header class="project-header"><details class="project-info"><summary aria-label="Daedalus 项目介绍">Daedalus</summary><div class="project-description"><strong>50 道产品 UI 题的公开答卷展厅</strong><p>同一道题，看见不同的产品品味。001–040 页面设计，041–050 连续产品原型。</p><p id="browse-note" class="browse-note" role="status"></p></div></details><div id="workspace-heading" class="workspace-heading"></div><nav id="question-pager" class="question-pager" aria-label="逐题浏览" hidden><button id="previous-question" type="button">← 上一题</button><span id="question-progress" role="status" aria-live="polite"></span><button id="next-question" type="button">下一题 →</button></nav></header><main></main>
<footer class="toolbar" aria-label="展厅选择与操作">
<div class="mode-switch" role="group" aria-label="展厅模式"><button id="browse-mode" type="button" aria-pressed="true">逐题浏览</button><button id="compare-mode" type="button" aria-pressed="false">对比 041–050</button></div>
<div id="browse-filters" class="filters">{chooser}<label>分区 <select id="category-filter"><option value="">全部分区</option>{category_options}</select></label></div>
<div id="prototype-picker" class="filters" hidden><label>题目 <select id="prototype-filter">{prototype_options}</select></label></div>
<div id="pair-picker" class="pair-picker" role="group" aria-label="选择 Battle 双方" hidden><label>A <select id="compare-left">{left_options}</select></label><button id="swap-pair" type="button" aria-label="交换双方">⇄</button><label>B <select id="compare-right">{right_options}</select></label></div>
<div class="dock-actions"><button id="export-specs" class="export" type="button">一键导出规范</button><button id="page-top" class="page-top" type="button" aria-label="返回页面顶部">↑ 顶部</button></div></footer>
<div id="reader-overlay" class="reader-overlay" hidden><section class="reader-panel" role="dialog" aria-modal="true" aria-labelledby="reader-title" aria-describedby="reader-note"><div class="reader-head"><div><div id="reader-kind" class="reader-kind"></div><h2 id="reader-title"></h2></div><div class="reader-actions"><a id="reader-export" class="open" href="#" download>导出此规范</a><button id="reader-close" class="reader-close" type="button">关闭</button></div></div><p id="reader-note" class="reader-note"></p><pre id="reader-content" class="reader-content" tabindex="0"></pre><div class="reader-foot"><span id="reader-progress" class="reader-progress" role="progressbar" aria-label="阅读进度" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">阅读进度 0%</span><button id="reader-top" type="button">回到顶部</button></div></section></div><script>window.DAEDALUS_DATA={_json_for_script(payload)};</script><script>{GALLERY_JS}</script></body></html>"""


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


def _build_payload(validation: Validation, site: Path) -> tuple[dict[str, Any], dict[str, dict[str, dict[str, str]]]]:
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
    texts: dict[str, dict[str, dict[str, str]]] = {}
    exports_dir = site / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    for item in validation.submissions:
        entry, manifest, folder = item["entry"], item["manifest"], item["folder"]
        key = "--".join((entry["harness"], entry["model"], entry["reasoningEffort"]))
        answer_dir = site / "answers" / key
        answer_dir.mkdir(parents=True, exist_ok=True)
        pieces = []
        piece_texts: dict[str, dict[str, str]] = {}
        specs: dict[str, str] = {}
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
            specs[piece["id"]] = spec_text
            piece_texts[piece["id"]] = {"spec": spec_text, "intent": intent_text}
            pieces.append(
                {
                    "id": piece["id"],
                    "slug": piece["slug"],
                    "title": piece.get("title") or brief["title"],
                    "scene": brief["scene"],
                    "category": brief["category"],
                    "url": f"answers/{key}/{target_name}",
                    "specUrl": f"answers/{key}/{target_spec_name}",
                    "intentUrl": f"answers/{key}/{target_intent_name}",
                    "archiveUrl": f"answers/{key}/{target_archive_name}",
                }
            )
        (exports_dir / f"{key}-specs.json").write_text(
            json.dumps(specs, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        texts[key] = piece_texts
        rows.append(
            {
                "key": key,
                "harness": entry["harness"],
                "model": entry["model"],
                "reasoningEffort": entry["reasoningEffort"],
                "displayName": entry.get("displayName") or manifest.get("displayName") or key,
                "status": manifest["status"],
                "forfeitReason": (manifest.get("forfeit") or {}).get("reason", ""),
                "bundleUrl": f"exports/{key}-specs.json",
                "pieces": pieces,
            }
        )
    prototype_tasks = [
        {"id": brief["id"], "title": brief["title"], "scene": brief["scene"]}
        for brief in briefs
        if brief["id"] in PROTOTYPE_IDS
    ]
    return {"schemaVersion": 1, "catalogCount": 50, "categories": categories, "prototypeTasks": prototype_tasks, "submissions": rows}, texts


def _payload_with_texts(payload: dict[str, Any], texts: dict[str, dict[str, dict[str, str]]]) -> dict[str, Any]:
    full = json.loads(json.dumps(payload, ensure_ascii=False))
    for submission in full["submissions"]:
        for piece in submission["pieces"]:
            body = texts[submission["key"]][piece["id"]]
            piece["spec"] = body["spec"]
            piece["intent"] = body["intent"]
    return full


def _zip_tree(
    source: Path,
    destination: Path,
    *,
    prefix: str = "",
    overrides: dict[str, bytes] | None = None,
) -> None:
    overrides = overrides or {}
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file() and item != destination):
            relative = path.relative_to(source).as_posix()
            name = PurePosixPath(prefix, relative).as_posix()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            body = overrides.get(relative)
            archive.writestr(info, body if body is not None else path.read_bytes())


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
        payload, texts = _build_payload(validation, site)
        (site / "index.html").write_text(_gallery_document(payload), encoding="utf-8")
        overrides: dict[str, bytes] = {}
        for submission in payload["submissions"]:
            solo_dir = site / "submissions" / submission["key"]
            solo_dir.mkdir(parents=True)
            solo_submission = dict(submission)
            solo_submission["bundleUrl"] = "../../" + submission["bundleUrl"]
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
            overrides[f"submissions/{submission['key']}/index.html"] = _gallery_document(
                _payload_with_texts(solo_payload, texts), locked=True
            ).encode("utf-8")
        overrides["index.html"] = _gallery_document(_payload_with_texts(payload, texts)).encode("utf-8")
        _zip_tree(
            site,
            stage / "daedalus-offline-gallery.zip",
            prefix="daedalus-gallery",
            overrides=overrides,
        )
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
