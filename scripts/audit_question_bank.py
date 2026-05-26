#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter
from pathlib import Path


def looks_garbled(value: str) -> bool:
    if not value:
        return False
    if "\ufffd" in value:
        return True
    if re.search(r"(.)\1{12,}", value):
        return True
    symbols = sum(1 for ch in value if not ch.isalnum() and not ch.isspace())
    return len(value) > 40 and symbols / max(len(value), 1) > 0.45


def audit(path: Path) -> dict:
    questions = json.loads(path.read_text(encoding="utf-8"))
    ids = Counter(q.get("id") for q in questions)
    issues = []
    for index, q in enumerate(questions):
        label = q.get("id") or f"row:{index}"
        options = q.get("options") or {}
        answer = q.get("answer") or ""
        if not q.get("question"):
            issues.append({"severity": "error", "id": label, "message": "missing question text"})
        if len(options) < 2:
            issues.append({"severity": "error", "id": label, "message": "fewer than two options"})
        if answer and answer not in options:
            issues.append({"severity": "error", "id": label, "message": "answer does not match options"})
        if not q.get("source_file") or not q.get("source_page"):
            issues.append({"severity": "error", "id": label, "message": "missing source metadata"})
        for field in ("question", "explanation", "attachment_text"):
            if looks_garbled(str(q.get(field) or "")):
                issues.append({"severity": "warning", "id": label, "message": f"possible garbled text in {field}"})
    for duplicate_id, count in ids.items():
        if duplicate_id and count > 1:
            issues.append({"severity": "error", "id": duplicate_id, "message": f"duplicate id appears {count} times"})
    return {
        "question_count": len(questions),
        "with_answers": sum(1 for q in questions if q.get("has_answer")),
        "with_explanations": sum(1 for q in questions if q.get("explanation")),
        "issue_count": len(issues),
        "error_count": sum(1 for i in issues if i["severity"] == "error"),
        "warning_count": sum(1 for i in issues if i["severity"] == "warning"),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit quiz question JSON.")
    parser.add_argument("questions_json", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = audit(args.questions_json)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    print(text)
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
