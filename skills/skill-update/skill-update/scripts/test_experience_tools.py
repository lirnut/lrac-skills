#!/usr/bin/env python3
"""Integration tests using isolated repositories, never the real experience inbox."""

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


GROUP = Path(__file__).resolve().parents[2]
CAPTURE = GROUP / "skill-expcap/scripts/record_experience.py"
MANAGE = GROUP / "skill-update/scripts/manage_experiences.py"
LOG_REL = Path("skills/skill-update/logs")


class ExperienceToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="skill-experience-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        for name in ("skill-update", "skill-expcap"):
            entry = self.repo / "skills/skill-update" / name / "SKILL.md"
            entry.parent.mkdir(parents=True)
            entry.write_text(f"# {name}\n")
        (self.repo / ".gitignore").write_text("logs\n")
        self.git("add", ".gitignore", "skills")
        self.git("commit", "-qm", "fixture")
        self.payload = {
            "source": {"project": "test-project", "session_id": None},
            "topics": ["slide-share", "render-validation"],
            "kind": "verified-fix",
            "problem": "编译成功后仍有内容裁切。",
            "lesson": "需要检查渲染。",
            "action": "布局修改后检查渲染。",
            "evidence": "重新渲染后确认裁切消失。",
            "scope": "布局修改",
            "confidence": "verified",
        }

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True, text=True, capture_output=True,
        ).stdout.strip()

    def run_tool(self, script, *args, payload=None, success=True, repo=None):
        result = subprocess.run(
            [sys.executable, str(script), "--repo", str(repo or self.repo), *args],
            input=json.dumps(payload, ensure_ascii=False) if payload is not None else None,
            text=True, capture_output=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def capture(self, **kwargs):
        return self.run_tool(CAPTURE, payload=self.payload, **kwargs)

    def test_capture_and_exact_duplicate(self):
        first = self.capture()
        second = self.capture()
        self.assertEqual(first["status"], "recorded")
        self.assertEqual(second["status"], "duplicate")
        self.assertEqual(first["id"], second["id"])
        path = Path(first["path"])
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(len(self.run_tool(MANAGE, "list")), 1)

    def test_parallel_capture_deduplicates(self):
        with ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda _: self.capture(), range(10)))
        self.assertEqual(sum(r["status"] == "recorded" for r in results), 1)
        self.assertEqual(len({r["id"] for r in results}), 1)

    def test_distinct_sources_are_preserved(self):
        self.capture()
        self.payload["source"]["project"] = "another-project"
        self.capture()
        self.assertEqual(len(self.run_tool(MANAGE, "list")), 2)
        self.assertEqual(self.run_tool(MANAGE, "list", "--topic", "unrelated"), [])

    def test_missing_repo_and_missing_ignore_do_not_write(self):
        missing = self.repo / "missing"
        self.capture(success=False, repo=missing)
        self.assertFalse(missing.exists())
        (self.repo / ".gitignore").write_text("")
        self.capture(success=False)
        self.assertFalse((self.repo / LOG_REL).exists())

    def test_invalid_payloads_and_secrets(self):
        for field, value in (("kind", []), ("confidence", {}), ("topics", [])):
            payload = {**self.payload, field: value}
            self.run_tool(CAPTURE, payload=payload, success=False)
        payload = {**self.payload, "evidence": "api_key=abcdefghijklmnop123456"}
        self.run_tool(CAPTURE, payload=payload, success=False)
        payload = {**self.payload, "confidence": "unverified"}
        self.run_tool(CAPTURE, payload=payload, success=False)
        self.assertFalse((self.repo / LOG_REL).exists())

    def test_symlink_and_tracked_logs_are_refused(self):
        root = self.repo / LOG_REL
        outside = self.repo / "elsewhere"
        outside.mkdir()
        root.symlink_to(outside, target_is_directory=True)
        self.capture(success=False)
        root.unlink()
        result = self.capture()
        self.git("add", "-f", str(Path(result["path"]).relative_to(self.repo)))
        self.capture(success=False)

    def test_decision_lifecycle(self):
        event_id = self.capture()["id"]
        self.git("branch", "feat/slide-share-skill")
        commit = self.git("rev-parse", "HEAD")
        self.run_tool(
            MANAGE, "record", "--event", event_id, "--decision", "applied",
            "--reason", "test incorporation", "--branch", "feat/slide-share-skill",
            "--commit", commit,
        )
        self.assertEqual(self.run_tool(MANAGE, "list"), [])
        self.assertEqual(self.run_tool(MANAGE, "list", "--all")[0]["decision"], "applied")
        self.run_tool(
            MANAGE, "record", "--event", event_id, "--decision", "pending",
            "--reason", "branch abandoned",
        )
        self.assertEqual(self.run_tool(MANAGE, "list")[0]["decision"], "pending")
        self.run_tool(
            MANAGE, "record", "--event", event_id, "--decision", "deferred",
            "--reason", "needs evidence",
        )
        self.assertEqual(self.run_tool(MANAGE, "list")[0]["decision"], "deferred")

    def test_invalid_decisions_and_malformed_logs_fail_safely(self):
        event = self.capture()
        self.run_tool(
            MANAGE, "record", "--event", event["id"], "--decision", "applied",
            "--reason", "missing commit", success=False,
        )
        self.run_tool(
            MANAGE, "record", "--event", "unknown", "--decision", "pending",
            "--reason", "unknown event", success=False,
        )
        Path(event["path"]).write_text("{broken", encoding="utf-8")
        self.run_tool(MANAGE, "list", success=False)
        self.capture(success=False)

    def test_scripts_run_from_separate_installation(self):
        install = self.repo / "installation"
        install.mkdir()
        capture = install / CAPTURE.name
        manage = install / MANAGE.name
        shutil.copyfile(CAPTURE, capture)
        shutil.copyfile(MANAGE, manage)
        result = self.run_tool(capture, payload=self.payload)
        self.assertTrue(Path(result["path"]).is_relative_to(self.repo / LOG_REL))
        self.assertEqual(len(self.run_tool(manage, "list")), 1)
        self.assertFalse((install / "logs").exists())

    def test_rejected_events_can_be_reopened(self):
        event_id = self.capture()["id"]
        self.run_tool(
            MANAGE, "record", "--event", event_id, "--decision", "rejected",
            "--reason", "already covered",
        )
        self.assertEqual(self.run_tool(MANAGE, "list"), [])
        self.assertEqual(self.run_tool(MANAGE, "list", "--all")[0]["decision"], "rejected")
        self.run_tool(
            MANAGE, "record", "--event", event_id, "--decision", "pending",
            "--reason", "new evidence",
        )
        self.assertEqual(len(self.run_tool(MANAGE, "list")), 1)

    def test_unrelated_commit_cannot_be_marked_applied(self):
        event_id = self.capture()["id"]
        self.git("branch", "feat/slide-share-skill")
        (self.repo / "unrelated.txt").write_text("unrelated\n")
        self.git("add", "unrelated.txt")
        self.git("commit", "-qm", "not on review branch")
        self.run_tool(
            MANAGE, "record", "--event", event_id, "--decision", "applied",
            "--reason", "wrong branch", "--branch", "feat/slide-share-skill",
            "--commit", self.git("rev-parse", "HEAD"), success=False,
        )
        self.assertEqual(self.run_tool(MANAGE, "list")[0]["decision"], "pending")


if __name__ == "__main__":
    unittest.main()
