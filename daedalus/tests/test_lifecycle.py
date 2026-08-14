from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from daedalus.lifecycle import (
    PROTOTYPE_SPEC_HEADINGS,
    PROTOTYPE_VIEWPORTS,
    TASK_IDS,
    VISUAL_SPEC_HEADINGS,
)


HTML = """<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>@media(prefers-reduced-motion:reduce){*{animation:none}}</style></head><body><main id="app">ok</main></body></html>"""


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def make_repo(root: Path, *, submission: str | None = None, mismatch: bool = False) -> None:
    briefs = []
    for task_id in TASK_IDS:
        brief = {
            "id": task_id,
            "job": "job-" + task_id,
            "title": "题目" + task_id,
            "category": "prototype" if task_id in PROTOTYPE_VIEWPORTS else "pages",
            "scene": "测试场景",
            "viewport": PROTOTYPE_VIEWPORTS.get(task_id, "desktop"),
            "must_have": ["一个模块"],
        }
        if task_id in PROTOTYPE_VIEWPORTS:
            brief["core_flow"] = ["开始", "完成"]
            brief["exception"] = {"trigger": "失败", "recovery": ["重试"]}
        briefs.append(brief)
    write_json(root / "catalog" / "briefs.json", {"schemaVersion": 3, "count": 50, "briefs": briefs})
    entries = []
    if submission:
        ident = {"harness": "codex", "model": "gpt-5.6-sol", "reasoningEffort": "xhigh"}
        folder = root / "models" / "codex" / "gpt-5.6-sol" / "xhigh"
        folder.mkdir(parents=True)
        pieces = []
        ids = TASK_IDS if submission == "complete" else TASK_IDS[:3]
        visual = "\n".join(f"## {heading}\n内容" for heading in VISUAL_SPEC_HEADINGS)
        product = "\n".join(f"## {heading}\n内容" for heading in PROTOTYPE_SPEC_HEADINGS)
        for task_id in ids:
            slug = "scheme-" + task_id
            html_name = f"{task_id}-{slug}.html"
            spec_name = f"{task_id}-{slug}.spec.md"
            (folder / html_name).write_text(HTML, encoding="utf-8")
            (folder / spec_name).write_text(visual + ("\n" + product if task_id in PROTOTYPE_VIEWPORTS else ""), encoding="utf-8")
            pieces.append({"id": task_id, "slug": slug, "title": "方案" + task_id, "file": html_name, "spec": spec_name, "status": "complete"})
        manifest = {"schemaVersion": 3, **ident, "displayName": "Fixture", "status": submission, "pieces": pieces, "runReceipt": "run-receipt.json"}
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


if __name__ == "__main__":
    unittest.main()
