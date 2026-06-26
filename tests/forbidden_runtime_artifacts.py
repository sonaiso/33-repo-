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


def _has_unsafe_path_format(path_value: str) -> bool:
    if path_value != path_value.strip():
        return True
    if any(char in path_value for char in ("\x00", "\r", "\n", "\t")):
        return True
    if ":" in path_value or path_value.startswith("~"):
        return True
    if (
        path_value.startswith(("/", "./", "../"))
        or "\\" in path_value
        or "//" in path_value
        or path_value.endswith("/")
        or "/./" in path_value
        or "/../" in path_value
    ):
        return True
    return any(part in {"", ".", ".."} for part in path_value.split("/"))


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
        if _has_unsafe_path_format(item):
            raise ValueError(
                "data/forbidden_runtime_artifacts.json must not contain absolute, "
                "relative, backslash, empty-segment, trailing-slash, navigation, "
                "or other unsafe path formats"
            )
        candidate = (REPO_ROOT / item).resolve(strict=False)
        try:
            candidate.relative_to(repo_root_resolved)
        except ValueError as exc:
            raise ValueError(
                "data/forbidden_runtime_artifacts.json paths must stay within the repository"
            ) from exc
    return tuple(payload)
