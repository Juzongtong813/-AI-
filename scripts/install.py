#!/usr/bin/env python3
"""install.py — AI Reality Check Skill installer.

Real, dependency-free installer. Detects common Agent skill directories, then
installs / updates / uninstalls / verifies the Skill. Supports Windows, macOS,
Linux. For unknown Agents, use --target <path> or the manual steps printed.

Supported Agents (auto-detected under the user home):
    workbuddy  ~/.workbuddy/skills/
    claude     ~/.claude/skills/
    cursor     ~/.cursor/skills/
    codex      ~/.codex/skills/

Usage:
    python scripts/install.py install [--agent workbuddy] [--force]
    python scripts/install.py update  [--agent workbuddy]
    python scripts/install.py uninstall [--agent workbuddy]
    python scripts/install.py check   [--agent workbuddy]
    python scripts/install.py list
    python scripts/install.py install --target /abs/path/to/skills

Exit codes: 0 = ok, 1 = action failed, 2 = usage error.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "ai-reality-check"
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_SOURCE = (SCRIPT_DIR / ".." / "skills" / SKILL_NAME).resolve()

KNOWN_AGENTS = {
    "workbuddy": ".workbuddy/skills",
    "claude": ".claude/skills",
    "cursor": ".cursor/skills",
    "codex": ".codex/skills",
}


def home():
    return Path.home()


def agent_target(agent):
    if agent not in KNOWN_AGENTS:
        raise ValueError("Unknown agent %r. Use --target to specify a path." % agent)
    return (home() / KNOWN_AGENTS[agent]).resolve()


def skill_dest(base_dir):
    return (Path(base_dir) / SKILL_NAME).resolve()


def verify_skill(skill_dir):
    """Check a SKILL.md exists and has required frontmatter keys."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return False, "SKILL.md missing"
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if not (text.startswith("---") or "\n---" in text):
        return False, "no frontmatter delimiters"
    has_name = bool(_find_key(text, "name:"))
    has_desc = bool(_find_key(text, "description:"))
    has_agent = "agent_created: true" in text
    missing = [k for k, ok in (("name", has_name), ("description", has_desc), ("agent_created: true", has_agent)) if not ok]
    if missing:
        return False, "missing frontmatter: " + ", ".join(missing)
    return True, "ok"


def _find_key(text, key):
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(key):
            return stripped
    return None


def do_install(target_base, force, dry_run):
    dest = skill_dest(target_base)
    if dest.exists():
        if not force:
            print("Already installed at %s" % dest)
            print("Use 'update' or --force to overwrite.")
            return 1
        if not dry_run:
            shutil.rmtree(dest)
    if dry_run:
        print("[dry-run] would install %s -> %s" % (SKILL_SOURCE, dest))
        return 0
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL_SOURCE, dest)
    ok, msg = verify_skill(dest)
    if not ok:
        print("ERROR: install completed but verification failed: %s" % msg)
        return 1
    print("Installed: %s" % dest)
    print("Verified: %s" % msg)
    return 0


def do_update(target_base, dry_run):
    return do_install(target_base, force=True, dry_run=dry_run)


def do_uninstall(target_base, dry_run):
    dest = skill_dest(target_base)
    if not dest.exists():
        print("Not installed at %s" % dest)
        return 0
    if dry_run:
        print("[dry-run] would remove %s" % dest)
        return 0
    shutil.rmtree(dest)
    print("Uninstalled: %s" % dest)
    return 0


def do_check(target_base):
    dest = skill_dest(target_base)
    if not dest.exists():
        print("Not installed at %s" % dest)
        return 1
    ok, msg = verify_skill(dest)
    print(("OK: " if ok else "FAIL: ") + str(dest) + " — " + msg)
    return 0 if ok else 1


def do_list():
    print("Known Agent skill directories:")
    for name, rel in KNOWN_AGENTS.items():
        base = (home() / rel).resolve()
        dest = skill_dest(base)
        state = "INSTALLED" if dest.exists() else ("exists" if base.exists() else "absent")
        print("  %-10s %s  [%s]" % (name, base, state))
    return 0


def resolve_base(args):
    if args.target:
        return Path(args.target).expanduser().resolve()
    if args.agent:
        return agent_target(args.agent)
    # default to workbuddy
    return agent_target("workbuddy")


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI Reality Check Skill installer.")
    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ("install", "update", "uninstall", "check"):
        p = sub.add_parser(cmd)
        p.add_argument("--agent", help="Agent name: " + ", ".join(KNOWN_AGENTS))
        p.add_argument("--target", help="Explicit skills directory path")
        p.add_argument("--force", action="store_true", help="Overwrite if present")
        p.add_argument("--dry-run", action="store_true", help="Show actions, do nothing")

    pl = sub.add_parser("list")
    _ = pl

    args = parser.parse_args(argv)

    if args.command == "list":
        return do_list()

    try:
        base = resolve_base(args)
    except ValueError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    if args.command == "install":
        return do_install(base, getattr(args, "force", False), args.dry_run)
    if args.command == "update":
        return do_update(base, args.dry_run)
    if args.command == "uninstall":
        return do_uninstall(base, args.dry_run)
    if args.command == "check":
        return do_check(base)
    return 2


if __name__ == "__main__":
    sys.exit(main())
