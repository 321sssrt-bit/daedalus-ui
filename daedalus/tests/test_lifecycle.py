from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from daedalus.lifecycle import (
    PROTOTYPE_SPEC_HEADINGS,
    PROTOTYPE_VIEWPORTS,
    TASK_IDS,
    VISUAL_SPEC_HEADINGS,
    _atomic_replace,
)


HTML = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--page:#101820;--surface:#1f2933;--text:#f5f7fa;--muted:#9fb3c8;--accent:#3ebd93;--danger:#e66a6a}
body{margin:0;padding:24px;background:#101820;color:#f5f7fa;font:16px/1.5 system-ui}
main{display:grid;gap:16px;max-width:960px;min-height:480px;padding:32px;border:1px solid #9fb3c8;border-radius:12px;background:#1f2933}
button{min-height:44px;padding:10px 16px;border-radius:8px;background:#3ebd93;color:#101820;transition:transform 180ms ease}
button:focus{outline:3px solid #e66a6a}@media(max-width:700px){body{padding:12px}main{padding:20px}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style></head><body><main id="app"><h1>题目</h1><p>测试场景</p><button type="button">完成操作</button></main></body></html>"""


def valid_spec(task_id: str, html_name: str) -> str:
    viewport = "390 × 844 px" if PROTOTYPE_VIEWPORTS.get(task_id) == "mobile" else "1280 × 800 px"
    text = f"""# {task_id} 方案{task_id}

## 规范元数据

- 规范版本：2
- 主视口：{viewport}
- 对应页面：`{html_name}`
- 复现范围：单页核心操作

## 画布与区域布局

| 区域 | 边界与尺寸 | 布局与对齐 | 层级与滚动 |
| --- | --- | --- | --- |
| 页面画布 | 1280 × 800 px，外边距 24px | 块布局 | 固定背景 |
| 主区域 | 最大宽度 960px，最小高度 480px | grid，间距 16px | 正常文档流 |
| 操作区 | 内边距 32px | 纵向排列 | 不滚动 |

## 设计令牌

### 色彩

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--page` | `#101820` | 页面背景 |
| `--surface` | `#1f2933` | 主容器 |
| `--text` | `#f5f7fa` | 正文 |
| `--muted` | `#9fb3c8` | 边框与辅助文字 |
| `--accent` | `#3ebd93` | 主操作 |
| `--danger` | `#e66a6a` | 焦点轮廓 |

### 字体

| 角色 | 字体栈 | 字号 / 行高 | 字重 / 字距 |
| --- | --- | --- | --- |
| 显示字 | system-ui | 32px / 1.2 | 700 / 0 |
| 标题 | system-ui | 24px / 1.3 | 700 / 0 |
| 正文 | system-ui | 16px / 1.5 | 400 / 0 |
| 辅助文字 | system-ui | 14px / 1.5 | 400 / 0 |

### 间距、圆角与层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| 基础间距 | 16px | 栅格 |
| 控件圆角 | 8px | 按钮 |
| 容器圆角 | 12px | 主区域 |
| 边框 / 阴影 | 1px / 无 | 容器边界 |

## 组件规格与状态

| 组件 | 结构与尺寸 | 默认样式 | 状态变化 |
| --- | --- | --- | --- |
| 主按钮 | 最小高度 44px，内边距 10px 16px | 强调色实底 | focus 为 3px 危险色轮廓 |
| 标题 | 32px 单行 | 正文色 | 无交互状态 |
| 主容器 | 最大宽度 960px，圆角 12px | 表面色 | 窄屏内边距降为 20px |

## 响应式规则

| 条件 | 布局变化 | 组件变化 |
| --- | --- | --- |
| 主视口 | 页面外边距 24px | 容器内边距 32px |
| ≤ 700px | 页面外边距 12px | 容器内边距 20px |

## 内容与数据

标题固定为“题目”，正文为“测试场景”，主按钮为“完成操作”；初始状态不产生数据。

## 动效与反馈

| 触发 | 时长与缓动 | 可见反馈 | `prefers-reduced-motion` |
| --- | --- | --- | --- |
| 页面进入 | 0ms | 直接显示 | 不变 |
| 按钮交互 | 180ms ease | transform 过渡 | 关闭 transition |

## 复现验收清单

- [ ] 1280 × 800 px 下主区域最大宽度为 960px。
- [ ] 页面使用六个已登记色值且层级一致。
- [ ] 主按钮最小高度为 44px，键盘焦点可见。
- [ ] 700px 断点下页面和容器内边距按表变化。
- [ ] 减少动态模式关闭 transition 和 animation。
"""
    if task_id in PROTOTYPE_VIEWPORTS:
        text += """
## 产品边界

只实现开始到完成的一次核心操作，不包含账户管理。

## 状态地图

初始态 → 操作成功态；失败开关 → 异常态 → 重试 → 成功态。

## 正常流程

点击“完成操作”，按钮状态更新并显示完成反馈。

## 异常触发与恢复

主动触发失败后保留输入，点击重试恢复并完成。

## 数据变化

成功前记录为 0，成功后为 1；异常时仍为 0。

## 人工验收步骤

先完成正常操作并确认结果；再触发失败、确认保留状态、重试并确认成功。
"""
    return text


def valid_intent(task_id: str, spec_name: str) -> str:
    return f"""# {task_id} 方案{task_id}

## 意图元数据

- 意图版本：1
- 对应规范：`{spec_name}`
- 说明：本文件不参与结构、尺寸、状态或交互验收。

## 设计意图

用清晰的单页结构让测试流程一眼可读。

## 适用场景与目标用户

适合需要快速完成单一任务的普通用户。

## 非目标

不实现账户管理，也不追求装饰性动画。

## 复刻提示词

制作一个深色、克制、单任务导向的自包含页面。
"""


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def windows_acl_is_protected(path: Path) -> bool:
    completed = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            "(Get-Acl -LiteralPath $env:DAEDALUS_OUTPUT).AreAccessRulesProtected",
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "DAEDALUS_OUTPUT": str(path)},
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr)
    return completed.stdout.strip() == "True"


def make_repo(root: Path, *, submission: str | None = None, mismatch: bool = False) -> None:
    categories = [
        {"id": "enter", "label": "进入产品", "range": ["001", "008"]},
        {"id": "work", "label": "工作台", "range": ["009", "016"]},
        {"id": "commerce", "label": "内容与消费", "range": ["017", "024"]},
        {"id": "settings", "label": "设置与表单", "range": ["025", "032"]},
        {"id": "mobile", "label": "移动与状态", "range": ["033", "040"]},
        {"id": "prototype", "label": "连续产品原型", "range": ["041", "050"]},
    ]
    briefs = []
    for task_id in TASK_IDS:
        category = next(item["id"] for item in categories if item["range"][0] <= task_id <= item["range"][1])
        brief = {
            "id": task_id,
            "job": "job-" + task_id,
            "title": "题目" + task_id,
            "category": category,
            "scene": "测试场景",
            "viewport": PROTOTYPE_VIEWPORTS.get(task_id, "desktop"),
            "must_have": ["一个模块"],
        }
        if task_id in PROTOTYPE_VIEWPORTS:
            brief["core_flow"] = ["开始", "完成"]
            brief["exception"] = {"trigger": "失败", "recovery": ["重试"]}
        briefs.append(brief)
    write_json(root / "catalog" / "briefs.json", {"schemaVersion": 3, "count": 50, "categories": categories, "briefs": briefs})
    entries = []
    if submission:
        ident = {"harness": "codex", "model": "gpt-5.6-sol", "reasoningEffort": "xhigh"}
        folder = root / "models" / "codex" / "gpt-5.6-sol" / "xhigh"
        folder.mkdir(parents=True)
        pieces = []
        ids = TASK_IDS if submission == "complete" else TASK_IDS[:3]
        for task_id in ids:
            slug = "scheme-" + task_id
            html_name = f"{task_id}-{slug}.html"
            spec_name = f"{task_id}-{slug}.spec.md"
            intent_name = f"{task_id}-{slug}.intent.md"
            (folder / html_name).write_text(HTML, encoding="utf-8")
            (folder / spec_name).write_text(valid_spec(task_id, html_name), encoding="utf-8")
            (folder / intent_name).write_text(valid_intent(task_id, spec_name), encoding="utf-8")
            pieces.append({"id": task_id, "slug": slug, "title": "方案" + task_id, "file": html_name, "spec": spec_name, "intent": intent_name, "status": "complete"})
        manifest = {"schemaVersion": 4, "specVersion": 2, **ident, "displayName": "Fixture", "status": submission, "pieces": pieces, "runReceipt": "run-receipt.json"}
        if submission == "forfeited":
            manifest["forfeit"] = {"phrase": "我是鸡", "reason": "测试主动弃权"}
        write_json(folder / "model.json", manifest)
        agent_model = "other-model" if mismatch else ident["model"]
        write_json(folder / "run-receipt.json", {"schemaVersion": 1, "mainAgent": {"model": ident["model"], "reasoningEffort": ident["reasoningEffort"]}, "subagents": [{"model": agent_model, "reasoningEffort": "xhigh"}]})
        entries.append({**ident, "displayName": "Fixture", "path": "models/codex/gpt-5.6-sol/xhigh"})
    write_json(root / "models" / "_index.json", {"schemaVersion": 3, "submissions": entries})
    (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
    (root / "README.md").write_text("# Daedalus\n", encoding="utf-8")


class LifecycleTests(unittest.TestCase):
    def run_cli(self, root: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        completed = subprocess.run(
            [sys.executable, "-m", "daedalus", *args, "--root", str(root)],
            cwd=Path(__file__).resolve().parents[2],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return completed, json.loads(completed.stdout)

    def test_empty_v3_registry_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root)
            completed, receipt = self.run_cli(root, "validate")
            self.assertEqual(completed.returncode, 0)
            self.assertTrue(receipt["ok"])
            self.assertEqual(receipt["catalogTasks"], 50)

    def test_complete_submission_validates_and_build_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            gallery = (root / "dist" / "site" / "index.html").read_text(encoding="utf-8")
            solo = (root / "dist" / "site" / "submissions" / "codex--gpt-5.6-sol--xhigh" / "index.html").read_text(encoding="utf-8")
            self.assertIn('setAttribute("sandbox","allow-scripts")', gallery)
            self.assertNotIn("allow-same-origin", gallery)
            self.assertIn("noopener noreferrer", gallery)
            self.assertIn("../../answers/codex--gpt-5.6-sol--xhigh/", solo)
            self.assertTrue((root / "dist" / "daedalus-offline-gallery.zip").is_file())

    @unittest.skipUnless(os.name == "nt", "Windows ACL regression")
    def test_build_output_inherits_parent_acl_on_windows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            self.assertFalse(windows_acl_is_protected(root / "dist"))

    def test_gallery_has_sections_export_and_prototype_compare(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            gallery = (root / "dist" / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="export-specs"', gallery)
            self.assertIn("[hidden]{display:none!important}", gallery)
            self.assertIn("一键导出规范", gallery)
            self.assertIn("对比 041–050", gallery)
            self.assertIn("导出本题对比规范", gallery)
            self.assertIn("设计意图", gallery)
            self.assertIn('"label":"进入产品","range":["001","008"]', gallery)
            self.assertIn('"label":"连续产品原型","range":["041","050"]', gallery)
            self.assertIn('"prototypeTasks":[{"id":"041"', gallery)
            self.assertIn("function renderCompare()", gallery)

    def test_spec_and_intent_open_inside_gallery_without_blob_navigation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            gallery = (root / "dist" / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('id="reader-overlay"', gallery)
            self.assertIn('id="reader-export"', gallery)
            self.assertIn('id="reader-progress"', gallery)
            self.assertIn('id="reader-content" class="reader-content" tabindex="0"', gallery)
            self.assertIn("function showReader", gallery)
            self.assertIn("function closeReader", gallery)
            self.assertIn("导出方案", gallery)
            self.assertIn("archive.href=piece.archiveUrl", gallery)
            self.assertIn("readerExport.href=normative?piece.specUrl:piece.intentUrl", gallery)
            self.assertIn("scrollbar-gutter:stable", gallery)
            self.assertIn("grid-template-rows:minmax(0,1fr)", gallery)
            self.assertIn("readerContent.focus()", gallery)
            self.assertIn("function scrollReaderByKeyboard", gallery)
            self.assertNotIn("function pieceArchive", gallery)
            self.assertNotIn("function viewText(text){const blob=", gallery)

    def test_reader_keyboard_works_after_focus_moves_to_dialog_controls(self) -> None:
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is required for the generated-gallery behavior probe")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            gallery_path = root / "dist" / "site" / "index.html"
            probe_path = root / "reader-probe.js"
            probe_path.write_text(
                r"""
const fs = require("fs");
const vm = require("vm");
const page = fs.readFileSync(process.argv[2], "utf8");
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const source = scripts.at(-1)[1];
class FakeClassList { add(){} remove(){} }
class FakeElement {
  constructor(tag="div") { this.tagName=tag.toUpperCase(); this.children=[]; this.listeners={}; this.attributes={}; this.classList=new FakeClassList(); this.hidden=false; this.inert=false; this.textContent=""; this.scrollTop=0; this.clientHeight=500; this.scrollHeight=2000; }
  append(...items){ this.children.push(...items); }
  appendChild(item){ this.children.push(item); }
  replaceChildren(...items){ this.children=[...items]; }
  setAttribute(name,value){ this.attributes[name]=String(value); }
  addEventListener(name,handler){ (this.listeners[name] ||= []).push(handler); }
  dispatch(name,event){ for(const handler of this.listeners[name]||[]) handler(event); }
  focus(){ document.activeElement=this; this.focused=true; }
  click(){}
  remove(){}
  scrollTo({top}){ this.scrollTop=Math.max(0,Math.min(top,this.scrollHeight-this.clientHeight)); this.dispatch("scroll",{}); }
}
const elements = {};
for (const selector of ["main","#browse-mode","#compare-mode","#export-specs","#reader-overlay",".reader-panel","#reader-kind","#reader-title","#reader-note","#reader-content","#reader-export","#reader-progress","#reader-top","#reader-close","body>header"]) elements[selector]=new FakeElement();
const document = {
  body:new FakeElement("body"), activeElement:null,
  querySelector(selector){ return elements[selector] || null; },
  createElement(tag){ return new FakeElement(tag); },
  addEventListener(){}
};
const context = {window:{DAEDALUS_DATA:{submissions:[],categories:[],prototypeTasks:[]}},document,Blob:function(){},URL:{createObjectURL(){return "blob:test";},revokeObjectURL(){}},setTimeout(){}};
vm.runInNewContext(source,context);
const piece={id:"001",slug:"scheme-001",title:"方案001",spec:"规范正文",intent:"意图正文",specUrl:"answers/001.spec.md",intentUrl:"answers/001.intent.md"};
const opener=new FakeElement("button");
context.showReader(piece,"spec",opener);
const content=elements["#reader-content"];
const topButton=elements["#reader-top"];
topButton.focus();
let prevented=false;
elements[".reader-panel"].dispatch("keydown",{key:"PageDown",target:topButton,preventDefault(){prevented=true;}});
if(!prevented || content.scrollTop<=0) throw new Error("PageDown did not scroll after focus moved to a dialog button");
if(!content.attributes["aria-label"]?.includes("复现规范正文")) throw new Error("reader content has no dynamic accessible name");
if(elements["#reader-export"].href!==piece.specUrl || elements["#reader-export"].download!=="001-scheme-001.spec.md") throw new Error("reader export is not a native file link");
context.closeReader();
if(!opener.focused) throw new Error("reader did not restore focus to its opener");
""",
                encoding="utf-8",
            )
            probe = subprocess.run(
                [node, str(probe_path), str(gallery_path)],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(probe.returncode, 0, probe.stderr)

    def test_build_emits_native_single_piece_files_and_reproducible_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            answer_dir = root / "dist" / "site" / "answers" / "codex--gpt-5.6-sol--xhigh"
            spec_path = answer_dir / "001-scheme-001.spec.md"
            intent_path = answer_dir / "001-scheme-001.intent.md"
            archive_path = answer_dir / "001-scheme-001.archive.html"
            self.assertEqual(spec_path.read_text(encoding="utf-8"), valid_spec("001", "001-scheme-001.html"))
            self.assertEqual(intent_path.read_text(encoding="utf-8"), valid_intent("001", "001-scheme-001.spec.md"))
            archive = archive_path.read_text(encoding="utf-8")
            encoded_html = base64.b64encode(HTML.encode("utf-8")).decode("ascii")
            self.assertIn("安全预览", archive)
            self.assertIn("导出原始 H5（完整运行）", archive)
            self.assertIn(f'data:text/html;base64,{encoded_html}', archive)
            self.assertIn('download="001-scheme-001.html"', archive)
            self.assertIn("## 规范元数据", archive)
            self.assertIn("## 设计意图", archive)
            self.assertNotIn("allow-same-origin", archive)
            gallery = (root / "dist" / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn('"specUrl":"answers/codex--gpt-5.6-sol--xhigh/001-scheme-001.spec.md"', gallery)
            self.assertIn('"intentUrl":"answers/codex--gpt-5.6-sol--xhigh/001-scheme-001.intent.md"', gallery)
            self.assertIn('"archiveUrl":"answers/codex--gpt-5.6-sol--xhigh/001-scheme-001.archive.html"', gallery)
            self.assertNotIn("function pieceArchive", gallery)

    def test_forfeit_is_valid_and_visible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="forfeited")
            completed, receipt = self.run_cli(root, "build", "--output", "dist")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            gallery = (root / "dist" / "site" / "index.html").read_text(encoding="utf-8")
            self.assertIn("我是鸡", gallery)
            self.assertIn("测试主动弃权", gallery)

    def test_subagent_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="forfeited", mismatch=True)
            completed, receipt = self.run_cli(root, "validate")
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("receipt-subagent-mismatch", {error["code"] for error in receipt["errors"]})

    def test_unsafe_declared_path_fails_before_reading_it(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            manifest_path = root / "models" / "codex" / "gpt-5.6-sol" / "xhigh" / "model.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["pieces"][0]["file"] = "../../../../secret.html"
            write_json(manifest_path, manifest)
            completed, receipt = self.run_cli(root, "validate")
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("unsafe-declared-path", {error["code"] for error in receipt["errors"]})

    def test_missing_intent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            folder = root / "models" / "codex" / "gpt-5.6-sol" / "xhigh"
            (folder / "001-scheme-001.intent.md").unlink()
            completed, receipt = self.run_cli(root, "validate")
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("invalid-intent-file", {error["code"] for error in receipt["errors"]})

    def test_prompt_heading_inside_spec_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            path = root / "models" / "codex" / "gpt-5.6-sol" / "xhigh" / "001-scheme-001.spec.md"
            path.write_text(path.read_text(encoding="utf-8") + "\n## 复刻提示词\n不应出现在这里。\n", encoding="utf-8")
            completed, receipt = self.run_cli(root, "validate")
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("spec-non-normative", {error["code"] for error in receipt["errors"]})

    def test_spec_color_missing_from_html_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            path = root / "models" / "codex" / "gpt-5.6-sol" / "xhigh" / "001-scheme-001.spec.md"
            path.write_text(path.read_text(encoding="utf-8").replace("#3ebd93", "#abcdef"), encoding="utf-8")
            completed, receipt = self.run_cli(root, "validate")
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("spec-color-mismatch", {error["code"] for error in receipt["errors"]})

    def test_starter_contains_no_answers_or_session_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_repo(root, submission="complete")
            (root / "CONTEXT.md").write_text("session claim", encoding="utf-8")
            completed, receipt = self.run_cli(root, "starter", "--output", "dist/clean.zip")
            self.assertEqual(completed.returncode, 0, completed.stdout)
            self.assertTrue(receipt["ok"])
            with zipfile.ZipFile(root / "dist" / "clean.zip") as archive:
                names = archive.namelist()
                self.assertIn("daedalus-starter/models/_index.json", names)
                self.assertFalse(any("model.json" in name or "CONTEXT" in name or name.endswith(".html") for name in names))
                registry = json.loads(archive.read("daedalus-starter/models/_index.json"))
                self.assertEqual(registry["submissions"], [])

    def test_atomic_replace_falls_back_when_live_output_cannot_be_renamed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            staged = root / "staged"
            output = root / "dist"
            staged.mkdir()
            output.mkdir()
            (staged / "site").mkdir()
            (output / "site").mkdir()
            (staged / "site" / "new.txt").write_text("new", encoding="utf-8")
            (output / "site" / "old.txt").write_text("old", encoding="utf-8")
            original_replace = Path.replace

            def deny_live_directory_rename(source: Path, target: Path) -> Path:
                if source == output:
                    raise PermissionError("simulated live preview lock")
                return original_replace(source, target)

            with patch.object(Path, "replace", deny_live_directory_rename):
                _atomic_replace(staged, output)

            self.assertEqual((output / "site" / "new.txt").read_text(encoding="utf-8"), "new")
            self.assertFalse((output / "site" / "old.txt").exists())
            self.assertFalse(staged.exists())
            self.assertFalse((root / "dist.previous").exists())

    @unittest.skipUnless(os.name == "nt", "Windows ACL regression")
    def test_atomic_replace_repairs_private_acl_when_live_output_cannot_be_renamed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            staged = root / "staged"
            staged.mkdir()
            (staged / "site").mkdir()
            (staged / "site" / "new.txt").write_text("new", encoding="utf-8")

            private_output = Path(tempfile.mkdtemp(prefix="private-output-", dir=root))
            output = root / "dist"
            private_output.replace(output)
            (output / "site").mkdir()
            (output / "site" / "old.txt").write_text("old", encoding="utf-8")
            self.assertTrue(windows_acl_is_protected(output))

            original_replace = Path.replace

            def deny_live_directory_rename(source: Path, target: Path) -> Path:
                if source == output:
                    raise PermissionError("simulated live preview lock")
                return original_replace(source, target)

            with patch.object(Path, "replace", deny_live_directory_rename):
                _atomic_replace(staged, output)

            self.assertFalse(windows_acl_is_protected(output))
            self.assertEqual((output / "site" / "new.txt").read_text(encoding="utf-8"), "new")


if __name__ == "__main__":
    unittest.main()
