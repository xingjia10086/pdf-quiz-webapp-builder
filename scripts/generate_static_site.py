#!/usr/bin/env python3
import argparse
import json
import shutil
from collections import Counter
from pathlib import Path


def stats(questions: list[dict]) -> dict:
    return {
        "total": len(questions),
        "with_answers": sum(1 for q in questions if q.get("has_answer")),
        "by_exam_type": dict(Counter(q.get("exam_type", "shared") for q in questions)),
        "by_exam_part": dict(Counter(q.get("exam_part", "part1") for q in questions)),
        "by_chapter": dict(Counter(q.get("chapter", "Unclassified") for q in questions)),
        "by_question_style": dict(Counter(q.get("question_style", "independent") for q in questions)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a static quiz site from questions.json.")
    parser.add_argument("questions_json", type=Path)
    parser.add_argument("site_dir", type=Path)
    args = parser.parse_args()

    template_dir = Path(__file__).resolve().parents[1] / "assets" / "frontend-template"
    if args.site_dir.exists():
        shutil.rmtree(args.site_dir)
    shutil.copytree(template_dir, args.site_dir)

    questions = json.loads(args.questions_json.read_text(encoding="utf-8"))
    data_dir = args.site_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    (data_dir / "stats.json").write_text(json.dumps(stats(questions), ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"site_dir": str(args.site_dir), "questions": len(questions)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
