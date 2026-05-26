#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
from pathlib import Path


QUESTION_RE = re.compile(r"(?m)^\s*(?:Q(?:uestion)?\s*)?(\d{1,4})[\.)、:]?\s+(.+)$|^\s*第\s*(\d{1,4})\s*[題题][\.:：]?\s*(.+)$")
OPTION_RE = re.compile(r"(?m)^\s*[\(\[]?([A-J])[\)\].、:]?\s+(.+?)(?=^\s*[\(\[]?[A-J][\)\].、:]?\s+|\Z)", re.S)
ANSWER_RE = re.compile(r"(?:^|\s)(?:Q(?:uestion)?\s*)?(\d{1,4})[\.)、:]?\s*([A-J])(?:\s|$)|第\s*(\d{1,4})\s*[題题][\s:：]*([A-J])", re.I)


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_pages(path: Path) -> list[str]:
    try:
        import pdfplumber

        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                pages.append(clean_text(page.extract_text(x_tolerance=1, y_tolerance=3) or ""))
        return pages
    except Exception:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return [clean_text(page.extract_text() or "") for page in reader.pages]


def stable_id(source_file: str, page: int, number: str, question: str) -> str:
    seed = f"{source_file}|{page}|{number}|{question[:80]}"
    return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:16]


def infer_style(text: str) -> str:
    lower = text.lower()
    if any(word in lower for word in ["land search", "register", "attachment", "annex"]):
        return "land_search"
    if any(word in lower for word in ["case", "scenario", "situation"]):
        return "case"
    if re.search(r"\$|%|\bcalculate\b|\bamount\b", lower):
        return "calculation"
    return "independent"


def parse_answers(all_text: str) -> dict[str, str]:
    answers = {}
    for match in ANSWER_RE.finditer(all_text):
        number = match.group(1) or match.group(3)
        letter = match.group(2) or match.group(4)
        if number and letter:
            answers[number] = letter.upper()
    return answers


def parse_questions(source_file: str, page_number: int, page_text: str, answers: dict[str, str]) -> list[dict]:
    starts = list(QUESTION_RE.finditer(page_text))
    rows = []
    for index, match in enumerate(starts):
        number = match.group(1) or match.group(3)
        first_line = (match.group(2) or match.group(4) or "").strip()
        end = starts[index + 1].start() if index + 1 < len(starts) else len(page_text)
        block = clean_text(first_line + "\n" + page_text[match.end() : end])
        options = {m.group(1).upper(): clean_text(m.group(2)) for m in OPTION_RE.finditer(block)}
        question_text = clean_text(OPTION_RE.split(block)[0]) if options else block
        if len(question_text) < 8 or len(options) < 2:
            continue
        answer = answers.get(number, "")
        rows.append(
            {
                "id": stable_id(source_file, page_number, number, question_text),
                "exam_type": "shared",
                "exam_part": "part1",
                "chapter": "Unclassified",
                "question_style": infer_style(block),
                "source_kind": "pdf",
                "source_file": source_file,
                "source_page": page_number,
                "question_number": number,
                "question": question_text,
                "options": options,
                "answer": answer,
                "has_answer": bool(answer and answer in options),
                "explanation": "",
                "attachment_title": "",
                "attachment_text": "",
                "tags": [],
            }
        )
    return rows


def build(input_dir: Path) -> list[dict]:
    questions = []
    for path in sorted(input_dir.rglob("*.pdf")):
        pages = extract_pdf_pages(path)
        all_text = "\n".join(pages)
        answers = parse_answers(all_text)
        for page_index, page_text in enumerate(pages, start=1):
            questions.extend(parse_questions(path.name, page_index, page_text, answers))
    return questions


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a starter JSON question bank from PDFs.")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--out", type=Path, default=Path("quiz_work"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    questions = build(args.input_dir)
    (args.out / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"questions": len(questions), "with_answers": sum(1 for q in questions if q["has_answer"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
