"""
AI-Powered Study Buddy

"""

from flask import Flask, render_template, request, jsonify, session
import anthropic
import json
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "study-buddy-secret-2024")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/explain")
def explain_page():
    return render_template("explain.html")

@app.route("/summarize")
def summarize_page():
    return render_template("summarize.html")

@app.route("/quiz")
def quiz_page():
    return render_template("quiz.html")

@app.route("/flashcards")
def flashcards_page():
    return render_template("flashcards.html")

# ──────────────────────────────────────────────
# API Endpoints
# ──────────────────────────────────────────────

@app.route("/api/explain", methods=["POST"])
def explain():
    data = request.get_json()
    topic = data.get("topic", "").strip()
    level = data.get("level", "beginner")

    if not topic:
        return jsonify({"error": "Please enter a topic."}), 400

    level_desc = {
        "beginner": "a complete beginner (age 12-14), use simple analogies and everyday examples",
        "intermediate": "a high school student with basic knowledge",
        "advanced": "a college student or advanced learner"
    }.get(level, "a beginner")

    prompt = f"""Explain the concept of "{topic}" for {level_desc}.

Structure your response with:
1. **Simple Definition** – What is it in one sentence?
2. **Key Idea** – The core concept in plain language
3. **Real-World Analogy** – A relatable everyday comparison
4. **How It Works** – Step-by-step breakdown (3-5 points)
5. **Quick Example** – A concrete example
6. **Remember This** – One key takeaway

Use clear headings, bullet points where helpful, and avoid jargon."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"result": message.content[0].text})


@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    notes = data.get("notes", "").strip()
    style = data.get("style", "structured")

    if not notes:
        return jsonify({"error": "Please paste your notes."}), 400
    if len(notes) < 50:
        return jsonify({"error": "Notes too short. Please provide more content."}), 400

    style_instructions = {
        "structured": "Create a structured summary with clear headings, bullet points for key facts, and a 'Key Takeaways' section at the end.",
        "concise": "Write a concise paragraph summary (max 150 words) hitting only the most critical points.",
        "outline": "Convert into a clean hierarchical outline with main topics, subtopics, and supporting details."
    }.get(style, "structured")

    prompt = f"""Summarize the following study notes. {style_instructions}

Also add at the end:
- **Difficult Terms**: List any technical terms with brief definitions
- **Study Tips**: 2-3 specific tips for remembering this material

NOTES:
{notes}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return jsonify({"result": message.content[0].text})


@app.route("/api/quiz", methods=["POST"])
def generate_quiz():
    data = request.get_json()
    topic = data.get("topic", "").strip()
    num_questions = min(int(data.get("num_questions", 5)), 10)
    difficulty = data.get("difficulty", "medium")

    if not topic:
        return jsonify({"error": "Please enter a topic."}), 400

    prompt = f"""Generate {num_questions} multiple-choice quiz questions about "{topic}" at {difficulty} difficulty.

Return ONLY a valid JSON array with this exact structure (no extra text, no markdown fences):
[
  {{
    "question": "Question text here?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "answer": "A) Option 1",
    "explanation": "Brief explanation of why this is correct."
  }}
]

Rules:
- Each question must have exactly 4 options labeled A), B), C), D)
- The answer must exactly match one of the options
- Vary question types (definition, application, comparison)
- Make distractors plausible but clearly wrong upon reflection"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    # Strip markdown fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    questions = json.loads(raw)
    return jsonify({"questions": questions})


@app.route("/api/flashcards", methods=["POST"])
def generate_flashcards():
    data = request.get_json()
    content = data.get("content", "").strip()
    num_cards = min(int(data.get("num_cards", 8)), 15)

    if not content:
        return jsonify({"error": "Please enter a topic or paste your notes."}), 400

    prompt = f"""Create {num_cards} study flashcards from the following content.

Return ONLY a valid JSON array (no extra text, no markdown fences):
[
  {{
    "front": "Question or term",
    "back": "Answer or definition",
    "hint": "A one-sentence memory hint or mnemonic"
  }}
]

Content:
{content}

Rules:
- Front: clear, focused question or term
- Back: concise but complete answer (1-3 sentences max)
- Hint: a creative mnemonic, analogy, or memory trick
- Cover the most important concepts"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    cards = json.loads(raw)
    return jsonify({"flashcards": cards})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
