"""Canonical forbidden runtime artifact paths for embargo guard tests.

trace_ref: docs/12_RUNTIME_EMBARGO_CONSTITUTION.md
"""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
CANONICAL_FORBIDDEN_RUNTIME_ARTIFACTS_PATH = (
    REPO_ROOT / "data" / "forbidden_runtime_artifacts.json"
)


def load_forbidden_runtime_artifact_paths() -> tuple[str, ...]:
    try:
        payload = json.loads(
            CANONICAL_FORBIDDEN_RUNTIME_ARTIFACTS_PATH.read_text(encoding="utf-8")
        )
    except OSError as exc:
        raise RuntimeError(
            "Missing canonical forbidden runtime artifact list: "
            "data/forbidden_runtime_artifacts.json"
        ) from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Invalid JSON in canonical forbidden runtime artifact list: "
            "data/forbidden_runtime_artifacts.json"
        ) from exc
    if not isinstance(payload, list) or not all(
        isinstance(item, str) and item for item in payload
    ):
        raise ValueError(
            "data/forbidden_runtime_artifacts.json must be a list of non-empty strings"
        )
    if len(payload) != len(set(payload)):
        raise ValueError("data/forbidden_runtime_artifacts.json must contain unique paths")
    repo_root_resolved = REPO_ROOT.resolve(strict=False)
    for item in payload:
        if (
            item.startswith(("/", "./", "../"))
            or "\\" in item
            or "//" in item
            or item.endswith("/")
            or "/./" in item
            or "/../" in item
        ):
            raise ValueError(
                "data/forbidden_runtime_artifacts.json must not contain absolute, "
                "relative, backslash, empty-segment, trailing-slash, or navigation paths"
            )
        candidate = (REPO_ROOT / item).resolve(strict=False)
        try:
            candidate.relative_to(repo_root_resolved)
        except ValueError as exc:
            raise ValueError(
                "data/forbidden_runtime_artifacts.json paths must stay within the repository"
            ) from exc
    return tuple(payload)
