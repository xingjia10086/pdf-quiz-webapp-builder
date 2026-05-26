# QA Checklist

Run this checklist before delivering a generated quiz app.

## Data QA

- PDF count matches the inventory.
- Every question has stable `id`, `source_file`, and `source_page`.
- No duplicate question ids.
- Options are complete and readable.
- Answers point to existing options.
- Missing answers are marked as `has_answer: false`.
- Existing source explanations are attached.
- Missing source explanations are clearly labeled.
- Attachment/case/table questions display the needed source text.
- Garbled text count is reviewed and either fixed or documented.

## Product QA

- The app loads offline/static from a local server.
- Filters work.
- Answer feedback shows correct answer and source citation.
- Mistake book updates.
- Mock exam starts, scores, and finishes.
- Progress survives refresh.
- 390px and 360px mobile widths have no horizontal overflow.
- Long questions and long options wrap cleanly.

## Deployment QA

- Do not deploy private PDFs or raw work files.
- Deploy only the generated static site or approved backend.
- Check `data/questions.json` and `data/stats.json` on the live URL.
- Smoke-test one real answer submission if cloud sync is enabled.
