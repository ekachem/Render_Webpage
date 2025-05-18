from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Load questions from JSON file
def load_questions():
    with open("data/eqao_sample1.json", "r") as f:
        return json.load(f)

@app.route("/")
def index():
    test_data = load_questions()
    return render_template("index.html", title=test_data["title"])

@app.route("/test")
def test():
    test_data = load_questions()
    return render_template("test.html", questions=test_data["questions"], title=test_data["title"])

@app.route("/submit", methods=["POST"])
def submit():
    test_data = load_questions()
    questions = test_data["questions"]
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

    return render_template("result.html", score=score, total=len(questions), results=results, title=test_data["title"])

if __name__ == "__main__":
    app.run()  # Turn off debug in production

