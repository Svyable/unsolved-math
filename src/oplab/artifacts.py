from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ValidationError

from oplab.errors import IntegrityError
from oplab.hashing import canonical_json_bytes


def atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
        temporary.write(content)
        temporary.flush()
        os.fsync(temporary.fileno())
    os.replace(temporary_path, path)


def model_jsonl_bytes(models: Iterable[BaseModel]) -> bytes:
    return b"".join(canonical_json_bytes(model.model_dump(mode="json")) for model in models)


def jsonl_bytes(values: Iterable[dict[str, Any]]) -> bytes:
    return b"".join(canonical_json_bytes(value) for value in values)


def read_model_jsonl[T: BaseModel](path: Path, model_type: type[T]) -> list[T]:
    if not path.exists():
        return []
    parsed: list[T] = []
    line_number = 0
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line_number += 1
                if line.strip():
                    parsed.append(model_type.model_validate_json(line))
    except (OSError, ValidationError, ValueError) as exc:
        raise IntegrityError(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
    return parsed


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"cannot read JSON artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise IntegrityError(f"expected a JSON object at {path}")
    return value
