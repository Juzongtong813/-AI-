#!/usr/bin/env python3
"""test_schema.py — Validate the report JSON Schema engine against samples and edge cases."""
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import validate_schema as vs  # noqa: E402

SAMPLE = os.path.join(ROOT, "tests", "samples", "sample-report.json")


class TestSchema(unittest.TestCase):
    def setUp(self):
        with open(SAMPLE, "r", encoding="utf-8") as f:
            self.good = json.load(f)
        with open(os.path.join(ROOT, "skills", "ai-reality-check", "templates", "investigation-report.json"), "r", encoding="utf-8") as f:
            self.schema = json.load(f)

    def test_valid_sample(self):
        errors = vs.validate(self.good, self.schema)
        self.assertEqual(errors, [], "valid sample should have no errors: %s" % errors)

    def test_missing_required_meta_field(self):
        bad = json.loads(json.dumps(self.good))
        del bad["meta"]["mode"]
        errors = vs.validate(bad, self.schema)
        self.assertTrue(any("mode" in e for e in errors), "should flag missing meta.mode")

    def test_bad_verdict_enum(self):
        bad = json.loads(json.dumps(self.good))
        bad["verdict"] = "totally_real"
        errors = vs.validate(bad, self.schema)
        self.assertTrue(any("verdict" in e for e in errors), "should flag bad verdict enum")

    def test_bad_core_claim_category(self):
        bad = json.loads(json.dumps(self.good))
        bad["core_claims"][0]["category"] = "not_a_category"
        errors = vs.validate(bad, self.schema)
        self.assertTrue(any("category" in e for e in errors), "should flag bad category")

    def test_personal_impact_additional_properties(self):
        bad = json.loads(json.dumps(self.good))
        bad["personal_impact"] = {
            "user_goal": "x", "relevance": "y", "recommendation": "z", "caveats": "w",
            "secret_extra": "not allowed",
        }
        errors = vs.validate(bad, self.schema)
        self.assertTrue(any("secret_extra" in e for e in errors), "additionalProperties:false should catch extra key")

    def test_empty_claims(self):
        bad = json.loads(json.dumps(self.good))
        bad["core_claims"] = []
        errors = vs.validate(bad, self.schema)
        self.assertTrue(any("core_claims" in e for e in errors), "should flag minItems=1 on core_claims")

    def test_cli_valid(self):
        rc = vs.main(["--quiet", SAMPLE])
        self.assertEqual(rc, 0)

    def test_cli_invalid_exit(self):
        rc = vs.main(["--quiet", __file__])  # this file is not valid JSON
        self.assertNotEqual(rc, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
