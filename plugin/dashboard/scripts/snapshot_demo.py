"""Snapshot a persona's userdata/ into a static JSON bundle for the demo build.

Imports the parsing helpers from `serve.py` and writes JSON/markdown files
matching the exact shape the live HTTP API returns, so the demo bundle's
frontend can swap fetch() calls for static-file loads.

Output layout (under --out):
    state.json                              # /api/state payload
    artifacts/<folder_path>.json            # one per position
    notes/<folder_path>.md                  # raw notes.md content (or empty)

folder_path uses literal slashes ("Anthropic" or "Anthropic/product-manager")
so the frontend can compute the URL as ${BASE_URL}demo/artifacts/${folderPath}.json
without URL-encoding.

Usage:
    python plugin/dashboard/scripts/snapshot_demo.py \\
        --persona maya \\
        --out plugin/dashboard/public/demo/
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Make `serve` importable when running this script directly.
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR.parent))

from serve import (  # noqa: E402
    collect_artifacts,
    collect_companies,
    compute_weekly_progress,
    latest_brief,
    read_strategy,
)


def build_snapshot(
    persona_root: Path,
    out_root: Path,
    today: date,
) -> dict[str, int]:
    """Walk persona_root, write JSON/markdown into out_root. Return counts dict."""
    if not (persona_root / "companies").is_dir():
        raise FileNotFoundError(f"no companies/ under {persona_root}")

    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "artifacts").mkdir(exist_ok=True)
    (out_root / "notes").mkdir(exist_ok=True)

    companies = collect_companies(persona_root)
    state_payload = {
        "companies": companies,
        "strategy": read_strategy(persona_root),
        "weekly_progress": compute_weekly_progress(persona_root, companies, today=today),
        "latest_brief": latest_brief(persona_root),
        # Hide the real on-disk path from the public bundle.
        "userdata_root": f"<demo: {persona_root.name}>",
    }
    (out_root / "state.json").write_text(
        json.dumps(state_payload, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    artifact_count = 0
    notes_count = 0
    for record in companies:
        folder_path = record["folder_path"]
        meta_dir = persona_root / "companies" / folder_path

        artifact_target = out_root / "artifacts" / f"{folder_path}.json"
        artifact_target.parent.mkdir(parents=True, exist_ok=True)
        artifact_target.write_text(
            json.dumps(collect_artifacts(meta_dir), indent=2) + "\n",
            encoding="utf-8",
        )
        artifact_count += 1

        notes_path = meta_dir / "notes.md"
        notes_md = notes_path.read_text(encoding="utf-8") if notes_path.is_file() else ""
        notes_target = out_root / "notes" / f"{folder_path}.md"
        notes_target.parent.mkdir(parents=True, exist_ok=True)
        notes_target.write_text(notes_md, encoding="utf-8")
        notes_count += 1

    return {
        "companies": len(companies),
        "artifacts": artifact_count,
        "notes": notes_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="snapshot_demo")
    parser.add_argument("--persona", default="maya")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--userdata-examples",
        type=Path,
        default=Path(__file__).resolve().parents[3] / "userdata" / "examples",
        help="Path to userdata/examples/ root. Defaults to the repo's userdata/examples/.",
    )
    # Pin "today" so the snapshot is reproducible. Default lands on the Friday
    # of Maya's most active week so the dashboard's "this week" panel is populated.
    parser.add_argument("--today", default="2026-05-15")
    args = parser.parse_args(argv)

    persona_root = (args.userdata_examples / args.persona).resolve()
    if not persona_root.is_dir():
        print(f"error: persona root not found: {persona_root}", file=sys.stderr)
        return 1

    out_root = args.out.resolve()
    today = date.fromisoformat(args.today)

    counts = build_snapshot(persona_root, out_root, today=today)
    print(
        f"snapshot ok: {counts['companies']} companies, "
        f"{counts['artifacts']} artifact files, {counts['notes']} notes files, "
        f"out={out_root}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
