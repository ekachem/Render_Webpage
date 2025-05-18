from flask import Flask, render_template, request

app = Flask(__name__)

def load_questions():
    return {
        "title": "Grade 3 EQAO Practice",
        "questions": [
            {
                "question": "What is 2 + 2?",
                "choices": ["3", "4", "5"],
                "answer": "4"
            },
            {
                "question": "What color is the sky on a clear day?",
                "choices": ["Blue", "Green", "Red"],
                "answer": "Blue"
            },
            {
                "question": "How many days are there in a week?",
                "choices": ["5", "7", "10"],
                "answer": "7"
            }
        ]
    }

@app.route("/")
def index():
    data = load_questions()
    return render_template("index.html", title=data["title"])

@app.route("/test")
def test():
    data = load_questions()
    return render_template("test.html", questions=data["questions"], title=data["title"])

@app.route("/submit", methods=["POST"])
def submit():
    data = load_questions()
    score = 0
    results = []

    for i, q in enumerate(data["questions"]):
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

    return render_template("result.html", score=score, total=len(data["questions"]), results=results, title=data["title"])

if __name__ == "__main__":
    app.run()
