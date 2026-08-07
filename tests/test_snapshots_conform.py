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
    for raw_line in f.read_text().splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = [s.strip() for s in line.split("::")]
        if len(parts) != 2:
            raise ValueError(
                f"{f}: exceptions line missing '::' separator: {raw_line!r} "
                "(expected '<path> :: <rule>')")
        path, rule = parts
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


def test_load_exceptions_missing_separator_raises_readable_error(tmp_path):
    snapshot = tmp_path / "some-snapshot"
    snapshot.mkdir()
    exceptions = snapshot / ".schema-exceptions"
    exceptions.write_text("companies/Plaid/meta.md meta.status-enum\n")
    with pytest.raises(ValueError) as exc_info:
        load_exceptions(snapshot)
    message = str(exc_info.value)
    assert str(exceptions) in message
    assert "companies/Plaid/meta.md meta.status-enum" in message
