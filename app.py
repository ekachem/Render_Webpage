import os
import json
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change this to something secure for production

QUESTION_FOLDER = os.path.join(os.getcwd(), "questions")

def list_quiz_files():
    return [f for f in os.listdir(QUESTION_FOLDER) if f.endswith(".json")]

def load_questions(filename, limit=5):
    filepath = os.path.join(QUESTION_FOLDER, filename)
    with open(filepath, "r") as f:
        data = json.load(f)
    all_questions = data["questions"]
    random.shuffle(all_questions)
    data["questions"] = all_questions[:limit]
    return data

@app.route("/", methods=["GET", "POST"])
def index():
    quiz_files = list_quiz_files()
    if request.method == "POST":
        selected_file = request.form["quiz"]
        return redirect(url_for("test", quiz_file=selected_file))
    return render_template("index.html", quiz_files=quiz_files)

@app.route("/test")
def test():
    quiz_file = request.args.get("quiz_file")
    data = load_questions(quiz_file, limit=5)
    session["questions"] = data["questions"]
    session["quiz_file"] = quiz_file
    return render_template("test.html", questions=data["questions"], title=data["title"])

@app.route("/submit", methods=["POST"])
def submit():
    questions = session.get("questions", [])
    quiz_file = session.get("quiz_file", "unknown.json")
    score = 0
    results = []

    for i, q in enumerate(questions):
        user_answer = request.form.get(f"q{i}")
        correct = user_answer == q["answer"]
        if correct:
            score += 1
        results.append({
            "question": q["question"],
            "your_answer": user_answer,
            "correct_answer": q["answer"],
            "is_correct": correct
        })

    return render_template("result.html", score=score, total=len(questions), results=results, title="Your Results", quiz_file=quiz_file)

if __name__ == "__main__":
    app.run()

