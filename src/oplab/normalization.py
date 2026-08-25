from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from oplab.config import RankingConfig
from oplab.errors import RecordValidationError
from oplab.hashing import canonical_json_bytes, sha256_bytes
from oplab.models import NormalizedProblem
from oplab.security import contains_instruction_like_content


def _string(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _nested_string(record: Mapping[str, Any], parent: str, *keys: str) -> str | None:
    nested = record.get(parent)
    if not isinstance(nested, Mapping):
        return None
    for key in keys:
        value = _string(nested.get(key))
        if value:
            return value
    return None


def normalize_status(value: object) -> str:
    status = (_string(value) or "unknown").casefold().replace("-", "_").replace(" ", "_")
    aliases = {"partiallysolved": "partially_solved", "partial": "partially_solved"}
    return aliases.get(status, status)


def _difficulty(record: Mapping[str, Any]) -> int | None:
    nested = record.get("difficulty")
    candidates: tuple[object, ...] = (
        nested.get("level") if isinstance(nested, Mapping) else None,
        record.get("difficulty_level_id"),
        record.get("difficulty_level"),
    )
    for value in candidates:
        if isinstance(value, bool):
            continue
        if isinstance(value, int) and 1 <= value <= 5:
            return value
        if isinstance(value, str) and value.strip().isdigit():
            parsed = int(value.strip())
            if 1 <= parsed <= 5:
                return parsed
    return None


def _keyword_matches(record: Mapping[str, Any], config: RankingConfig) -> tuple[str, ...]:
    tags = record.get("tags")
    tag_text = " ".join(str(value) for value in tags) if isinstance(tags, list) else ""
    haystack = "\n".join(
        filter(
            None,
            (
                _string(record.get("title")),
                _string(record.get("statement")),
                tag_text,
            ),
        )
    ).casefold()
    return tuple(
        sorted({word for word in config.keywords.computational if word.casefold() in haystack})
    )


def normalize_problem(record: Mapping[str, Any], config: RankingConfig) -> NormalizedProblem:
    canonical_id = _string(record.get("problem_number")) or _string(record.get("id"))
    if not canonical_id:
        raise RecordValidationError("record is missing both problem_number and id")
    title = _string(record.get("title"))
    if not title:
        raise RecordValidationError(f"record {canonical_id} is missing a title")

    category = _nested_string(record, "category", "slug", "name", "display_name")
    if not category:
        category = (
            _string(record.get("category"))
            if not isinstance(record.get("category"), Mapping)
            else None
        )

    research_classification = _string(record.get("research_classification"))
    statement_status = (_string(record.get("statement_status")) or "unknown").casefold()
    suspicious = contains_instruction_like_content(
        (
            record.get("title"),
            record.get("statement"),
            record.get("background"),
            record.get("research_summary"),
        )
    )

    return NormalizedProblem(
        problem_id=canonical_id,
        upstream_id=_string(record.get("id")),
        title=title,
        imported_status=normalize_status(record.get("status")),
        category=category,
        difficulty_level=_difficulty(record),
        statement_status=statement_status,
        research_classification=(
            research_classification.upper() if research_classification else None
        ),
        source_url=_string(record.get("source_url")),
        source_citation=_string(record.get("source_citation")),
        upstream_updated_at=_string(record.get("updated_at")),
        literature_checked_at=_string(record.get("literature_checked_at")),
        computational_keywords=_keyword_matches(record, config),
        suspicious_content=suspicious,
        raw_record_sha256=sha256_bytes(canonical_json_bytes(record)),
    )
