/* ─── Global Helpers ─────────────────────────────────── */

/** Mobile nav toggle */
function toggleNav() {
  const menu = document.getElementById("mobileMenu");
  if (menu) menu.classList.toggle("open");
}

/** Option button selection (radio-style) */
function selectOption(btn, group) {
  document.querySelectorAll(`[onclick*="'${group}'"]`).forEach(b => b.classList.remove("active"));
  btn.classList.add("active");

  // Store selected value on window for easy retrieval
  const key = "selected" + group.charAt(0).toUpperCase() + group.slice(1);
  window[key] = btn.dataset.value;
}

/** Show/hide loading state on a button */
function setLoading(btn, loading) {
  if (!btn) return;
  const textEl = btn.querySelector(".btn-text");
  const loadEl = btn.querySelector(".btn-loading");
  btn.disabled = loading;
  if (textEl) textEl.classList.toggle("hidden", loading);
  if (loadEl) loadEl.classList.toggle("hidden", !loading);
}

/** Show result content */
function showResult(text) {
  const area = document.getElementById("resultArea");
  const content = document.getElementById("resultContent");
  if (!area || !content) return;
  content.innerHTML = parseMarkdown(text);
  area.classList.remove("hidden");
}

/** Show error message */
function showError(msg) {
  const el = document.getElementById("errorArea");
  if (!el) return;
  el.textContent = msg;
  el.classList.remove("hidden");
}

/** Clear results and errors */
function clearResults() {
  const resultArea = document.getElementById("resultArea");
  const errorArea = document.getElementById("errorArea");
  if (resultArea) resultArea.classList.add("hidden");
  if (errorArea) errorArea.classList.add("hidden");
}

/** Copy result text to clipboard */
function copyResult() {
  const content = document.getElementById("resultContent");
  if (!content) return;
  navigator.clipboard.writeText(content.innerText).then(() => {
    const btn = document.querySelector(".copy-btn");
    if (btn) {
      btn.textContent = "Copied!";
      setTimeout(() => btn.textContent = "Copy", 2000);
    }
  });
}

/* ─── Basic Markdown Parser ──────────────────────────── */
function parseMarkdown(text) {
  // Bold
  text = text.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  // Italic
  text = text.replace(/\*(.+?)\*/g, "<em>$1</em>");
  // Code
  text = text.replace(/`(.+?)`/g, "<code>$1</code>");
  // H1
  text = text.replace(/^# (.+)$/gm, "<h1>$1</h1>");
  // H2
  text = text.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  // H3
  text = text.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  // Unordered list items
  text = text.replace(/^\s*[-*] (.+)$/gm, "<li>$1</li>");
  text = text.replace(/(<li>.*<\/li>\n?)+/g, s => `<ul>${s}</ul>`);
  // Numbered list items
  text = text.replace(/^\s*\d+\. (.+)$/gm, "<li>$1</li>");
  // Horizontal rule
  text = text.replace(/^---+$/gm, "<hr>");
  // Paragraphs (double newline)
  text = text.split(/\n{2,}/).map(block => {
    block = block.trim();
    if (!block) return "";
    if (block.startsWith("<h") || block.startsWith("<ul") || block.startsWith("<ol") || block.startsWith("<hr")) return block;
    return `<p>${block.replace(/\n/g, "<br>")}</p>`;
  }).join("\n");

  return text;
}
