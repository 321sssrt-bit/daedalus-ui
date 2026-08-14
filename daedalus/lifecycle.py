"""One public lifecycle seam for validating and packaging Daedalus.

The module deliberately uses only Python's standard library.  Callers should use
``python -m daedalus`` rather than importing its private helpers.
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
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
    "一句话气质",
    "适合用在哪种产品",
    "色板",
    "字体和字号",
    "间距、圆角、阴影",
    "按钮 / 输入框 / 卡片",
    "动效",
    "不要做什么",
    "复刻提示词",
)
PROTOTYPE_SPEC_HEADINGS = (
    "产品定位与目标用户",
    "核心任务",
    "页面或状态地图",
    "正常流程",
    "异常触发与恢复",
    "数据变化",
    "主设备与响应式规则",
    "人工验收步骤",
)


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


def _validate_spec(result: Validation, path: Path, task_id: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError) as exc:
        result.error("invalid-spec-file", path, f"规范缺失或不是 UTF-8：{exc}")
        return
    required = VISUAL_SPEC_HEADINGS + (PROTOTYPE_SPEC_HEADINGS if task_id in PROTOTYPE_IDS else ())
    missing = [heading for heading in required if not re.search(rf"(?m)^##\s+.*{re.escape(heading)}\s*$", text)]
    if missing:
        result.error("spec-headings", path, "规范缺少章节：" + "、".join(missing))


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
    if manifest.get("schemaVersion") != 3:
        result.error("manifest-version", manifest_path, "model.json 必须使用 schemaVersion 3")
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
            if piece.get("file") != expected_html or piece.get("spec") != expected_spec:
                result.error("piece-filename", manifest_path, f"题目 {task_id} 文件名必须由题号和 slug 唯一确定")
        if isinstance(piece.get("file"), str):
            declared_files.append(piece["file"])
        if isinstance(piece.get("spec"), str):
            declared_files.append(piece["spec"])
        html_path = _declared_path(result, folder, piece.get("file"), ".html", f"题目 {task_id} file")
        spec_path = _declared_path(result, folder, piece.get("spec"), ".md", f"题目 {task_id} spec")
        if html_path is not None:
            _validate_html(result, html_path)
        if spec_path is not None and isinstance(task_id, str):
            _validate_spec(result, spec_path, task_id)
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
header,main{width:min(1440px,100%);margin:auto;padding:24px}h1{margin:.15em 0}.kicker{color:var(--accent);letter-spacing:.16em;text-transform:uppercase}
.identity,.toolbar{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.identity{color:var(--muted)}button,select,a.open{font:inherit;border:1px solid var(--line);border-radius:999px;padding:6px 12px;background:#fff;color:inherit;text-decoration:none;cursor:pointer}
.notice{border:2px solid var(--accent);padding:12px 16px;border-radius:12px;margin:14px 0;background:#fff}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-top:18px}
article{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}.preview{height:230px;background:#e5ddce}.preview iframe{width:1280px;height:800px;border:0;transform:scale(.25);transform-origin:0 0;pointer-events:none}
.meta{padding:12px}.meta h2{margin:3px 0;font-size:17px}.meta p{margin:5px 0;color:var(--muted)}.actions{display:flex;gap:7px;margin-top:10px}.empty{padding:60px 20px;text-align:center;color:var(--muted)}
@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;animation:none!important;transition:none!important}}
"""


GALLERY_JS = r"""
const DATA=window.DAEDALUS_DATA;
const app=document.querySelector("main");
const select=document.querySelector("select");
function node(name,text,cls){const n=document.createElement(name);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n}
function render(){app.replaceChildren();const chosen=select?select.value:"";const rows=chosen?DATA.submissions.filter(x=>x.key===chosen):DATA.submissions;
if(!rows.length){app.append(node("div","还没有符合新版规则的答卷。","empty"));return}
for(const sub of rows){const section=node("section");const ident=node("div",`${sub.harness} / ${sub.model} / ${sub.reasoningEffort}`,"identity");section.append(ident);
if(sub.status==="forfeited"){const f=node("div",`我是鸡 — ${sub.forfeitReason}`,"notice");section.append(f)}
const grid=node("div",undefined,"grid");for(const p of sub.pieces){const card=node("article");const preview=node("div",undefined,"preview");const frame=node("iframe");frame.setAttribute("sandbox","allow-scripts");frame.title=`${p.id} ${p.title}`;frame.srcdoc=p.html;preview.append(frame);card.append(preview);
const meta=node("div",undefined,"meta");meta.append(node("div",p.id),node("h2",p.title),node("p",p.scene));const actions=node("div",undefined,"actions");const open=node("a","独立打开","open");open.href=p.url;open.target="_blank";open.rel="noopener noreferrer";actions.append(open);const spec=node("button","查看规范");spec.onclick=()=>{const blob=new Blob([p.spec],{type:"text/plain;charset=utf-8"});const url=URL.createObjectURL(blob);const link=node("a");link.href=url;link.target="_blank";link.rel="noopener noreferrer";link.click();setTimeout(()=>URL.revokeObjectURL(url),60000)};actions.append(spec);meta.append(actions);card.append(meta);grid.append(card)}section.append(grid);app.append(section)}}
if(select){select.addEventListener("change",render)}render();
"""


def _gallery_document(payload: dict[str, Any], *, locked: bool = False) -> str:
    options = "".join(
        f'<option value="{html.escape(item["key"], quote=True)}">{html.escape(item["displayName"])}</option>'
        for item in payload["submissions"]
    )
    chooser = "" if locked else f'<label>答卷 <select><option value="">全部</option>{options}</select></label>'
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Daedalus · Product UI Model Gallery</title><style>{GALLERY_CSS}</style></head><body><header><div class="kicker">Product UI Model Gallery</div><h1>Daedalus</h1><p>50 道产品 UI 题的公开答卷展厅</p><div class="toolbar">{chooser}</div></header><main></main><script>window.DAEDALUS_DATA={_json_for_script(payload)};</script><script>{GALLERY_JS}</script></body></html>"""


def _build_payload(validation: Validation, site: Path) -> dict[str, Any]:
    catalog_by_id = {item["id"]: item for item in validation.catalog["briefs"]}  # type: ignore[index]
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
            target_name = f'{piece["id"]}-{piece["slug"]}.html'
            shutil.copyfile(source_html, answer_dir / target_name)
            brief = catalog_by_id[piece["id"]]
            pieces.append(
                {
                    "id": piece["id"],
                    "title": piece.get("title") or brief["title"],
                    "scene": brief["scene"],
                    "html": source_html.read_text(encoding="utf-8"),
                    "spec": source_spec.read_text(encoding="utf-8"),
                    "url": f"answers/{key}/{target_name}",
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
    return {"schemaVersion": 1, "catalogCount": 50, "submissions": rows}


def _zip_tree(source: Path, destination: Path, *, prefix: str = "") -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file() and item != destination):
            name = PurePosixPath(prefix, path.relative_to(source).as_posix()).as_posix()
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def _atomic_replace(staged: Path, output: Path) -> None:
    backup = output.with_name(output.name + ".previous")
    if backup.exists():
        shutil.rmtree(backup)
    if output.exists():
        output.replace(backup)
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
    if backup.exists():
        shutil.rmtree(backup)


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
    stage = Path(tempfile.mkdtemp(prefix=".daedalus-build-", dir=output.parent))
    try:
        site = stage / "site"
        site.mkdir()
        payload = _build_payload(validation, site)
        (site / "index.html").write_text(_gallery_document(payload), encoding="utf-8")
        for submission in payload["submissions"]:
            solo_dir = site / "submissions" / submission["key"]
            solo_dir.mkdir(parents=True)
            solo_submission = dict(submission)
            solo_submission["pieces"] = [dict(piece, url="../../" + piece["url"]) for piece in submission["pieces"]]
            solo_payload = {"schemaVersion": 1, "catalogCount": 50, "submissions": [solo_submission]}
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
