# AI-Powered-Study-Buddy
⚡ AI Study Buddy


An AI-powered web application that helps students understand complex concepts, summarize notes, and generate quizzes and flashcards on demand.




📌 Problem Statement

Students often struggle to understand complex academic concepts while studying independently. Traditional search engines return long, irrelevant results that require significant effort to filter. Teachers and tutors are not always available for immediate assistance. There is a clear need for a tool that can explain topics in simple terms, summarize study notes, and generate self-assessment materials on demand — without requiring prior knowledge to find the right answers.


💡 Proposed System / Solution

AI Study Buddy is a web-based application powered by Claude (Anthropic's AI) that provides:

FeatureDescription🧠 Concept ExplainerExplains any topic at beginner, intermediate, or advanced level using structured explanations and real-world analogies📋 Note SummarizerConverts messy lecture notes into structured summaries, outlines, or concise digests✅ Quiz GeneratorCreates adaptive multiple-choice quizzes with instant feedback and detailed explanations🃏 Flashcard MakerGenerates interactive flashcard decks with memory hints for active recall practice


🛠 Technology Stack

LayerTechnologyBackendPython 3.10+, FlaskAI EngineAnthropic Claude API (claude-sonnet-4-6)FrontendHTML5, CSS3, Vanilla JavaScriptFontsSpace Grotesk, Inter, JetBrains Mono (Google Fonts)DeploymentRender / Railway / Heroku (any WSGI host)


🚀 Setup & Installation

Prerequisites


Python 3.10 or higher
An Anthropic API key


1. Clone the repository

bashgit clone https://github.com/YOUR_USERNAME/ai-study-buddy.git
cd ai-study-buddy

2. Create a virtual environment

bashpython -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

3. Install dependencies

bashpip install -r requirements.txt

4. Set environment variables

bash# Linux / macOS
export ANTHROPIC_API_KEY="your_api_key_here"

# Windows CMD
set ANTHROPIC_API_KEY=your_api_key_here

# Or create a .env file (see .env.example)

5. Run the application

bashpython app.py

Visit http://localhost:5000 in your browser.


📁 Project Structure

ai-study-buddy/
├── app.py                  # Flask application and API routes
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   └── js/
│       └── main.js         # Shared JavaScript utilities
├── templates/
│   ├── base.html           # Base layout with navbar
│   ├── index.html          # Landing page
│   ├── explain.html        # Concept Explainer tool
│   ├── summarize.html      # Note Summarizer tool
│   ├── quiz.html           # Quiz Generator tool
│   └── flashcards.html     # Flashcard Maker tool
└── README.md


🔄 Algorithm & System Flow

User Input (Topic / Notes)
        │
        ▼
   Flask Route Handler
        │
        ▼
  Prompt Engineering
  (level-aware, structured)
        │
        ▼
  Anthropic Claude API
  (claude-sonnet-4-6)
        │
        ▼
  Response Parsing
  (JSON or markdown)
        │
        ▼
  Rendered Output to User
  (interactive UI)

Key Algorithms


Prompt templating: Each tool constructs a structured prompt with role, task, format constraints, and output schema
JSON extraction: Quiz and flashcard endpoints strip markdown fences and parse validated JSON arrays
Client-side markdown rendering: A lightweight parser converts AI markdown output to HTML without external libraries



📊 Results

The application successfully:


Generates structured concept explanations tailored to 3 difficulty levels
Summarizes notes in 3 formats (structured, concise, outline)
Produces validated multiple-choice quizzes (5–10 questions) with answer explanations
Creates interactive flashcard decks (6–15 cards) with memory hints
Delivers results in under 5 seconds on average



✅ Conclusion

AI Study Buddy demonstrates how large language models can be productively integrated into educational tools. By abstracting complexity behind a clean, intuitive interface, students can access AI-powered tutoring instantly — without prior AI knowledge. The project validates the practical value of LLM APIs in real-world educational applications.

