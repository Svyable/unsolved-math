"""Keep human/agent entry points usable without granting execution authority."""

import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import pytest
import yaml

REPO_URL = "https://github.com/Svyable/unsolved-math"
FORM_NAMES = ("research-task.yml", "evidence-review.yml", "bug-report.yml")


def _index(root: Path) -> dict:
    return json.loads((root / "agents.json").read_text(encoding="utf-8"))


def test_agent_index_points_to_real_safe_entrypoints(project_root: Path) -> None:
    index = _index(project_root)
    assert index["schema_version"] == 1
    assert index["kind"] == "repository_contribution_index"
    assert index["project"] == "Svyable/unsolved-math"
    assert index["repository_url"] == REPO_URL
    assert index["clone_url"] == REPO_URL + ".git"
    for relative in index["entrypoints"].values():
        path = project_root / relative
        assert not Path(relative).is_absolute()
        assert path.resolve().is_relative_to(project_root.resolve())
        assert path.is_file(), relative
    for url in index["interfaces"].values():
        parts = urlsplit(url)
        assert parts.scheme == "https"
        assert parts.netloc in {"github.com", "api.github.com"}
        assert "Svyable/unsolved-math" in parts.path
    # Work-source files may legitimately be absent before synchronization.
    assert index["work_sources"]["research_queue"] == "data/queues/research.json"
    assert index["work_sources"]["history"] == "data/research-loop/history.jsonl"
    assert "do not invent" in index["work_sources"]["missing_queue_policy"]


def test_agent_index_preserves_authority_and_research_gates(project_root: Path) -> None:
    policy = _index(project_root)["contribution_policy"]
    for key in [
        "operator_authorization_required",
        "writes_require_own_github_identity",
        "search_before_create",
        "human_review_required",
        "agent_assistance_disclosure_required",
        "research_packets_require_two_lanes",
        "fork_pull_requests",
    ]:
        assert policy[key] is True
    for key in [
        "auto_merge_allowed",
        "upstream_status_writeback_allowed",
        "autonomous_parent_solve_claims_allowed",
        "hosted_agent_execution_service",
    ]:
        assert policy[key] is False
    assert policy["reserved_branch"] == "automation/hourly-research-loop"
    assert _index(project_root)["research_checks"][-1].startswith(
        "uv run oplab loop verify-manifest"
    )


@pytest.mark.parametrize("name", FORM_NAMES)
def test_issue_forms_match_machine_index(project_root: Path, name: str) -> None:
    path = f".github/ISSUE_TEMPLATE/{name}"
    form = yaml.safe_load((project_root / path).read_text(encoding="utf-8"))
    entry = next(item for item in _index(project_root)["issue_templates"] if item["path"] == path)
    assert len(form["name"]) > 3
    assert form["description"] and form["title"]
    assert not form.get("assignees")  # No unsolicited automatic assignment.
    assert not form.get("projects")
    fields = [item for item in form["body"] if item["type"] != "markdown"]
    ids = [item["id"] for item in fields]
    assert len(ids) == len(set(ids))
    assert all(re.fullmatch(r"[a-z][a-z0-9_-]*", value) for value in ids)
    assert all(item["type"] in {"input", "textarea", "checkboxes"} for item in fields)
    required = {
        item["id"] for item in fields if item.get("validations", {}).get("required") is True
    }
    assert required == set(entry["required_fields"])
    assert "attribution" in required
    checks = next(item for item in fields if item["id"] == "acknowledgements")
    assert checks["type"] == "checkboxes"
    assert len(checks["attributes"]["options"]) >= 3
    assert all(item["required"] is True for item in checks["attributes"]["options"])


def test_contribution_links_and_chooser_are_consistent(project_root: Path) -> None:
    config = yaml.safe_load(
        (project_root / ".github/ISSUE_TEMPLATE/config.yml").read_text(encoding="utf-8")
    )
    assert config["blank_issues_enabled"] is True
    assert all(item["url"].startswith(REPO_URL) for item in config["contact_links"])
    for name in ["README.md", "CONTRIBUTING.md", "docs/agent-contributions.md"]:
        path = project_root / name
        content = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if "://" in target or target.startswith("#"):
                continue
            local = (path.parent / target.split("#", 1)[0]).resolve()
            assert local.is_relative_to(project_root.resolve())
            assert local.exists(), f"Broken link in {name}: {target}"
    navigation = (project_root / "llms.txt").read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)]+)\)", navigation):
        if "/main/" in target:
            assert (project_root / target.split("/main/", 1)[1]).is_file()
    readme = (project_root / "README.md").read_text(encoding="utf-8")
    stack_start = "<!-- OPLAB:RESEARCH-STACK:START -->"
    assert readme.index("## Humans and agents") < readme.index(stack_start)
    assert readme.count("<!-- OPLAB:RESEARCH-STACK:START -->") == 1
    assert readme.count("<!-- OPLAB:RESEARCH-STACK:END -->") == 1


def test_fork_ci_stays_read_only_without_issue_execution(project_root: Path) -> None:
    # BaseLoader retains YAML's "on" as a string, not YAML 1.1's boolean True.
    ci = yaml.load(
        (project_root / ".github/workflows/ci.yml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )
    assert set(ci["on"]) == {"push", "pull_request"}
    assert ci["permissions"] == {"contents": "read"}
    steps = ci["jobs"]["quality"]["steps"]
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"]["persist-credentials"] == "false"
    assert "secrets." not in json.dumps(ci)
    for path in (project_root / ".github/workflows").glob("*.yml"):
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        assert not {"issues", "issue_comment", "pull_request_target"}.intersection(workflow["on"])
