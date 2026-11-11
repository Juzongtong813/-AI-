#!/usr/bin/env python3
"""dedup_sources.py — Heuristic co-origin / duplicate-source detector.

Helps the investigator avoid counting one original story (press release / repost)
as multiple independent pieces of evidence. Heuristics only — the Agent should
still apply judgment and write independence_note.

Checks:
  1. Same publisher host grouping (shared domain).
  2. Headline similarity (Jaccard over tokens) to flag reposts of the same story.
  3. Surfaces existing independence_note text for review.

Usage:
    python scripts/dedup_sources.py --json report.json
    python scripts/dedup_sources.py --json report.json --threshold 0.4

Exit codes: 0 = ok, 1 = potential co-origin found, 2 = usage/IO error.
"""
import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

STOP = set("the a an of to in on for and or with is are was were this that it as at by from".split())


def host_of(url):
    try:
        h = urlparse(url).netloc.lower()
        return h[4:] if h.startswith("www.") else h
    except Exception:
        return ""


def tokens(title):
    if not title:
        return set()
    return {t for t in re.split(r"[^0-9a-zA-Z\u4e00-\u9fff]+", title.lower()) if t and t not in STOP and len(t) > 1}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect co-origin / duplicate sources.")
    parser.add_argument("--json", required=True, help="Path to report JSON.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Title similarity threshold.")
    args = parser.parse_args(argv)

    try:
        with open(args.json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    sources = data.get("evidence_sources", [])
    if not sources:
        print("No evidence_sources to analyze.")
        return 0

    found = False
    print("=== Source host grouping ===")
    by_host = {}
    for s in sources:
        by_host.setdefault(host_of(s.get("url", "")), []).append(s.get("id", "?"))
    for host, ids in sorted(by_host.items()):
        flag = "  <-- multiple sources, same host" if len(ids) > 1 else ""
        if len(ids) > 1:
            found = True
        print("  %-30s %s%s" % (host or "(no url)", ", ".join(ids), flag))

    print("\n=== Headline similarity (possible reposts) ===")
    sim_found = False
    for i in range(len(sources)):
        for j in range(i + 1, len(sources)):
            ti, tj = tokens(sources[i].get("title", "")), tokens(sources[j].get("title", ""))
            sim = jaccard(ti, tj)
            if sim >= args.threshold and (ti or tj):
                sim_found = True
                found = True
                print("  %.2f  %s <-> %s" % (sim, sources[i].get("id", "?"), sources[j].get("id", "?")))
    if not sim_found:
        print("  (none above threshold %.2f)" % args.threshold)

    print("\n=== Existing independence notes ===")
    any_note = False
    for s in sources:
        note = s.get("independence_note")
        if note:
            any_note = True
            print("  %s: %s" % (s.get("id", "?"), note))
    if not any_note:
        print("  (none recorded — consider filling independence_note)")

    if found:
        print("\nRESULT: potential co-origin / duplicate sources detected. Review before counting as independent evidence.")
        return 1
    print("\nRESULT: no obvious co-origin signals.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
