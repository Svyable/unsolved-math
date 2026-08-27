from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from oplab.artifacts import atomic_write_bytes, read_model_jsonl
from oplab.cycle_store import load_cycle
from oplab.errors import IntegrityError, OplabError
from oplab.launch import assess_loop_readiness, load_launch_card
from oplab.loop import LoopHistoryEntry, evaluate_ranked_candidates, load_ranked_queue
from oplab.loop_config import load_research_loop_config

STACK_START = "<!-- OPLAB:RESEARCH-STACK:START -->"
STACK_END = "<!-- OPLAB:RESEARCH-STACK:END -->"
DEFAULT_NEXT_LIMIT = 5


def _code(value: str, *, limit: int | None = None) -> str:
    compact = " ".join(value.split()).replace("`", "'").replace("|", "/")
    if limit is not None and len(compact) > limit:
        compact = compact[: limit - 1].rstrip() + "…"
    return f"`{compact}`"


def _utc_text(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _active_stack(
    repo_root: Path,
    history: list[LoopHistoryEntry],
    *,
    as_of: datetime,
    queue_rank: dict[str, int],
) -> list[str]:
    visible = [entry for entry in history if entry.completed_at <= as_of]
    by_problem: dict[str, list[LoopHistoryEntry]] = defaultdict(list)
    for entry in visible:
        by_problem[entry.problem_id].append(entry)
    rows: list[tuple[int, float, str]] = []
    for problem_id, entries in by_problem.items():
        latest = max(entries, key=lambda item: (item.completed_at, item.cycle_id))
        title = problem_id
        next_step = "Cycle packet unavailable; inspect history before continuing."
        cycle_path = repo_root / "cases" / problem_id / "cycles" / latest.cycle_id
        try:
            cycle = load_cycle(cycle_path)
        except OplabError:
            pass
        else:
            title = cycle.frozen_problem.title
            next_step = cycle.next_step
        queue_position = queue_rank.get(problem_id, 10**9)
        queue_position_text = str(queue_position) if problem_id in queue_rank else "—"
        row = (
            f"| {{stack}} | {queue_position_text} | "
            f"{_code(f'{problem_id} — {title}', limit=90)} | "
            f"{len(entries)} | {_code(latest.conclusion.value)} | "
            f"{_utc_text(latest.completed_at)} | {_code(next_step, limit=120)} |"
        )
        rows.append((queue_position, -latest.completed_at.timestamp(), row))
    rows.sort(key=lambda item: (item[0], item[1], item[2]))
    return [
        row.replace("{stack}", str(index))
        for index, (_, _, row) in enumerate(rows, start=1)
    ]


def render_readme_dashboard(
    repo_root: Path,
    *,
    as_of: datetime | None = None,
    next_limit: int = DEFAULT_NEXT_LIMIT,
) -> str:
    """Render the generated work stack and next-run queue from tracked evidence."""

    now = as_of or datetime.now(UTC)
    if now.tzinfo is None:
        now = now.replace(tzinfo=UTC)
    config, _ = load_research_loop_config(repo_root / "config" / "research-loop.toml")
    history = read_model_jsonl(
        repo_root / "data" / "research-loop" / "history.jsonl", LoopHistoryEntry
    )
    queue_path = repo_root / "data" / "queues" / "research.json"
    queue = load_ranked_queue(queue_path) if queue_path.is_file() else []
    queue_rank = {candidate.problem_id: index for index, candidate in enumerate(queue, 1)}
    active_rows = _active_stack(repo_root, history, as_of=now, queue_rank=queue_rank)

    lines = [
        STACK_START,
        f"_Generated from tracked queue and cycle evidence as of {_utc_text(now)}._",
        "",
        "> Rankings prioritize research fit; they are not mathematical importance, truth, or",
        "> evidence that a problem is open or solved.",
        "",
        "### Current research stack",
        "",
    ]
    if queue:
        lines.append(
            "Active problems are ordered by deterministic queue rank; active problems absent "
            "from the current queue follow by most recent accepted cycle."
        )
    else:
        lines.append(
            "The ranked queue is unavailable. Active problems are shown by recent accepted "
            "cycle only; this is provisional activity order, not a ranking."
        )
    lines.extend(
        [
            "",
            "| Work order | Queue rank | Problem | Accepted cycles | Latest conclusion | "
            "Last progress | Next evidence target |",
            "|---:|---:|---|---:|---|---|---|",
        ]
    )
    lines.extend(
        active_rows or ["| — | — | No accepted research cycles yet | 0 | — | — | Run preflight |"]
    )
    lines.extend(["", "### Next up", ""])

    if queue:
        gates = evaluate_ranked_candidates(queue, history, config, as_of=now)
        eligible = [gate for gate in gates if gate.eligible][:next_limit]
        lines.extend(
            [
                "Candidates retain their deterministic queue rank after cooldown and "
                "anti-thrashing gates are applied. The first row is selected next if state "
                "does not change.",
                "",
                "| Run order | Queue rank | Problem | Score | Gate |",
                "|---:|---:|---|---:|---|",
            ]
        )
        for run_order, gate in enumerate(eligible, start=1):
            candidate = gate.candidate
            lines.append(
                f"| {run_order} | {gate.queue_rank} | "
                f"{_code(f'{candidate.problem_id} — {candidate.title}', limit=100)} | "
                f"{candidate.score:.2f} | {_code(gate.reason)} |"
            )
        if not eligible:
            lines.append("| — | — | No ranked candidate currently clears the loop gates | — | — |")
    else:
        report = assess_loop_readiness(repo_root, as_of=now)
        card = load_launch_card(repo_root / "config" / "first-run.json")
        status = (
            "eligible for next run"
            if report.ready and report.selection_mode == "provisional_launch_card"
            else "; ".join(report.blockers) or "blocked"
        )
        lines.extend(
            [
                "No deterministic research queue is tracked. The launch card below is "
                "provisional and explicitly not ranked; synchronization remains the next-run "
                "priority.",
                "",
                "| Order | Problem | Mode | Gate |",
                "|---:|---|---|---|",
            ]
        )
        for order, launch_candidate in enumerate(card.candidates, start=1):
            candidate_label = f"{launch_candidate.problem_id} — {launch_candidate.title}"
            candidate_status = (
                status
                if launch_candidate.problem_id == report.selected_problem_id or not report.ready
                else "not selected"
            )
            lines.append(
                f"| {order} | "
                f"{_code(candidate_label, limit=100)} | "
                f"{_code('PROVISIONAL_BOOTSTRAP_NOT_RANKED')} | "
                f"{_code(candidate_status, limit=140)} |"
            )
    lines.extend(
        [
            "",
            "The loop keeps retrying synchronization and eligible research on future runs. "
            "A blocked hour creates no cosmetic cycle and never bypasses human review.",
            STACK_END,
        ]
    )
    return "\n".join(lines)


def update_readme_dashboard(
    repo_root: Path,
    *,
    as_of: datetime | None = None,
    next_limit: int = DEFAULT_NEXT_LIMIT,
) -> bool:
    """Replace only the generated README section and report whether bytes changed."""

    readme_path = repo_root / "README.md"
    try:
        current = readme_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise IntegrityError(f"cannot read README dashboard target: {exc}") from exc
    if current.count(STACK_START) != 1 or current.count(STACK_END) != 1:
        raise IntegrityError("README must contain exactly one research-stack marker pair")
    start = current.index(STACK_START)
    end = current.index(STACK_END, start) + len(STACK_END)
    replacement = render_readme_dashboard(repo_root, as_of=as_of, next_limit=next_limit)
    updated = current[:start] + replacement + current[end:]
    if updated == current:
        return False
    atomic_write_bytes(readme_path, updated.encode("utf-8"))
    return True
