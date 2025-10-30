# Simple Rule-based Chatbot

A compact Flask web app implementing a rules-only chatbot. The bot logic lives
in `app.py` and uses an ordered set of inline checks (if/elif/else) and shared
response pools so replies are fast and deterministic.

## 🎯 Objectives
- Understand how rule-based systems work.  
- Implement basic text processing and pattern matching.  
- Learn how to build an interactive chatbot.  

## Contents

- `app.py` — Flask app with the `get_bot_response()` rule engine (rules-only).
- `templates/index.html` — minimal browser UI for interacting with the bot.
- `requirements.txt` — Python dependencies.

## Quick start
1. Create and activate a virtualenv, then install deps:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

2. Run the app:

```bash
python3 app.py
```

3. Open the UI in your browser:

- http://localhost:5000 (local)
- Use your container/IDE port preview if running remotely.

## How responses are chosen

- Messages are normalized (lowercased) and matched against an ordered list of
  built-in rules in `get_bot_response()`.
- Responses are drawn from module-level pools (greetings, jokes, advice, etc.).
- A math helper evaluates simple binary expressions like `a + b`, `a - b`,
  `a * b`, and `a / b` (division-by-zero is handled safely).
- The first matching rule wins — ordering is important when you add rules.

Safety

- The frontend inserts replies as plain text to avoid XSS. If you enable HTML
	rendering, sanitize responses (for example with DOMPurify) and only render
	trusted content.

# Minimal contract

- Input: plain text message via the web UI or POST `/chat` with JSON
	`{ "message": "..." }`.
- Output: JSON `{ "reply": "..." }`.