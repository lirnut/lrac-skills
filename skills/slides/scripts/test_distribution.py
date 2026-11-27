#!/usr/bin/env python3
"""Test bundling safety and local resource links without slide dependencies."""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


GROUP = Path(__file__).resolve().parents[1]
SKILLS = ("slide-share", "slide-survey", "slide-tech")


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="slide-distribution-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "scripts").mkdir()
        self.script = self.root / "scripts/sync_common.py"
        shutil.copyfile(GROUP / "scripts/sync_common.py", self.script)
        for name in SKILLS:
            entry = self.root / name / "SKILL.md"
            entry.parent.mkdir()
            entry.write_text(f"# {name}\n")
        self.source = self.root / "_shared/assets/template.txt"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("shared template\n")

    def run_sync(self, *args, success=True):
        result = subprocess.run(
            [sys.executable, str(self.script), *args], text=True, capture_output=True,
        )
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return result

    def test_initial_sync_and_source_updates(self):
        self.run_sync("--check", success=False)
        self.run_sync("--write")
        self.run_sync("--check")
        self.source.write_text("new template\n")
        self.run_sync("--check", success=False)
        self.run_sync("--write")
        self.run_sync("--check")
        for name in SKILLS:
            self.assertEqual((self.root / name / "common/assets/template.txt").read_bytes(), self.source.read_bytes())

    def test_modified_bundle_is_preserved(self):
        self.run_sync("--write")
        target = self.root / "slide-share/common/assets/template.txt"
        target.write_text("user work\n")
        self.run_sync("--write", success=False)
        self.assertEqual(target.read_text(), "user work\n")

    def test_unmanaged_files_are_preserved(self):
        self.run_sync("--write")
        target = self.root / "slide-tech/common/private.txt"
        target.write_text("user work\n")
        self.run_sync("--write", success=False)
        self.assertEqual(target.read_text(), "user work\n")

    def test_only_owned_stale_files_are_removed(self):
        self.run_sync("--write")
        self.source.unlink()
        replacement = self.source.with_name("new.txt")
        replacement.write_text("new source\n")
        self.run_sync("--write")
        for name in SKILLS:
            self.assertFalse((self.root / name / "common/assets/template.txt").exists())
            self.assertTrue((self.root / name / "common/assets/new.txt").exists())

    def test_symlink_is_refused(self):
        target = self.root / "slide-tech/common"
        target.symlink_to(self.source.parent, target_is_directory=True)
        self.run_sync("--write", success=False)

    def test_repository_bundles_and_links(self):
        result = subprocess.run(
            [sys.executable, str(GROUP / "scripts/sync_common.py"), "--check"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((GROUP / "SKILL.md").exists())
        for name in SKILLS:
            root = GROUP / name
            # Standalone copies must resolve without _shared or sibling directories.
            installed = self.root / "installed" / name
            shutil.copytree(root, installed)
            for markdown in installed.rglob("*.md"):
                for link in re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
                    if "://" in link or link.startswith("#"):
                        continue
                    target = (markdown.parent / link.split("#", 1)[0]).resolve()
                    self.assertTrue(target.is_relative_to(installed.resolve()), str(target))
                    self.assertTrue(target.exists(), f"{markdown}: {link}")


if __name__ == "__main__":
    unittest.main()
