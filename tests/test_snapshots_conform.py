"""Every committed snapshot must conform to the schemas — except the mess
each snapshot deliberately carries, declared in its .schema-exceptions file.

Failure modes caught:
  * fixture rot: a snapshot drifts out of schema (plugin changed, fixture didn't)
  * mess rot: a deliberate violation silently disappears, so the journey that
    exists to exercise it stops testing anything
"""
from pathlib import Path

import pytest

from validate_userdata import validate_tree

SNAPSHOT_ROOT = Path(__file__).resolve().parent / "snapshots"
SNAPSHOTS = sorted(p.name for p in SNAPSHOT_ROOT.iterdir() if p.is_dir())


def load_exceptions(snapshot: Path) -> set[tuple[str, str]]:
    f = snapshot / ".schema-exceptions"
    if not f.exists():
        return set()
    pairs = set()
    for line in f.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            path, rule = [s.strip() for s in line.split("::")]
            pairs.add((path, rule))
    return pairs


@pytest.mark.parametrize("name", SNAPSHOTS)
def test_snapshot_conforms(name):
    snapshot = SNAPSHOT_ROOT / name
    expected = load_exceptions(snapshot)
    actual = {(f.path, f.rule) for f in validate_tree(snapshot)}
    unexpected = actual - expected
    missing_mess = expected - actual
    assert not unexpected, f"schema drift in {name}: {sorted(unexpected)}"
    assert not missing_mess, f"deliberate mess missing from {name}: {sorted(missing_mess)}"
