"""Offline, dependency-free retrieval over the podcast's verified evidence rows."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "references"
STOP = {"什么", "怎么", "如何", "是否", "一个", "这个", "那个", "他们", "我们", "你们", "就是", "然后", "觉得", "认为", "关于", "有没有", "问题", "观点", "说过", "提到", "播客", "访谈", "孙宇晨", "邵艾伦"}


def tokens(value: str) -> set[str]:
    value = value.lower()
    terms = set(re.findall(r"[a-z][a-z0-9+.-]{1,}|\d+(?:\.\d+)?", value))
    for segment in re.findall(r"[\u3400-\u9fff]+", value):
        terms.update(segment[i:i+2] for i in range(len(segment) - 1))
        if len(segment) >= 4:
            terms.update(segment[i:i+3] for i in range(len(segment) - 2))
    return {term for term in terms if term not in STOP}


def load() -> list[dict]:
    meta = json.loads((DATA / "provenance.json").read_text(encoding="utf-8"))
    source_hash = hashlib.sha256((DATA / "transcript.md").read_bytes()).hexdigest().upper()
    evidence_hash = hashlib.sha256((DATA / "evidence.jsonl").read_bytes()).hexdigest().upper()
    if source_hash != meta["source_sha256"] or evidence_hash != meta["evidence_sha256"]:
        raise SystemExit("Evidence integrity check failed; use an unmodified Skill package")
    lines = (DATA / "transcript.md").read_text(encoding="utf-8").splitlines()
    rows = [json.loads(line) for line in (DATA / "evidence.jsonl").read_text(encoding="utf-8").splitlines()]
    for row in rows:
        if row["text"] not in lines[row["line"] - 1]:
            raise SystemExit(f"Evidence text differs from manuscript at line {row['line']}")
    return rows


def search(rows: list[dict], query: str, limit: int, speaker: str | None = None) -> list[dict]:
    query_terms = tokens(query)
    if not query_terms:
        return []
    docs = [tokens(row["text"]) for row in rows]
    df = Counter(term for doc in docs for term in doc)
    scored = []
    n = len(rows)
    for row, doc in zip(rows, docs):
        if speaker and row["speaker"] != speaker:
            continue
        common = query_terms & doc
        if not common:
            continue
        weight = sum(math.log1p((n - df[t] + 0.5) / (df[t] + 0.5)) for t in common)
        coverage = len(common) / len(query_terms)
        score = weight * (0.45 + 0.55 * coverage) / (1 + max(0, len(row["text"]) - 260) / 1200)
        if query.lower() in row["text"].lower():
            score *= 1.35
        scored.append((score, row, len(common) / len(query_terms)))
    scored.sort(key=lambda item: (-item[0], item[1]["order"]))
    # Prevent long turns from filling the shortlist with adjacent body paragraphs.
    selected, seen = [], set()
    for score, row, coverage in scored:
        if row["turn"] in seen:
            continue
        seen.add(row["turn"])
        selected.append({**row, "score": round(score, 3), "term_coverage": round(coverage, 3)})
        if len(selected) == limit:
            break
    return selected


def format_rows(rows: list[dict], full: bool) -> list[dict]:
    result = []
    for row in rows:
        clean = {key: row[key] for key in ("id", "speaker", "time", "time_scope", "line", "audio_status", "alignment", "score", "term_coverage") if key in row}
        clean["text"] = row["text"] if full or len(row["text"]) <= 420 else row["text"][:420] + "…"
        result.append(clean)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("search", "compare", "connect"):
        command = sub.add_parser(action)
        command.add_argument("query")
        if action == "connect":
            command.add_argument("second_query")
        command.add_argument("--limit", type=int, default=6)
        command.add_argument("--full", action="store_true")
    context = sub.add_parser("context")
    context.add_argument("evidence_id")
    context.add_argument("--radius", type=int, default=2)
    args = parser.parse_args()
    rows = load()
    if args.action == "search":
        result = {"query": args.query, "results": format_rows(search(rows, args.query, args.limit), args.full)}
    elif args.action == "compare":
        result = {"query": args.query, "by_speaker": {name: format_rows(search(rows, args.query, args.limit, name), args.full) for name in ("邵艾伦", "孙宇晨")}}
    elif args.action == "connect":
        first = search(rows, args.query, args.limit)
        second = search(rows, args.second_query, args.limit)
        result = {"themes": [args.query, args.second_query], "first": format_rows(first, args.full), "second": format_rows(second, args.full)}
        pairs = []
        for left in first:
            for right in second:
                if left["id"] == right["id"]:
                    continue
                gap = abs(left["order"] - right["order"])
                pairs.append((gap, left["id"], right["id"]))
        result["closest_pair"] = {"order_gap": pairs[0][0], "evidence_ids": list(pairs[0][1:])} if pairs and (pairs := sorted(pairs)) else None
    else:
        index = next((i for i, row in enumerate(rows) if row["id"] == args.evidence_id), None)
        if index is None:
            raise SystemExit("Evidence ID not found")
        result = {"context": format_rows(rows[max(0, index - args.radius):index + args.radius + 1], True)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
