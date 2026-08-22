"""Headless tests for grade-judge.html's parser, run under node.

The tool is a single self-contained HTML file with no build step and no JS test
runner in this repo, so its logic previously had zero automated coverage — which
is how it once shipped a blind-pass leak that exposed judge verdicts before the
gate. The DOM wiring is guarded behind `typeof document !== "undefined"`, so the
parser can be required from node and exercised against the real corpus.

Skips cleanly if node isn't installed; never silently passes.
"""
import json
import re
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tests" / "judge-calibration" / "grade-judge.html"
RUNS = ROOT / "tests" / "judge-calibration" / "runs"

node = shutil.which("node")
pytestmark = pytest.mark.skipif(node is None, reason="node not installed")

RUBRICS = ["lint", "groundedness", "coherence", "conformance", "tone"]


def extract_js() -> str:
    blocks = re.findall(r"<script[^>]*>(.*?)</script>", TOOL.read_text(), re.S)
    assert blocks, "no <script> block found in grade-judge.html"
    return "\n;\n".join(blocks)


def run_node(body: str, tmp_path: Path):
    """Evaluate `body` with the tool's exports in scope; body prints JSON."""
    # .cjs already provides `module` — redeclaring it is a SyntaxError.
    script = tmp_path / "harness.cjs"
    script.write_text(
        extract_js()
        + "\nconst T = module.exports;\n"
        + textwrap.dedent(body)
    )
    proc = subprocess.run([node, str(script)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def judge_files():
    """Only files in the restructured format. The six retired-journey judge
    files (reflection, case-practice, cold-start-cv) were never re-judged and
    are still four-tier hard/soft/spec/critique — the tool is not expected to
    parse them, and sweeping them in would make this suite fail for the wrong
    reason."""
    return sorted(p for p in RUNS.rglob("*.judge.md")
                  if "## Groundedness" in p.read_text())


def test_tool_exports_load_under_node(tmp_path):
    out = run_node("console.log(JSON.stringify(T.RUBRICS));", tmp_path)
    assert out == RUBRICS


def test_dom_wiring_is_guarded(tmp_path):
    """Loading the file under node must not throw — proof the DOM guard holds."""
    out = run_node("console.log(JSON.stringify(typeof T.parseJudgeFile));", tmp_path)
    assert out == "function"


def test_corpus_has_judge_files():
    assert len(judge_files()) >= 8


@pytest.mark.parametrize("path", judge_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_every_corpus_judge_file_parses(path, tmp_path):
    """Every rubric section must be found and yield a PASS/FAIL. An unparseable
    verdict silently becomes an unlabellable row in the tool."""
    out = run_node(f"""
        const fs = require('fs');
        const r = T.parseJudgeFile(fs.readFileSync({json.dumps(str(path))}, 'utf8'));
        console.log(JSON.stringify({{
          verdicts: Object.fromEntries(T.RUBRICS.map(k => [k, r.rubrics[k].verdict])),
          present: Object.fromEntries(T.RUBRICS.map(k => [k, r.rubrics[k].present])),
          counts: Object.fromEntries(T.RUBRICS.map(k => [k, r.rubrics[k].findings.length])),
          overall: r.overallJudge, notes: r.notes, meta: r.meta,
        }}));
    """, tmp_path)
    assert all(out["present"].values()), f"missing sections: {out['present']}"
    for rubric, v in out["verdicts"].items():
        assert v in ("PASS", "FAIL"), f"{rubric} verdict unparseable: {v!r}"
    assert out["overall"] and out["overall"].startswith(("PASS", "FAIL"))
    assert out["notes"] == []
    assert out["meta"].get("snapshot")


@pytest.mark.parametrize("path", judge_files(), ids=lambda p: f"{p.parent.name}/{p.name}")
def test_parsed_verdicts_match_the_files_own_summary(path, tmp_path):
    """The five-line block at the bottom is written by the orchestrator; the
    per-section verdicts are written by four separate judges. They must agree,
    or the file is internally inconsistent and the tool would show one of them."""
    text = path.read_text()
    summary = {}
    for rubric in RUBRICS:
        m = re.search(rf"^\s+{rubric.capitalize()}:\s+(PASS|FAIL)", text,
                      re.IGNORECASE | re.MULTILINE)
        assert m, f"no summary line for {rubric} in {path.name}"
        summary[rubric] = m.group(1).upper()
    out = run_node(f"""
        const fs = require('fs');
        const r = T.parseJudgeFile(fs.readFileSync({json.dumps(str(path))}, 'utf8'));
        console.log(JSON.stringify(Object.fromEntries(
          T.RUBRICS.map(k => [k, r.rubrics[k].verdict])));
        );
    """.replace("));\n        );", ")));"), tmp_path)
    assert out == summary


def test_zero_tolerance_rubrics_never_pass_with_findings(tmp_path):
    """groundedness and conformance are zero-tolerance — a PASS alongside a
    finding means a judge broke its own aggregation rule."""
    bad = []
    for path in judge_files():
        out = run_node(f"""
            const fs = require('fs');
            const r = T.parseJudgeFile(fs.readFileSync({json.dumps(str(path))}, 'utf8'));
            console.log(JSON.stringify(Object.fromEntries(
              ['groundedness','conformance'].map(k =>
                [k, [r.rubrics[k].verdict, r.rubrics[k].findings.length]]))));
        """, tmp_path)
        for rubric, (verdict, n) in out.items():
            if verdict == "PASS" and n:
                bad.append(f"{path.parent.name}/{path.name}:{rubric} PASS with {n}")
    assert bad == [], bad


def test_no_findings_phrase_yields_zero(tmp_path):
    out = run_node("""
        const r = T.parseJudgeFile([
          '# Findings — x', '**Snapshot:** empty',
          '## Lint', '', '## Groundedness', '### Findings', 'No findings.',
          '### Verdict', '**PASS** — clean',
          '## Coherence', '### Findings', 'No findings.', '### Verdict', '**PASS** — ok',
          '## Conformance', '### Findings', 'No findings.', '### Verdict', '**PASS** — ok',
          '## Tone', '### Findings', 'No findings.', '### Verdict', '**PASS** — ok',
          '## Verdict', '**Overall: PASS**'].join('\\n'));
        console.log(JSON.stringify({
          g: r.rubrics.groundedness.findings.length,
          lint: r.rubrics.lint.verdict, overall: r.overallJudge, notes: r.notes }));
    """, tmp_path)
    assert out == {"g": 0, "lint": "PASS", "overall": "PASS", "notes": []}


def test_lint_verdict_derives_from_script_lines_not_a_stated_verdict(tmp_path):
    out = run_node("""
        const r = T.parseJudgeFile([
          '## Lint', '', '    turn 16: lint.jargon — x', '    NOT CHECKED: lint.hardcoded-cadence',
          '## Verdict', '**Overall: FAIL**'].join('\\n'));
        console.log(JSON.stringify({
          v: r.rubrics.lint.verdict, n: r.rubrics.lint.findings.length,
          turn: r.rubrics.lint.findings[0].turn, skipped: r.rubrics.lint.skipped.length }));
    """, tmp_path)
    assert out == {"v": "FAIL", "n": 1, "turn": 16, "skipped": 1}


def test_not_checked_alone_is_a_lint_pass(tmp_path):
    """A rule that couldn't run is not a violation."""
    out = run_node("""
        const r = T.parseJudgeFile(['## Lint', '    NOT CHECKED: lint.hardcoded-cadence'].join('\\n'));
        console.log(JSON.stringify({ v: r.rubrics.lint.verdict, n: r.rubrics.lint.findings.length }));
    """, tmp_path)
    assert out == {"v": "PASS", "n": 0}


def test_missing_section_reports_a_note_rather_than_guessing(tmp_path):
    out = run_node("""
        const r = T.parseJudgeFile(['# Findings — x', '## Tone', '### Verdict', '**PASS** — ok'].join('\\n'));
        console.log(JSON.stringify({ notes: r.notes.length, g: r.rubrics.groundedness.verdict }));
    """, tmp_path)
    assert out["g"] is None and out["notes"] >= 1


def test_derived_overall_uses_gating_rubrics_only(tmp_path):
    """Lint is not graded by a human — it enters the gate as the script's own
    verdict, passed in separately. Only groundedness and conformance need a
    human call."""
    out = run_node("""
        const all = v => ({groundedness:v, coherence:v, conformance:v, tone:v});
        console.log(JSON.stringify({
          allpass:  T.derivedOverall(all('PASS'), 'PASS'),
          advisory: T.derivedOverall(Object.assign(all('PASS'), {coherence:'FAIL', tone:'FAIL'}), 'PASS'),
          gating:   T.derivedOverall(Object.assign(all('PASS'), {groundedness:'FAIL'}), 'PASS'),
          lintfail: T.derivedOverall(all('PASS'), 'FAIL'),
          partial:  T.derivedOverall(Object.assign(all('PASS'), {conformance:null}), 'PASS'),
          nolint:   T.derivedOverall(all('PASS'), null),
        }));
    """, tmp_path)
    assert out == {"allpass": "PASS", "advisory": "PASS", "gating": "FAIL",
                   "lintfail": "FAIL", "partial": None, "nolint": None}


def test_lint_needs_no_human_verdict_for_overall_to_derive(tmp_path):
    """Regression: requiring a human lint verdict meant overall never derived
    once the tool stopped asking for one."""
    out = run_node("""
        console.log(JSON.stringify(
          T.derivedOverall({groundedness:'PASS', conformance:'PASS'}, 'PASS')));
    """, tmp_path)
    assert out == "PASS"


def test_wrapped_finding_bullet_stays_one_finding(tmp_path):
    out = run_node("""
        const r = T.parseJudgeFile([
          '## Coherence', '### Findings',
          '- **turn 4:** first line of a long finding',
          '  which wrapped onto a second line',
          '- **turn 9:** second finding',
          '### Verdict', '**FAIL** — x'].join('\\n'));
        console.log(JSON.stringify({ n: r.rubrics.coherence.findings.length,
          turns: r.rubrics.coherence.findings.map(f => f.turn),
          wrapped: r.rubrics.coherence.findings[0].text.indexOf('wrapped') > -1 }));
    """, tmp_path)
    assert out == {"n": 2, "turns": [4, 9], "wrapped": True}


def test_transcript_parser_finds_turns(tmp_path):
    path = RUNS / "2026-08-10" / "maya-cold-start.md"
    out = run_node(f"""
        const fs = require('fs');
        const t = T.parseTranscript(fs.readFileSync({json.dumps(str(path))}, 'utf8'));
        console.log(JSON.stringify({{ n: t.length, first: t[0].role,
          assistants: t.filter(x => x.role === 'ASSISTANT').length }}));
    """, tmp_path)
    assert out["n"] > 20 and out["first"] == "USER" and out["assistants"] >= 20


# --- negative controls -------------------------------------------------------

CONTROLS = ROOT / "tests" / "judge-calibration" / "controls"


def header_of(path: Path) -> str:
    """Everything before the first turn, blockquote markers stripped and
    whitespace collapsed. Two earlier versions of this failed for the wrong
    reason: a fixed character slice truncated the longer header, then a literal
    substring missed a phrase that happened to wrap across a line."""
    head = path.read_text().split("\n## Turn", 1)[0]
    return re.sub(r"\s+", " ", head.replace(">", " "))


def test_negative_controls_exist():
    """At least two. One is an anecdote; two is a check you can act on."""
    assert len(list(CONTROLS.glob("*.md"))) >= 2


@pytest.mark.parametrize("path", sorted(CONTROLS.glob("*.md")), ids=lambda p: p.name)
def test_controls_are_marked_synthetic(path):
    """These are hand-edited, not harness output. If one ever drifts into
    runs/ or gets read as a real run, its numbers become fiction."""
    head = header_of(path)
    assert "SYNTHETIC" in head
    assert "supposed to PASS" in head
    assert not path.is_relative_to(RUNS)


@pytest.mark.parametrize("path", sorted(CONTROLS.glob("*.md")), ids=lambda p: p.name)
def test_controls_say_which_rubrics_they_control(path):
    """A control that doesn't name its scope invites over-reading: these are
    clean on the named rubrics only, not clean overall."""
    assert "NOT controlled for" in header_of(path)


def test_controls_are_not_picked_up_as_corpus_runs():
    assert all(not p.is_relative_to(CONTROLS) for p in judge_files())
