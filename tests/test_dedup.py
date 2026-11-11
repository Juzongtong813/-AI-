#!/usr/bin/env python3
"""test_dedup.py — Co-origin / duplicate source detection."""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import dedup_sources as dd  # noqa: E402


def write_tmp(report):
    tf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(report, tf, ensure_ascii=False)
    tf.close()
    return tf.name


class TestDedup(unittest.TestCase):
    def test_host_grouping_detects_coorigin(self):
        report = {
            "evidence_sources": [
                {"id": "S1", "title": "AI company raises funds", "url": "https://news.a.com/x", "publisher": "A", "type": "media", "reliability": "medium"},
                {"id": "S2", "title": "AI company raises funds", "url": "https://news.b.com/x", "publisher": "B", "type": "media", "reliability": "medium"},
            ]
        }
        path = write_tmp(report)
        try:
            rc = dd.main(["--json", path, "--threshold", "0.5"])
            self.assertEqual(rc, 1, "same-host + similar headline should be flagged")
        finally:
            os.remove(path)

    def test_distinct_sources_clean(self):
        report = {
            "evidence_sources": [
                {"id": "S1", "title": "Official model card release", "url": "https://openai.com/card", "publisher": "official", "type": "official", "reliability": "high"},
                {"id": "S2", "title": "Independent benchmark review of model", "url": "https://arxiv.org/xyz", "publisher": "lab", "type": "academic", "reliability": "high"},
            ]
        }
        path = write_tmp(report)
        try:
            rc = dd.main(["--json", path])
            self.assertEqual(rc, 0, "distinct independent sources should be clean")
        finally:
            os.remove(path)

    def test_no_sources(self):
        path = write_tmp({"evidence_sources": []})
        try:
            rc = dd.main(["--json", path])
            self.assertEqual(rc, 0)
        finally:
            os.remove(path)

    def test_jaccard(self):
        self.assertGreaterEqual(dd.jaccard({"ai", "game", "tool"}, {"ai", "game", "demo"}), 0.0)
        self.assertEqual(dd.jaccard(set(), set()), 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
