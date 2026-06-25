"""Canonical forbidden runtime anti-pattern signatures for embargo guard tests.

trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple


REPO_ROOT = Path(__file__).parent.parent
CANONICAL_FORBIDDEN_RUNTIME_PATTERNS_PATH = (
    REPO_ROOT / "data" / "forbidden_runtime_patterns.json"
)
REQUIRED_PATTERN_FIELDS = frozenset(
    {"id", "pattern", "mode", "description", "allowed_in"}
)
VALID_PATTERN_MODES = frozenset({"regex", "literal"})
PATTERN_ID_REGEX = re.compile(r"^[A-Z][A-Z0-9_]*$")
ALLOWED_AUDIT_DOCUMENT_PREFIX = "docs/"
ALLOWED_AUDIT_DOCUMENT_SUFFIX = ".md"


class ForbiddenRuntimePattern(NamedTuple):
    id: str
    pattern: str
    mode: str
    description: str
    allowed_in: tuple[str, ...]


class CompiledForbiddenRuntimePattern(NamedTuple):
    id: str
    matcher: re.Pattern[str]


def _load_json_payload(path: Path = CANONICAL_FORBIDDEN_RUNTIME_PATTERNS_PATH) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(
            f"Missing canonical forbidden runtime pattern list: {path}"
        ) from exc
    except OSError as exc:
        raise RuntimeError(
            f"Unable to read canonical forbidden runtime pattern list: {path}"
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Invalid JSON in canonical forbidden runtime pattern list: {path}"
        ) from exc


def _validate_allowed_in(record_id: str, allowed_in: Any) -> tuple[str, ...]:
    if not isinstance(allowed_in, list) or not allowed_in:
        raise ValueError(f"{record_id}.allowed_in must be a non-empty list")
    if not all(isinstance(item, str) and item for item in allowed_in):
        raise ValueError(f"{record_id}.allowed_in must contain non-empty strings")
    if len(allowed_in) != len(set(allowed_in)):
        raise ValueError(f"{record_id}.allowed_in must contain unique paths")
    for path in allowed_in:
        if path.startswith(("/", "./", "../")) or "\\" in path or "//" in path:
            raise ValueError(
                f"{record_id}.allowed_in must not contain absolute, relative, "
                "backslash, or empty-segment paths"
            )
        if path.endswith("/") or "/./" in path or "/../" in path:
            raise ValueError(
                f"{record_id}.allowed_in must not contain trailing slashes "
                "or navigation segments"
            )
        candidate = REPO_ROOT / path
        try:
            candidate.relative_to(REPO_ROOT)
        except ValueError as exc:
            raise ValueError(
                f"{record_id}.allowed_in must stay within the repository"
            ) from exc
        if (
            not path.startswith(ALLOWED_AUDIT_DOCUMENT_PREFIX)
            or not path.endswith(ALLOWED_AUDIT_DOCUMENT_SUFFIX)
            or not candidate.is_file()
        ):
            raise ValueError(
                f"{record_id}.allowed_in must reference existing audit "
                "documentation files"
            )
    return tuple(allowed_in)


def _validate_record(record: Any, index: int) -> ForbiddenRuntimePattern:
    if not isinstance(record, dict):
        raise ValueError("data/forbidden_runtime_patterns.json records must be objects")
    missing = REQUIRED_PATTERN_FIELDS - set(record)
    if missing:
        raise ValueError(
            "data/forbidden_runtime_patterns.json record "
            f"{index} missing fields: {', '.join(sorted(missing))}"
        )

    record_id = record["id"]
    pattern = record["pattern"]
    mode = record["mode"]
    description = record["description"]
    allowed_in = record["allowed_in"]

    if not isinstance(record_id, str) or not PATTERN_ID_REGEX.fullmatch(record_id):
        raise ValueError(f"record {index}.id must be non-empty uppercase snake-case")
    if not isinstance(pattern, str):
        raise ValueError(f"{record_id}.pattern must be a string")
    if not pattern:
        raise ValueError(f"{record_id}.pattern must be non-empty")
    if mode not in VALID_PATTERN_MODES:
        raise ValueError(f"{record_id}.mode must be one of: literal, regex")
    if not isinstance(description, str) or not description:
        raise ValueError(f"{record_id}.description must be a non-empty string")

    allowed_paths = _validate_allowed_in(record_id, allowed_in)
    if mode == "regex":
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"{record_id}.pattern must compile as regex") from exc

    return ForbiddenRuntimePattern(
        id=record_id,
        pattern=pattern,
        mode=mode,
        description=description,
        allowed_in=allowed_paths,
    )


@cache
def load_forbidden_runtime_patterns(
    path: Path = CANONICAL_FORBIDDEN_RUNTIME_PATTERNS_PATH,
) -> tuple[ForbiddenRuntimePattern, ...]:
    payload = _load_json_payload(path)
    if not isinstance(payload, list) or not payload:
        raise ValueError(
            "data/forbidden_runtime_patterns.json must be a non-empty list"
        )

    records = tuple(
        _validate_record(record, record_index)
        for record_index, record in enumerate(payload)
    )
    ids = [record.id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("data/forbidden_runtime_patterns.json must contain unique ids")

    pattern_keys = [(record.mode, record.pattern) for record in records]
    if len(pattern_keys) != len(set(pattern_keys)):
        raise ValueError(
            "data/forbidden_runtime_patterns.json must contain unique pattern/mode pairs"
        )
    return records


def compile_forbidden_runtime_patterns(
    patterns: tuple[ForbiddenRuntimePattern, ...] | None = None,
) -> tuple[CompiledForbiddenRuntimePattern, ...]:
    source_patterns = patterns or load_forbidden_runtime_patterns()
    compiled: list[CompiledForbiddenRuntimePattern] = []
    for pattern in source_patterns:
        expression = pattern.pattern
        if pattern.mode == "literal":
            expression = re.escape(expression)
        compiled.append(
            CompiledForbiddenRuntimePattern(
                id=pattern.id,
                matcher=re.compile(expression),
            )
        )
    return tuple(compiled)


def allowed_forbidden_runtime_pattern_paths(
    records: tuple[ForbiddenRuntimePattern, ...] | None = None,
) -> frozenset[Path]:
    source_records = records or load_forbidden_runtime_patterns()
    return frozenset(
        REPO_ROOT / allowed_path
        for record in source_records
        for allowed_path in record.allowed_in
    )
