# Chat-VAO 🐍🤖

**Chat-VAO** is an intelligent web application designed for quick information retrieval on Python programming. The project combines a SQLite-based knowledge base with Artificial Intelligence elements for semantic search and question processing.

## 🎯 Project Goal
To help beginner programmers quickly find answers to questions about Python syntax, libraries, and best practices using natural language queries.

## ✨ Key Features
*   **Smart Search:** Powered by the Spacy library, the bot understands the meaning of questions, even if they contain typos or different wording.
*   **Knowledge Base:** Structured information organized by categories (variables, loops, OOP, etc.).
*   **Data Management:** Built-in functions to add, modify, and delete questions and answers.
*   **Web Interface:** A user-friendly chat experience in the browser built with Flask and Bootstrap 5.

## 🛠 Tech Stack
*   **Backend:** Python, Flask
*   **AI/NLP:** Spacy (using the `ru_core_news_lg` model)
*   **Database:** SQLite3
*   **Frontend:** HTML5, CSS3, Bootstrap 5
*   **Testing:** Pytest

## 📂 Project Structure
*   `app.py` — Main Flask application entry point.
*   `chat_bot.py` — Message processing logic and AI-driven search.
*   `create_db.py` — Database initialization script.
*   `faq.db` — SQLite database file containing questions and answers.
*   `tests/` — Automated test suite directory.
*   `static/` — Static assets (CSS styles, images, logos).
*   `templates/` — HTML page templates.

## 🚀 Installation & Setup

### 1. Requirements
Ensure you have Python 3.8+ installed. Install the necessary libraries:
```bash
pip install flask spacy pytest
```

### 2. AI Language Model Download
To enable semantic search, you must download the Russian language model:
```bash
python -m spacy download ru_core_news_lg
```

### 3. Running the Application
```bash
python app.py
```
Once started, open your browser and go to: `http://127.0.0.1:5000`

## 🧪 Testing
The project includes an automated test suite to ensure stability.
To run all tests, execute:
```bash
python -m pytest tests/test_app.py
```

## 👥 The Team
*   **Loiko** (GitHub: [ViktoriaLoiko](https://github.com/ViktoriaLoiko))
*   **Klimenko** (GitHub: [nasty-xd](https://github.com/nasty-xd))
*   **Evstafieva** (GitHub: [OlgaEvfs](https://github.com/OlgaEvfs))

## 📄 License
This project is released under the MIT License.
