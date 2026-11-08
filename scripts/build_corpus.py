"""Build the portable evidence file from the existing RAG project."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    destination = Path(__file__).resolve().parents[1] / "references"
    destination.mkdir(exist_ok=True)
    manifest = json.loads((project / "rag/build_manifest.json").read_text(encoding="utf-8"))
    source = project / "参考文献/完整逐字稿github.md"
    expected = manifest["inputs"]["canonical_markdown"]["sha256"]
    if digest(source) != expected:
        raise SystemExit("Canonical manuscript changed; rebuild the RAG evidence first")
    raw = project / "rag/data/paragraphs.jsonl"
    if digest(raw) != manifest["outputs"]["data/paragraphs.jsonl"]:
        raise SystemExit("RAG paragraphs differ from their build manifest")
    rows = [json.loads(line) for line in raw.read_text(encoding="utf-8").splitlines()]
    turns = {row["turn_id"]: row for row in rows if row["kind"] == "turn"}
    output = destination / "evidence.jsonl"
    count = 0
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            if row["kind"] not in {"turn", "body"} or not row["speaker"]:
                continue
            parent = turns.get(row["turn_id"], row)
            record = {
                "id": row["evidence_id"],
                "order": row["order"],
                "speaker": row["speaker"],
                "time": row["display_timestamp"] or parent.get("display_timestamp"),
                "time_scope": "turn_start" if row["kind"] == "body" else "display_anchor",
                "line": row["source"]["line_start"],
                "turn": row["turn_id"],
                "text": row["text"],
                "audio_status": row["audio"]["status"],
                "alignment": row["alignment_status"],
            }
            stream.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            count += 1
    shutil.copyfile(source, destination / "transcript.md")
    meta = {
        "source_sha256": expected,
        "evidence_sha256": digest(output),
        "evidence_rows": count,
        "source": "参考文献/完整逐字稿github.md",
        "source_policy": "Canonical manuscript supplies wording; RAG alignment supplies speaker and location metadata.",
    }
    (destination / "provenance.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
