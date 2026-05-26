# PDF Quiz Webapp Builder

**PDF Quiz Webapp Builder** is a Codex Skill and starter toolkit for turning exam-prep PDFs into a mobile-ready quiz website.

It helps an AI coding agent follow a repeatable production workflow: scan PDF folders, extract questions, preserve source citations, audit data quality, generate a static study app, and validate the result on mobile screens.

> This repository contains only generic open-source tooling, sample data, and templates. It does not include any private PDFs, paid question banks, customer codes, API keys, or deployment secrets.

## What It Builds

The default generated app is a static quiz site with:

- Question practice from `data/questions.json`
- Exam, part, chapter, and mode filters
- Answer submission and instant feedback
- Correct-answer highlighting
- Source PDF and page citation
- Optional attachment/case text display
- Local progress tracking
- Mistake-focused practice mode
- Responsive mobile layout

The Skill can also guide a more advanced build with cloud sync, customer login, admin panels, or deployment, but those features should be added only after the extracted question bank passes QA.

## Case Study: exam.xingjia.xyz

`exam.xingjia.xyz` is a real mobile-first exam practice product built from the same workflow this Skill captures: PDF inventory, question extraction, answer/explanation matching, QA, responsive UI, customer-code access, and cloud progress sync.

The screenshot below shows the real mobile practice interface, including learning stats, modes, filters, a question card, options, and answer controls.

![Mobile functional screenshot for exam.xingjia.xyz](assets/case-studies/exam-xingjia-functional.jpg)

With this Skill, a new PDF-based exam pack can follow the same path:

- Convert PDF folders into a structured question bank.
- Preserve source PDF/page evidence for every question.
- Surface attachment/case material inside the quiz UI.
- Generate a mobile-ready study website.
- Add commercial features such as customer login, admin management, and sync after the data passes QA.

## Repository Contents

```text
pdf-quiz-webapp-builder/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── extraction_rules.md
│   └── qa_checklist.md
├── scripts/
│   ├── scan_pdfs.py
│   ├── build_question_bank.py
│   ├── audit_question_bank.py
│   └── generate_static_site.py
└── assets/
    └── frontend-template/
```

## Quick Start

Install optional Python dependencies:

```bash
pip install pypdf pdfplumber
```

Scan a folder of PDFs:

```bash
python scripts/scan_pdfs.py ./my-pdfs --out ./quiz_work
```

Build a starter question bank:

```bash
python scripts/build_question_bank.py ./my-pdfs --out ./quiz_work
```

Audit the extracted questions:

```bash
python scripts/audit_question_bank.py ./quiz_work/questions.json --out ./quiz_work/qa_report.json
```

Generate a static quiz site:

```bash
python scripts/generate_static_site.py ./quiz_work/questions.json ./site_out
```

Preview locally:

```bash
cd site_out
python -m http.server 8000
```

Then open `http://127.0.0.1:8000`.

## Expected Question Schema

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
  "options": {
    "A": "Option A",
    "B": "Option B"
  },
  "answer": "A",
  "has_answer": true,
  "explanation": "Optional source explanation",
  "attachment_title": "Optional attachment title",
  "attachment_text": "Optional attachment text",
  "tags": ["keyword"]
}
```

## Quality Philosophy

PDF-to-quiz work fails when extraction is treated as a one-step conversion. This project is designed around a safer workflow:

1. Count every PDF before parsing.
2. Keep page-level source evidence.
3. Separate answer-key detection from question extraction.
4. Attach explanations only when the source mapping is reliable.
5. Preserve attachments, case data, land-search text, and tables.
6. Audit before building the app.
7. Test the generated site on mobile widths such as 390px and 360px.

## Using as a Codex Skill

Copy this repository folder into your Codex skills directory, for example:

```text
~/.codex/skills/pdf-quiz-webapp-builder
```

Then ask Codex:

```text
Use $pdf-quiz-webapp-builder to turn this folder of exam PDFs into a mobile-ready quiz website.
```

## Limitations

The included parser is intentionally conservative. Real-world exam PDFs often require project-specific parser improvements for:

- Multi-column layouts
- Scanned/OCR-only pages
- Answer tables split across pages
- Explanations stored in separate PDFs
- Non-standard option labels
- Case-study attachments and tables
- Domain-specific exam categories

Treat the scripts as a reliable starter pipeline, not a magic one-click extractor.

## Security and Privacy

Do not commit:

- Source PDFs from paid/private courses
- Extracted private question banks
- Student/customer data
- Access codes
- Supabase/Vercel/API secrets
- Generated production data files

The `.gitignore` is configured to avoid common accidental leaks, but you should still inspect `git status` before publishing.

## License

MIT

---

# PDF 刷题网站生成器

**PDF Quiz Webapp Builder** 是一个 Codex Skill 和开源工具包，用来把考试复习 PDF 转成适合手机访问的刷题网站。

它的目标不是简单地“把 PDF 转 JSON”，而是让 AI 编程助手按一套稳定流程交付产品：扫描 PDF、提取题目、保留原文出处、做数据质检、生成静态刷题网站，并完成移动端验证。

> 本仓库只包含通用开源工具、样例数据和模板。不包含任何私有 PDF、付费题库、客户访问码、API Key 或部署密钥。

## 可以生成什么

默认生成的是一个静态刷题网站，包含：

- 从 `data/questions.json` 读取题库
- 按考试、部分、章节、模式筛选
- 提交答案并即时反馈
- 高亮正确答案
- 显示来源 PDF 和页码
- 显示附件题 / 案例题原文
- 本地学习进度
- 错题练习模式
- 适配手机端的响应式布局

如果需要更商业化的版本，也可以在静态网站稳定之后继续扩展云端同步、客户码登录、管理后台和线上部署。

## 案例网站：exam.xingjia.xyz

`exam.xingjia.xyz` 是一个真实的手机端考试刷题产品，使用的正是这个 Skill 沉淀出来的流程：PDF 清单扫描、题库提取、答案/解析匹配、质量检查、响应式网页、客户码访问和云端进度同步。

下面的截图展示真实手机端刷题界面，包括学习统计、训练模式、筛选器、题目卡片、选项和答题控制。

![exam.xingjia.xyz 手机端真实功能截图](assets/case-studies/exam-xingjia-functional.jpg)

通过这个 Skill，新的 PDF 考试资料包可以复用同样的路径：

- 把 PDF 文件夹转成结构化题库。
- 为每道题保留来源 PDF 和页码证据。
- 在答题界面展示附件题 / 案例题原文。
- 生成手机端可用的刷题网站。
- 数据质检通过后，再扩展客户登录、后台管理和云端同步等商业功能。

## 仓库结构

```text
pdf-quiz-webapp-builder/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── extraction_rules.md
│   └── qa_checklist.md
├── scripts/
│   ├── scan_pdfs.py
│   ├── build_question_bank.py
│   ├── audit_question_bank.py
│   └── generate_static_site.py
└── assets/
    └── frontend-template/
```

## 快速开始

安装可选 Python 依赖：

```bash
pip install pypdf pdfplumber
```

扫描 PDF 文件夹：

```bash
python scripts/scan_pdfs.py ./my-pdfs --out ./quiz_work
```

生成初版题库：

```bash
python scripts/build_question_bank.py ./my-pdfs --out ./quiz_work
```

检查题库质量：

```bash
python scripts/audit_question_bank.py ./quiz_work/questions.json --out ./quiz_work/qa_report.json
```

生成静态刷题网站：

```bash
python scripts/generate_static_site.py ./quiz_work/questions.json ./site_out
```

本地预览：

```bash
cd site_out
python -m http.server 8000
```

然后打开 `http://127.0.0.1:8000`。

## 数据质量原则

PDF 题库项目最容易出问题的地方，不是网页，而是提取质量。本项目强调：

1. 先统计所有 PDF，防止漏题。
2. 每道题保留 PDF 文件名和页码。
3. 题目提取和答案表匹配分开处理。
4. 只有来源可靠时才绑定解析。
5. 附件、案例、土地查册、表格内容不能丢。
6. 先跑 QA，再生成网站。
7. 必须检查 390px / 360px 手机宽度下是否横向溢出。

## 作为 Codex Skill 使用

把仓库复制到 Codex skills 目录，例如：

```text
~/.codex/skills/pdf-quiz-webapp-builder
```

然后对 Codex 说：

```text
Use $pdf-quiz-webapp-builder to turn this folder of exam PDFs into a mobile-ready quiz website.
```

或者中文：

```text
用 $pdf-quiz-webapp-builder，把这个文件夹里的考试 PDF 做成手机端可用的刷题网站。
```

## 局限性

内置解析脚本是保守的通用起点。真实 PDF 经常需要针对具体资料调整：

- 多栏排版
- 扫描版 / OCR 页面
- 答案表跨页
- 解析和题目分布在不同 PDF
- 非标准选项编号
- 案例题附件和表格
- 具体考试的小牌 / 大牌 / 章节分类规则

所以它不是“一键万能转换器”，而是一套可靠的起步流水线。

## 安全和隐私

不要提交：

- 付费课程或私有资料 PDF
- 提取后的私有题库
- 学员 / 客户数据
- 访问码
- Supabase、Vercel 或其他 API 密钥
- 真实生产环境生成的数据文件

`.gitignore` 已经屏蔽常见敏感文件，但发布前仍然应该检查 `git status`。

## 开源协议

MIT
