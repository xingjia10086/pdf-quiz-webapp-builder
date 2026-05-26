---
name: pdf-quiz-webapp-builder
description: Build a polished quiz web app from exam-prep PDFs. Use when the user provides folders of PDF question banks and wants extracted questions, answer keys, explanations, attachments, QA checks, mobile validation, and a deployable static study site.
---

# PDF Quiz Webapp Builder

Turn PDF exam materials into a usable quiz website. The default output is a static app with question filters, answer feedback, source citations, attachment text, mistakes, mock exams, progress tracking, and mobile-ready layout.

## Safety rule

Never publish source PDFs, extracted question banks, customer codes, API keys, or paid/private materials unless the user explicitly asks and policy permits external disclosure. Open-source only generic scripts, templates, and instructions.

## Workflow

1. Inventory all PDFs.
   - Run `scripts/scan_pdfs.py <input_dir> --out <work_dir>`.
   - Confirm total PDF count, page count, unreadable files, and likely categories.

2. Extract and normalize questions.
   - Run `scripts/build_question_bank.py <input_dir> --out <work_dir>`.
   - Preserve `source_file`, `source_page`, `question`, `options`, `answer`, `explanation`, and `attachment_text`.
   - Do not silently drop pages, attachments, tables, answer-key pages, or repeated sections.

3. Audit before building the app.
   - Run `scripts/audit_question_bank.py <work_dir>/questions.json`.
   - Fix high-risk issues: empty question text, missing options, duplicate ids, invalid answers, garbled text, missing source metadata, and category drift.

4. Generate the website.
   - Run `scripts/generate_static_site.py <work_dir>/questions.json <site_dir>`.
   - The generated app reads `data/questions.json` and `data/stats.json`.

5. Browser QA.
   - Serve with `python -m http.server`.
   - Test desktop and mobile widths, especially 390px and 360px.
   - Verify login/gate if present, filters, answer submission, feedback, attachment display, mistakes, mock exam, and no horizontal overflow.

6. Deployment package.
   - Static-only output can be deployed to Vercel, Netlify, GitHub Pages, Cloudflare Pages, or any static host.
   - For multi-customer sync, add a backend such as Supabase only after the static app and extracted data pass QA.

## Extraction heuristics

Read `references/extraction_rules.md` before changing parser logic for a new exam pack. Read `references/qa_checklist.md` before final delivery.

## Expected question schema

```json
{
  "id": "source-stable-id",
  "exam_type": "shared",
  "exam_part": "part1",
  "chapter": "Unclassified",
  "question_style": "independent",
  "source_kind": "pdf",
  "source_file": "paper.pdf",
  "source_page": 12,
  "question": "Question text",
  "options": { "A": "Option A", "B": "Option B" },
  "answer": "A",
  "has_answer": true,
  "explanation": "Optional source explanation",
  "attachment_title": "Optional attachment title",
  "attachment_text": "Optional attachment text",
  "tags": ["keyword"]
}
```

## Quality bar

The first usable version should feel like a product, not a data dump:

- Mobile-first layout with no horizontal overflow.
- Every answer feedback cites the source PDF and page.
- If source explanations exist, attach them to the correct question.
- If source explanations do not exist, state that clearly.
- Mock exam scoring must match the target exam's pass rules.
- Do not claim the dataset is complete until the PDF inventory and final question count reconcile.
