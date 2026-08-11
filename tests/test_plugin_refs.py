"""Every internal reference in the plugin's own markdown must resolve.

Written after renaming rubrics/spec-criteria.md to conformance.md left four
journey files pointing at a file that no longer existed. lint_transcript.py
catches this class of bug in transcripts; nothing caught it in the docs that
produce them.
"""
from pathlib import Path

import pytest

from lint_transcript import ROOT_REF_RE, SKILL_REF_RE

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = [ROOT / "plugin", ROOT / "plugin-sweep"]


SKIP_DIRS = {"node_modules", "dist", "build", ".venv"}


def markdown_files() -> list[Path]:
    """The plugin's own markdown. `plugin/dashboard/` carries a vendored
    node_modules whose README files outnumber the real docs four to one."""
    return sorted(p for plugin in PLUGINS if plugin.is_dir()
                  for p in plugin.rglob("*.md")
                  if not SKIP_DIRS & set(p.parts))


def owning_plugin(path: Path) -> Path:
    return next(p for p in PLUGINS if path.is_relative_to(p))


def test_markdown_files_are_discovered():
    assert len(markdown_files()) > 20


@pytest.mark.parametrize("path", markdown_files(), ids=lambda p: str(p.name))
def test_plugin_root_references_resolve(path):
    """`${CLAUDE_PLUGIN_ROOT}/x` must exist inside the plugin that names it."""
    plugin = owning_plugin(path)
    missing = []
    for m in ROOT_REF_RE.finditer(path.read_text()):
        rel = m.group(1).rstrip(".,;:!?)\"'`")
        # Trailing-glob references (schemas/*.schema.md) name a set, not a file.
        if "*" in rel:
            if not list(plugin.glob(rel)):
                missing.append(rel)
        elif not (plugin / rel).exists():
            missing.append(rel)
    assert missing == [], f"{path.relative_to(ROOT)} -> {missing}"


@pytest.mark.parametrize("path", markdown_files(), ids=lambda p: str(p.name))
def test_skill_references_resolve(path):
    """`/pm-job-search:<name>` must name a real skill directory."""
    skills = ROOT / "plugin" / "skills"
    missing = sorted({m.group(1) for m in SKILL_REF_RE.finditer(path.read_text())
                      if not (skills / m.group(1)).is_dir()})
    assert missing == [], f"{path.relative_to(ROOT)} -> {missing}"


def test_rubrics_named_by_the_harness_all_exist():
    """Phase 0 reads exactly these four; Phase 4 dispatches one call each."""
    rubrics = ROOT / "plugin" / "skills" / "test-personas" / "rubrics"
    expected = {"groundedness.md", "coherence.md", "conformance.md", "tone.md"}
    actual = {p.name for p in rubrics.glob("*.md")}
    assert actual == expected


def test_every_rubric_declares_a_verdict_rule():
    """A rubric with no aggregation rule leaves the judge to invent one."""
    rubrics = ROOT / "plugin" / "skills" / "test-personas" / "rubrics"
    for p in sorted(rubrics.glob("*.md")):
        text = p.read_text()
        assert "## Verdict" in text, f"{p.name} has no '## Verdict' section"
        assert "## Worked examples" in text, f"{p.name} has no worked examples"
