from __future__ import annotations

from datetime import UTC, date, datetime

from oplab.config import RankingConfig
from oplab.models import NormalizedProblem, RankedProblem


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized).date()
    except ValueError:
        try:
            return date.fromisoformat(normalized[:10])
        except ValueError:
            return None


def _freshness(problem: NormalizedProblem, config: RankingConfig, as_of: date) -> tuple[float, str]:
    checked = _parse_date(problem.literature_checked_at)
    if checked is None:
        return config.freshness.missing, "literature check date is missing"
    age = max(0, (as_of - checked).days)
    if age <= config.freshness.fresh_days:
        return config.freshness.fresh, f"literature check is {age} days old"
    if age <= config.freshness.aging_days:
        return config.freshness.aging, f"literature check is aging ({age} days)"
    return config.freshness.stale, f"literature check is stale ({age} days)"


def is_research_eligible(problem: NormalizedProblem, config: RankingConfig) -> tuple[bool, str]:
    if problem.imported_status not in config.eligibility.statuses:
        return False, f"imported status {problem.imported_status!r} is outside the research gate"
    if problem.difficulty_level is None:
        return False, "difficulty is unknown"
    if problem.difficulty_level > config.eligibility.max_difficulty:
        return False, f"difficulty L{problem.difficulty_level} exceeds the configured maximum"
    if problem.statement_status in config.eligibility.excluded_statement_statuses:
        return False, f"statement status {problem.statement_status!r} requires review first"
    if (problem.research_classification or "").startswith("SOLVED-"):
        return False, "research classification conflicts with an active research queue"
    return True, "eligible"


def rank_research_problem(
    problem: NormalizedProblem, config: RankingConfig, *, as_of: date
) -> RankedProblem | None:
    eligible, _ = is_research_eligible(problem, config)
    if not eligible:
        return None

    difficulty_key = (
        f"L{problem.difficulty_level}" if problem.difficulty_level is not None else "unknown"
    )
    tractability = config.difficulty.get(difficulty_key, config.difficulty.get("unknown", 0.0))
    statement_quality = config.statement_quality.get(
        problem.statement_status, config.statement_quality.get("unknown", 0.0)
    )
    if problem.source_url and problem.source_citation:
        provenance = 1.0
        provenance_reason = "source URL and citation are present"
    elif problem.source_url or problem.source_citation:
        provenance = 0.7
        provenance_reason = "one provenance field is present"
    else:
        provenance = 0.0
        provenance_reason = "source URL and citation are missing"
    freshness, freshness_reason = _freshness(problem, config, as_of)
    classification = problem.research_classification or "unknown"
    traction = config.research_traction.get(
        classification, config.research_traction.get("unknown", 0.0)
    )
    keyword_count = len(problem.computational_keywords)
    computational = min(1.0, keyword_count / 2.0)

    components = {
        "tractability": tractability,
        "statement_quality": statement_quality,
        "provenance": provenance,
        "literature_freshness": freshness,
        "research_traction": traction,
        "computational_affordance": computational,
    }
    weighted = sum(
        components[name] * weight for name, weight in config.weights.model_dump().items()
    )
    keyword_reason = (
        "computational keywords: " + ", ".join(problem.computational_keywords)
        if problem.computational_keywords
        else "no configured computational keyword matched"
    )
    reasons = (
        f"difficulty {difficulty_key}",
        f"statement status {problem.statement_status}",
        provenance_reason,
        freshness_reason,
        f"research classification {classification}",
        keyword_reason,
    )
    return RankedProblem(
        problem_id=problem.problem_id,
        title=problem.title,
        imported_status=problem.imported_status,
        difficulty_level=problem.difficulty_level,
        category=problem.category,
        score=round(weighted * 100, 2),
        components={key: round(value, 4) for key, value in components.items()},
        reasons=reasons,
    )


def _status_conflict(problem: NormalizedProblem) -> bool:
    classification = problem.research_classification or ""
    classification_solved = classification.startswith("SOLVED-")
    status_solved = problem.imported_status == "solved"
    return classification_solved != status_solved and bool(classification)


def rank_status_review_problem(
    problem: NormalizedProblem, config: RankingConfig, *, as_of: date
) -> RankedProblem | None:
    conflict = 1.0 if _status_conflict(problem) else 0.0
    statement_issue = {
        "unrecoverable": 1.0,
        "reconstructed_unverified": 0.8,
        "unknown": 0.35,
    }.get(problem.statement_status, 0.0)
    checked = _parse_date(problem.literature_checked_at)
    if checked is None:
        freshness_issue = 1.0
        freshness_reason = "literature check date is missing"
    else:
        age = max(0, (as_of - checked).days)
        freshness_issue = min(1.0, age / max(1, config.freshness.aging_days))
        freshness_reason = f"literature check is {age} days old"
    provenance_issue = 1.0 - (
        1.0
        if problem.source_url and problem.source_citation
        else 0.7
        if problem.source_url or problem.source_citation
        else 0.0
    )
    suspicious = 1.0 if problem.suspicious_content else 0.0
    components = {
        "status_conflict": conflict,
        "statement_issue": statement_issue,
        "literature_staleness": freshness_issue,
        "provenance_gap": provenance_issue,
        "suspicious_content": suspicious,
    }
    score = 100 * (
        conflict * 0.35
        + statement_issue * 0.25
        + freshness_issue * 0.20
        + provenance_issue * 0.10
        + suspicious * 0.10
    )
    if score < 5.0:
        return None
    reasons = (
        "imported status conflicts with research classification"
        if conflict
        else "no status/classification conflict detected",
        f"statement status {problem.statement_status}",
        freshness_reason,
        "provenance is incomplete" if provenance_issue else "source URL and citation are present",
        "instruction-like imported content detected"
        if suspicious
        else "no configured instruction-like marker detected",
    )
    return RankedProblem(
        problem_id=problem.problem_id,
        title=problem.title,
        imported_status=problem.imported_status,
        difficulty_level=problem.difficulty_level,
        category=problem.category,
        score=round(score, 2),
        components={key: round(value, 4) for key, value in components.items()},
        reasons=reasons,
    )


def build_queues(
    problems: list[NormalizedProblem],
    config: RankingConfig,
    *,
    as_of: date | None = None,
    limit: int = 200,
) -> tuple[list[RankedProblem], list[RankedProblem]]:
    effective_date = as_of or datetime.now(UTC).date()
    research = [
        ranked
        for problem in problems
        if (ranked := rank_research_problem(problem, config, as_of=effective_date)) is not None
    ]
    status_review = [
        ranked
        for problem in problems
        if (ranked := rank_status_review_problem(problem, config, as_of=effective_date)) is not None
    ]
    research.sort(key=lambda item: (-item.score, item.problem_id))
    status_review.sort(key=lambda item: (-item.score, item.problem_id))
    return research[:limit], status_review[:limit]
