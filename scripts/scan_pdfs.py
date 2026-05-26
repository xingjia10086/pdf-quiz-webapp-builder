#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def read_page_count(path: Path) -> tuple[int, str | None]:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return len(reader.pages), None
    except Exception as exc:
        return 0, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory PDF files for quiz extraction.")
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--out", type=Path, default=Path("quiz_work"))
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in sorted(args.input_dir.rglob("*.pdf")):
        pages, error = read_page_count(path)
        rows.append(
            {
                "path": str(path),
                "relative_path": str(path.relative_to(args.input_dir)),
                "pages": pages,
                "error": error,
            }
        )

    summary = {
        "input_dir": str(args.input_dir),
        "pdf_count": len(rows),
        "page_count": sum(row["pages"] for row in rows),
        "error_count": sum(1 for row in rows if row["error"]),
        "files": rows,
    }
    (args.out / "pdf_inventory.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("pdf_count", "page_count", "error_count")}, ensure_ascii=False))
    return 0 if summary["error_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
