const state = {
  questions: [],
  pool: [],
  index: 0,
  selected: "",
  answered: false,
  progress: JSON.parse(localStorage.getItem("quiz_progress_v1") || "{}"),
};

const $ = (id) => document.getElementById(id);

function saveProgress() {
  localStorage.setItem("quiz_progress_v1", JSON.stringify(state.progress));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function optionList(id, label, values) {
  $(id).innerHTML = `<option value="">${label}</option>` + values.map((value) => `<option>${escapeHtml(value)}</option>`).join("");
}

function fillFilters() {
  optionList("exam-filter", "All exams", unique(state.questions.map((q) => q.exam_type || "shared")));
  optionList("part-filter", "All parts", unique(state.questions.map((q) => q.exam_part || "part1")));
  optionList("chapter-filter", "All chapters", unique(state.questions.map((q) => q.chapter || "Unclassified")));
}

function filtered() {
  const exam = $("exam-filter").value;
  const part = $("part-filter").value;
  const chapter = $("chapter-filter").value;
  const mode = $("mode-filter").value;
  return state.questions.filter((q) => {
    const rec = state.progress[q.id];
    if (exam && q.exam_type !== exam) return false;
    if (part && q.exam_part !== part) return false;
    if (chapter && q.chapter !== chapter) return false;
    if (mode === "unseen" && rec?.seen) return false;
    if (mode === "mistakes" && !rec?.wrong) return false;
    return true;
  });
}

function shuffle(items) {
  return [...items].sort(() => Math.random() - 0.5);
}

function buildPool() {
  state.pool = shuffle(filtered());
  state.index = 0;
  render();
  updateStats();
}

function render() {
  const q = state.pool[state.index];
  state.selected = "";
  state.answered = false;
  $("feedback").classList.add("hidden");
  $("feedback").classList.remove("bad");
  if (!q) {
    $("question-index").textContent = "0 / 0";
    $("question-source").textContent = "";
    $("question-text").textContent = "No questions match the current filters.";
    $("options").innerHTML = "";
    $("attachment").classList.add("hidden");
    return;
  }
  $("question-index").textContent = `${state.index + 1} / ${state.pool.length}`;
  $("question-source").textContent = `${q.source_file || "source"} p.${q.source_page || "?"}`;
  $("question-text").textContent = q.question;
  if (q.attachment_text) {
    $("attachment").textContent = q.attachment_text;
    $("attachment").classList.remove("hidden");
  } else {
    $("attachment").classList.add("hidden");
  }
  $("options").innerHTML = Object.entries(q.options || {})
    .map(([letter, text]) => `<button class="option" data-letter="${letter}"><span>${letter}</span><span>${escapeHtml(text)}</span></button>`)
    .join("");
  document.querySelectorAll(".option").forEach((button) => {
    button.addEventListener("click", () => {
      if (state.answered) return;
      state.selected = button.dataset.letter;
      document.querySelectorAll(".option").forEach((item) => item.classList.remove("selected"));
      button.classList.add("selected");
    });
  });
}

function submit() {
  const q = state.pool[state.index];
  if (!q || !state.selected || state.answered) return;
  state.answered = true;
  const rec = state.progress[q.id] || { seen: 0, correct: 0, wrong: 0 };
  const canJudge = !!q.has_answer;
  const correct = canJudge && state.selected === q.answer;
  rec.seen += 1;
  if (canJudge && correct) rec.correct += 1;
  if (canJudge && !correct) rec.wrong += 1;
  state.progress[q.id] = rec;
  saveProgress();
  document.querySelectorAll(".option").forEach((button) => {
    if (button.dataset.letter === q.answer) button.classList.add("correct");
    if (button.dataset.letter === state.selected && canJudge && !correct) button.classList.add("wrong");
  });
  $("feedback").classList.remove("hidden");
  $("feedback").classList.toggle("bad", canJudge && !correct);
  $("feedback").innerHTML = `
    <strong>${canJudge ? (correct ? "Correct." : `Wrong. Correct answer: ${q.answer}.`) : "No confirmed answer in source."}</strong>
    <p>${q.explanation ? escapeHtml(q.explanation) : "No source explanation was attached."}</p>
    <small>${escapeHtml(q.source_file || "source")} p.${q.source_page || "?"}</small>
  `;
  updateStats();
}

function updateStats() {
  const records = Object.values(state.progress);
  const done = records.reduce((sum, item) => sum + item.seen, 0);
  const correct = records.reduce((sum, item) => sum + item.correct, 0);
  $("done-count").textContent = `${done} done`;
  $("accuracy").textContent = `${done ? Math.round((correct / done) * 100) : 0}%`;
}

function move(delta) {
  if (!state.pool.length) return;
  state.index = (state.index + delta + state.pool.length) % state.pool.length;
  render();
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

async function init() {
  const response = await fetch("./data/questions.json");
  state.questions = await response.json();
  fillFilters();
  buildPool();
  ["exam-filter", "part-filter", "chapter-filter", "mode-filter"].forEach((id) => $(id).addEventListener("change", buildPool));
  $("shuffle").addEventListener("click", buildPool);
  $("submit").addEventListener("click", submit);
  $("prev").addEventListener("click", () => move(-1));
  $("next").addEventListener("click", () => move(1));
}

init().catch((error) => {
  $("question-text").textContent = "Failed to load questions.json.";
  console.error(error);
});
