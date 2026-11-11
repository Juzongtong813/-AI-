#!/usr/bin/env python3
"""validate_schema.py — Validate an AI Reality Check investigation report.

Validates a report JSON against the bundled JSON Schema (draft-07 subset:
type, required, enum, minLength, minItems, additionalProperties, properties).
Pure standard library — no third-party dependencies.

Usage:
    python scripts/validate_schema.py report.json
    python scripts/validate_schema.py report.json --schema path/to/schema.json
    cat report.json | python scripts/validate_schema.py -

Exit codes: 0 = valid, 1 = invalid, 2 = usage/IO error.
"""
import argparse
import json
import os
import sys

DEFAULT_SCHEMA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "skills",
    "ai-reality-check",
    "templates",
    "investigation-report.json",
)


class ValidationError(Exception):
    def __init__(self, message, path=None):
        self.message = message
        self.path = path or []
        super().__init__(message)


def _loc(path):
    return "/" + "/".join(str(p) for p in path) if path else "(root)"


def check_node(node, schema, path):
    """Recursively validate `node` against `schema` (a dict)."""
    if not isinstance(schema, dict):
        return
    node_type = schema.get("type")
    if node_type is not None:
        _check_type(node, node_type, path)
    if "enum" in schema:
        if node not in schema["enum"]:
            raise ValidationError(
                "value %r not in enum %s" % (node, schema["enum"]), path
            )
    if "minLength" in schema and isinstance(node, str):
        if len(node) < schema["minLength"]:
            raise ValidationError(
                "string length %d < minLength %d"
                % (len(node), schema["minLength"]),
                path,
            )
    if "minItems" in schema and isinstance(node, list):
        if len(node) < schema["minItems"]:
            raise ValidationError(
                "array length %d < minItems %d"
                % (len(node), schema["minItems"]),
                path,
            )
    if node_type == "object" and isinstance(node, dict):
        _check_object(node, schema, path)
    if node_type == "array" and isinstance(node, list):
        items = schema.get("items")
        if items is not None:
            for i, item in enumerate(node):
                check_node(item, items, path + [i])


def _check_type(node, expected, path):
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "boolean": bool,
        "integer": int,
        "number": (int, float),
    }
    # bool is subclass of int; handle explicitly
    if expected == "boolean":
        if isinstance(node, bool):
            return
        raise ValidationError("expected boolean, got %s" % type(node).__name__, path)
    if expected == "integer":
        if isinstance(node, int) and not isinstance(node, bool):
            return
        raise ValidationError("expected integer, got %s" % type(node).__name__, path)
    allowed = mapping.get(expected)
    if allowed is None:
        return  # unknown type keyword — ignore
    if expected == "string" and isinstance(node, str):
        return
    if expected == "array" and isinstance(node, list):
        return
    if expected == "object" and isinstance(node, dict):
        return
    if expected in ("number",) and isinstance(node, (int, float)) and not isinstance(node, bool):
        return
    raise ValidationError(
        "expected %s, got %s" % (expected, type(node).__name__), path
    )


def _check_object(node, schema, path):
    required = schema.get("required", [])
    for key in required:
        if key not in node:
            raise ValidationError("missing required property %r" % key, path + [key])
    props = schema.get("properties", {})
    for key, value in node.items():
        if key in props:
            check_node(value, props[key], path + [key])
    additional = schema.get("additionalProperties", True)
    if additional is False:
        for key in node.keys():
            if key not in props:
                raise ValidationError(
                    "additional property %r not allowed" % key, path + [key]
                )


def validate(data, schema):
    errors = []

    def collect(node, sch, path):
        try:
            check_node(node, sch, path)
        except ValidationError as e:
            errors.append("%s: %s" % (_loc(e.path), e.message))

    collect(data, schema, [])
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate AI Reality Check report JSON.")
    parser.add_argument("report", help="Path to report JSON, or '-' for stdin.")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA, help="Path to JSON Schema.")
    parser.add_argument("--quiet", action="store_true", help="Only print errors.")
    args = parser.parse_args(argv)

    try:
        if args.report == "-":
            data = json.load(sys.stdin)
        else:
            with open(args.report, "r", encoding="utf-8") as f:
                data = json.load(f)
        with open(args.schema, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    errors = validate(data, schema)
    if errors:
        if not args.quiet:
            print("INVALID — %d error(s):" % len(errors))
        for err in errors:
            print("  - %s" % err)
        return 1
    if not args.quiet:
        print("VALID: report conforms to schema %s" % schema.get("$id", args.schema))
    return 0


if __name__ == "__main__":
    sys.exit(main())
