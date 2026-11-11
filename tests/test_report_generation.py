#!/usr/bin/env python3
"""test_report_generation.py — Render Markdown from JSON and check key sections."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import generate_report as gr  # noqa: E402

SAMPLE = os.path.join(ROOT, "tests", "samples", "sample-report.json")


class TestReportGeneration(unittest.TestCase):
    def setUp(self):
        with open(SAMPLE, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.md = gr.render(self.data)

    def test_contains_core_sections(self):
        for section in [
            "一句话结论",
            "视频/内容核心主张",
            "主张逐项验证",
            "证据来源",
            "营销夸大分析",
            "调查局限",
            "最终判断",
        ]:
            self.assertIn(section, self.md, "missing section: %s" % section)

    def test_verdict_label_translated(self):
        # sample verdict is 'misleading' -> Chinese label '误导性表达'
        self.assertIn("误导性表达", self.md)

    def test_confidence_label_translated(self):
        self.assertIn("medium", self.md)  # confidence kept as enum token in summary line

    def test_personal_impact_absent_message(self):
        # sample has no personal_impact
        self.assertIn("未开启个人目标分析", self.md)

    def test_claims_rendered(self):
        self.assertIn("C1", self.md)
        self.assertIn("C3", self.md)

    def test_generate_to_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as tf:
            path = tf.name
        try:
            rc = gr.main(["--json", SAMPLE, "--out", path])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.getsize(path) > 1000)
        finally:
            os.remove(path)

    def test_personal_impact_present(self):
        data = json.loads(json.dumps(self.data))
        data["personal_impact"] = {
            "user_goal": "转 AI 应用开发",
            "relevance": "中等",
            "recommendation": "先补提示词与调试",
            "caveats": "技术仍在演进",
        }
        md = gr.render(data)
        self.assertIn("转 AI 应用开发", md)
        self.assertIn("个人目标分析", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
