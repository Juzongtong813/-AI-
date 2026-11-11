#!/usr/bin/env python3
"""test_install.py — Installer logic (install / check / uninstall) against a temp target."""
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import install as inst  # noqa: E402


class TestInstall(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="arc-install-")
        self.target = os.path.join(self.tmp, "skills")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_install_and_check(self):
        rc = inst.main(["install", "--target", self.target, "--force"])
        self.assertEqual(rc, 0)
        dest = os.path.join(self.target, "ai-reality-check")
        self.assertTrue(os.path.isfile(os.path.join(dest, "SKILL.md")))
        rc2 = inst.main(["check", "--target", self.target])
        self.assertEqual(rc2, 0)

    def test_already_installed_without_force(self):
        inst.main(["install", "--target", self.target, "--force"])
        rc = inst.main(["install", "--target", self.target])  # no force
        self.assertEqual(rc, 1, "should refuse re-install without --force")

    def test_uninstall(self):
        inst.main(["install", "--target", self.target, "--force"])
        rc = inst.main(["uninstall", "--target", self.target])
        self.assertEqual(rc, 0)
        self.assertFalse(os.path.isdir(os.path.join(self.target, "ai-reality-check")))
        rc2 = inst.main(["check", "--target", self.target])
        self.assertEqual(rc2, 1, "check should fail after uninstall")

    def test_dry_run(self):
        rc = inst.main(["install", "--target", self.target, "--dry-run", "--force"])
        self.assertEqual(rc, 0)
        self.assertFalse(os.path.isdir(os.path.join(self.target, "ai-reality-check")),
                         "dry-run must not create files")


if __name__ == "__main__":
    unittest.main(verbosity=2)
