# Extraction Rules

Use these rules when adapting the parser to a new PDF pack.

## Inventory first

- Count every PDF recursively.
- Record file path, page count, text length, and extraction errors.
- Do not start app generation until the final question count can be traced back to source PDFs.

## Text extraction

- Prefer `pdfplumber` when available because it handles page text and tables well.
- Fall back to `pypdf` when `pdfplumber` is unavailable.
- Keep page boundaries. Source page evidence matters more than pretty text.
- Normalize whitespace but do not destroy option labels, table rows, or attachment layout.

## Question segmentation

Common starts include:

- `1.`, `1)`, `Q1`, `Question 1`
- Chinese numbering such as `第 1 題`, `第1题`

Treat option starts as:

- `A.`, `A)`, `(A)`, `A `
- `A` through `E` by default; support `F` through `J` when detected.

## Answer keys

Search answer-key pages separately. Common patterns:

- `1 A`
- `1. A`
- `Q1: A`
- `第1題 A`

Never invent answers. If no answer key is found, keep `answer` empty and `has_answer` false.

## Explanations

Attach explanations only when source evidence is strong:

- The explanation page explicitly references the same question number.
- The explanation is adjacent to the question in the same page block.
- A source answer/explanation table clearly maps question number to text.

If uncertain, preserve the text as `attachment_text` or notes for manual review instead of pretending it is a confirmed explanation.

## Attachments and case data

Questions that say "according to attachment", "based on table", "land search", "case", or similar usually need extra source text. Capture nearby tables, title lines, and following page blocks as `attachment_text`.

## Classification

Infer fields conservatively:

- `exam_type`: target exam, paper type, folder name, or source filename. Use `shared` when uncertain.
- `exam_part`: part/section label. Use `part1` by default when unknown.
- `chapter`: folder name, PDF heading, or keyword map.
- `question_style`: `independent`, `case`, `land_search`, or `calculation`.

## Garbled text

Flag suspicious text when it contains:

- Replacement characters.
- Long repeated symbols.
- Excessive isolated Latin letters inside CJK material.
- Broken option labels or missing option text.
