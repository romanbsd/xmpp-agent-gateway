#!/usr/bin/env python3
"""Validate embedded protocol artifacts in the XMPP Agent Gateway ProtoXEP."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


EXAMPLE_PATTERN = re.compile(
    r"<example(?:\s+caption=(?P<quote>['\"])(?P<caption>.*?)(?P=quote))?>"
    r"\s*<!\[CDATA\[(?P<body>.*?)\]\]>\s*</example>",
    re.DOTALL,
)
NORMATIVE_JSON_SCHEMA_PATTERN = re.compile(
    r"<code\s+caption=(?P<quote>['\"])Normative .*? JSON Schema(?P=quote)>"
    r"\s*<!\[CDATA\[(?P<body>.*?)\]\]>\s*</code>",
    re.DOTALL,
)
XSD_PATTERN = re.compile(
    r"<code\s+caption=(?P<quote>['\"])Schema for .*?(?P=quote)>"
    r"\s*<!\[CDATA\[(?P<body>.*?)\]\]>\s*</code>",
    re.DOTALL,
)

REPRESENTATIVE_PAYLOADS = {
    "urn:xmpp:agent-api:0": (
        '<manifest-request xmlns="urn:xmpp:agent-api:0"/>'
    ),
    "urn:xmpp:agent-task:0": (
        '<task-state-request xmlns="urn:xmpp:agent-task:0" '
        'task-id="abcdefghijklmnopqrstuv"/>'
    ),
}


class ValidationError(RuntimeError):
    """A validation failure with a user-facing diagnostic."""


def run_xmllint(arguments: list[str], *, stdin: str | None = None) -> None:
    try:
        result = subprocess.run(
            ["xmllint", "--noout", *arguments],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ValidationError(
            "xmllint was not found; install libxml2 before running validation"
        ) from exc

    if result.returncode != 0:
        diagnostic = (result.stderr or result.stdout).strip()
        raise ValidationError(diagnostic or "xmllint failed without a diagnostic")


def validate_examples(source: str) -> int:
    examples = list(EXAMPLE_PATTERN.finditer(source))
    if not examples:
        raise ValidationError("no XML example blocks were found")

    for index, match in enumerate(examples, start=1):
        caption = match.group("caption") or f"example {index}"
        try:
            run_xmllint(["-"], stdin=f"<root>{match.group('body')}</root>")
        except ValidationError as exc:
            raise ValidationError(
                f"XML example {index} ({caption}) is not well-formed:\n{exc}"
            ) from exc

    return len(examples)


def validate_json_schemas(source: str) -> int:
    schemas = list(NORMATIVE_JSON_SCHEMA_PATTERN.finditer(source))
    if not schemas:
        raise ValidationError("no normative JSON Schema blocks were found")

    for index, match in enumerate(schemas, start=1):
        try:
            value = json.loads(match.group("body"))
        except json.JSONDecodeError as exc:
            raise ValidationError(
                f"normative JSON Schema {index} is invalid JSON: {exc}"
            ) from exc
        if not isinstance(value, dict):
            raise ValidationError(
                f"normative JSON Schema {index} must have an object root"
            )

    return len(schemas)


def validate_xml_schemas(source: str) -> int:
    schemas = list(XSD_PATTERN.finditer(source))
    if not schemas:
        raise ValidationError("no embedded XML Schema blocks were found")

    seen_namespaces: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="protoxep-schema-") as directory:
        temp_dir = Path(directory)
        for index, match in enumerate(schemas, start=1):
            schema = match.group("body")
            namespace_match = re.search(
                r"targetNamespace\s*=\s*['\"]([^'\"]+)['\"]", schema
            )
            if namespace_match is None:
                raise ValidationError(
                    f"embedded XML Schema {index} has no targetNamespace"
                )

            namespace = namespace_match.group(1)
            payload = REPRESENTATIVE_PAYLOADS.get(namespace)
            if payload is None:
                raise ValidationError(
                    "no representative payload is defined for XML Schema "
                    f"namespace {namespace!r}"
                )

            schema_path = temp_dir / f"schema-{index}.xsd"
            payload_path = temp_dir / f"payload-{index}.xml"
            schema_path.write_text(schema, encoding="utf-8")
            payload_path.write_text(payload, encoding="utf-8")

            try:
                run_xmllint(["--schema", str(schema_path), str(payload_path)])
            except ValidationError as exc:
                raise ValidationError(
                    f"embedded XML Schema for {namespace!r} failed:\n{exc}"
                ) from exc
            seen_namespaces.add(namespace)

    missing = set(REPRESENTATIVE_PAYLOADS) - seen_namespaces
    if missing:
        raise ValidationError(
            "missing embedded XML Schema for: " + ", ".join(sorted(missing))
        )

    return len(schemas)


def sha256_base64(value: str) -> str:
    return base64.b64encode(hashlib.sha256(value.encode()).digest()).decode()


def validate_canonical_hashes(source: str) -> int:
    patterns = {
        "manifest": re.compile(
            r"<manifest\s+xmlns=['\"]urn:xmpp:agent-api:0['\"].*?"
            r"(?P<hash><hash\b[^>]*>[^<]+</hash>)\s*"
            r"(?P<json><json>[^<]+</json>)",
            re.DOTALL,
        ),
        "tool schema": re.compile(
            r"<schema-hash>\s*(?P<hash><hash\b[^>]*>[^<]+</hash>)\s*"
            r"</schema-hash>\s*(?P<json><json>[^<]+</json>)",
            re.DOTALL,
        ),
    }

    for label, pattern in patterns.items():
        match = pattern.search(source)
        if match is None:
            raise ValidationError(
                f"could not find the canonical {label} hash example"
            )
        hash_element = ET.fromstring(match.group("hash"))
        if hash_element.get("algo") != "sha-256":
            raise ValidationError(f"canonical {label} hash must use sha-256")
        expected = (hash_element.text or "").strip()
        json_text = ET.fromstring(match.group("json")).text or ""
        actual = sha256_base64(json_text)
        if actual != expected:
            raise ValidationError(
                f"canonical {label} hash mismatch: expected {expected}, "
                f"calculated {actual}"
            )

    return len(patterns)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate embedded artifacts in the XMPP Agent Gateway ProtoXEP."
    )
    parser.add_argument(
        "xml",
        nargs="?",
        type=Path,
        default=Path("protoxep-xmpp-agent-gateway.xml"),
        help="ProtoXEP XML file (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    try:
        source = arguments.xml.read_text(encoding="utf-8")
        example_count = validate_examples(source)
        json_schema_count = validate_json_schemas(source)
        xml_schema_count = validate_xml_schemas(source)
        hash_count = validate_canonical_hashes(source)
    except (OSError, ValidationError) as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"validated {example_count} XML examples")
    print(f"validated {json_schema_count} normative JSON Schemas")
    print(f"validated {xml_schema_count} embedded XML Schemas")
    print(f"validated {hash_count} canonical artifact hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
