#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

REQUIRED = {"schemaVersion", "implementation", "digest", "suite", "startedAt", "finishedAt", "tests"}


def verify(document: dict) -> list[str]:
    errors = []
    missing = REQUIRED - document.keys()
    if missing:
        errors.append("missing fields: " + ", ".join(sorted(missing)))
    if document.get("schemaVersion") != "conformance.advfab.org/v1":
        errors.append("unsupported schemaVersion")
    if document.get("suite") != "v1.0":
        errors.append("unsupported suite")
    if not re.fullmatch(r"sha256:[a-f0-9]{64}", document.get("digest", "")):
        errors.append("digest must be immutable sha256")
    tests = document.get("tests", [])
    if not tests:
        errors.append("at least one test result is required")
    for result in tests:
        if result.get("status") not in {"pass", "fail", "skip"}:
            errors.append(f"invalid status for {result.get('id', '<unknown>')}")
        if result.get("status") == "skip" and not result.get("reason"):
            errors.append(f"skip requires reason for {result.get('id', '<unknown>')}")
    return errors


if __name__ == "__main__":
    payload = json.loads(Path(sys.argv[1]).read_text())
    failures = verify(payload)
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print("valid AdvFab Conformance v1 result")
