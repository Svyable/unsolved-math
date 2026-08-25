from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Annotated, NoReturn

import typer

from oplab.artifacts import read_model_jsonl
from oplab.config import load_ranking_config
from oplab.constants import UNVERIFIED_WARNING
from oplab.errors import OplabError
from oplab.models import NormalizedProblem, SourceManifest
from oplab.ranking import build_queues
from oplab.sources import HuggingFaceSource, LocalJsonSource
from oplab.sync import SyncService
from oplab.validation import validate_repository

app = typer.Typer(
    name="oplab",
    help="Evidence-first synchronization and ranking for open mathematics problems.",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
)
problems_app = typer.Typer(help="Search the compact imported problem index.")
problem_app = typer.Typer(help="Inspect one imported problem record.")
app.add_typer(problems_app, name="problems")
app.add_typer(problem_app, name="problem")


def _fail(message: str) -> NoReturn:
    typer.echo(f"error: {message}", err=True)
    raise typer.Exit(code=1)


def _load_index(repo_root: Path) -> list[NormalizedProblem]:
    index_path = repo_root / "data" / "current" / "problems.jsonl"
    if not index_path.exists():
        _fail("no current index; run `oplab sync` first")
    try:
        return read_model_jsonl(index_path, NormalizedProblem)
    except OplabError as exc:
        _fail(str(exc))


@app.command("sync")
def sync_command(
    revision: Annotated[str, typer.Option(help="Hugging Face revision to resolve.")] = "main",
    local_path: Annotated[
        Path | None, typer.Option(help="Offline problems.json path; disables remote fetch.")
    ] = None,
    source_revision: Annotated[
        str | None, typer.Option(help="Known immutable revision for --local-path.")
    ] = None,
    allow_network: Annotated[
        bool, typer.Option(help="Explicitly permit Hugging Face API/download access.")
    ] = False,
    force: Annotated[
        bool, typer.Option(help="Rebuild even when source and config are unchanged.")
    ] = False,
    limit: Annotated[int, typer.Option(min=1, max=5000, help="Entries per generated queue.")] = 200,
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Import a pinned UnsolvedMath snapshot and rebuild tracked review artifacts."""

    source = (
        LocalJsonSource(local_path, source_revision=source_revision)
        if local_path is not None
        else HuggingFaceSource(revision=revision, allow_network=allow_network)
    )
    service = SyncService(repo_root=repo_root.resolve(), source=source)
    try:
        outcome = service.run(force=force, queue_limit=limit)
    except OplabError as exc:
        _fail(str(exc))
    typer.echo(outcome.model_dump_json(indent=2))
    typer.echo(UNVERIFIED_WARNING)


@app.command("rank")
def rank_command(
    queue: Annotated[str, typer.Option(help="research or status-review")] = "research",
    limit: Annotated[int, typer.Option(min=1, max=1000)] = 25,
    as_of: Annotated[
        str | None, typer.Option(help="ISO date for deterministic freshness scoring.")
    ] = None,
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Preview an explainable ranking from the current compact index."""

    if queue not in {"research", "status-review"}:
        raise typer.BadParameter("queue must be 'research' or 'status-review'")
    if as_of is not None:
        try:
            effective_date = date.fromisoformat(as_of)
        except ValueError as exc:
            raise typer.BadParameter("as-of must be an ISO date (YYYY-MM-DD)") from exc
    else:
        effective_date = date.today()
    resolved_root = repo_root.resolve()
    problems = _load_index(resolved_root)
    try:
        config, _ = load_ranking_config(resolved_root / "config" / "ranking.toml")
    except OplabError as exc:
        _fail(str(exc))
    research, status_review = build_queues(problems, config, as_of=effective_date, limit=limit)
    selected = research if queue == "research" else status_review
    typer.echo(
        json.dumps(
            [item.model_dump(mode="json") for item in selected],
            ensure_ascii=False,
            indent=2,
        )
    )
    typer.echo(UNVERIFIED_WARNING)


@app.command("status")
def status_command(
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Show the pinned upstream revision and tracked artifact status."""

    manifest_path = repo_root.resolve() / "data" / "current" / "manifest.json"
    if not manifest_path.exists():
        typer.echo("No imported snapshot is tracked yet. Run `oplab sync`.")
        return
    try:
        manifest = SourceManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        _fail(f"invalid manifest: {exc}")
    typer.echo(manifest.model_dump_json(indent=2))
    typer.echo(UNVERIFIED_WARNING)


@problems_app.command("search")
def problems_search(
    status: Annotated[str | None, typer.Option(help="Imported status filter.")] = None,
    category: Annotated[str | None, typer.Option(help="Category slug/name filter.")] = None,
    max_difficulty: Annotated[
        int | None, typer.Option(min=1, max=5, help="Maximum imported difficulty level.")
    ] = None,
    limit: Annotated[int, typer.Option(min=1, max=1000)] = 25,
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Search normalized metadata without loading full problem statements."""

    problems = _load_index(repo_root.resolve())
    matches = [
        problem
        for problem in problems
        if (status is None or problem.imported_status == status.casefold())
        and (category is None or (problem.category or "").casefold() == category.casefold())
        and (
            max_difficulty is None
            or (problem.difficulty_level is not None and problem.difficulty_level <= max_difficulty)
        )
    ][:limit]
    typer.echo(
        json.dumps(
            [problem.model_dump(mode="json") for problem in matches],
            ensure_ascii=False,
            indent=2,
        )
    )


@problem_app.command("show")
def problem_show(
    problem_id: Annotated[str, typer.Argument(help="Canonical problem_number or upstream id.")],
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Show one normalized imported record and its trust marker."""

    match = next(
        (
            problem
            for problem in _load_index(repo_root.resolve())
            if problem.problem_id == problem_id
        ),
        None,
    )
    if match is None:
        _fail(f"problem not found: {problem_id}")
    typer.echo(match.model_dump_json(indent=2))


@app.command("validate")
def validate_command(
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Verify hashes, counts, trust markers, and research-queue guardrails."""

    try:
        report = validate_repository(repo_root.resolve())
    except OplabError as exc:
        _fail(str(exc))
    typer.echo(report.model_dump_json(indent=2))
    if not report.valid:
        raise typer.Exit(code=1)


@app.command("doctor")
def doctor_command(
    repo_root: Annotated[Path, typer.Option(help="Repository root.")] = Path("."),
) -> None:
    """Check the local runtime and repository layout."""

    resolved_root = repo_root.resolve()
    checks = {
        "python": sys.version.split()[0],
        "python_3_12_or_newer": sys.version_info >= (3, 12),
        "ranking_config": (resolved_root / "config" / "ranking.toml").is_file(),
        "current_manifest": (resolved_root / "data" / "current" / "manifest.json").is_file(),
        "local_snapshot_directory": str(resolved_root / ".oplab" / "snapshots"),
    }
    typer.echo(json.dumps(checks, indent=2))
    if not checks["python_3_12_or_newer"] or not checks["ranking_config"]:
        raise typer.Exit(code=1)
