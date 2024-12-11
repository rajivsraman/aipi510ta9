from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# Load the CSV file containing the math problems
DATA_FILE = "static/AIME_Dataset_1983_2024.csv"
data = pd.read_csv(DATA_FILE)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/mathproblems", methods=["GET", "POST"])
def math_problems():
    if request.method == "POST":
        # Reconstruct problems from the form data
        problems = []
        for i in range(3):
            problems.append({
                "level": request.form.get(f"level_{i}"),
                "problem": request.form.get(f"problem_{i}"),
                "answer": request.form.get(f"correct_{i}")
            })

        # Handle feedback for the submitted question
        feedback = {}
        for index in range(3):
            user_answer = request.form.get(f"answer_{index}")
            correct_answer = problems[index]["answer"]

            if f"submit_{index}" in request.form:
                if user_answer is not None and user_answer.strip() == correct_answer.strip():
                    feedback[index] = "Correct!"
                else:
                    feedback[index] = f"Incorrect. The correct answer is {correct_answer}."

        return render_template("mathproblems.html", problems=problems, feedback=feedback, enumerate=enumerate)

    # Generate new random problems
    problems = []
    levels = {
        1: data[(data["Problem Number"] >= 1) & (data["Problem Number"] <= 3)],
        2: data[(data["Problem Number"] >= 4) & (data["Problem Number"] <= 10)],
        3: data[(data["Problem Number"] >= 11) & (data["Problem Number"] <= 15)],
    }

    for level, df in levels.items():
        row = df.sample(1).iloc[0]
        problems.append({
            "level": f"Level {level}",
            "problem": row["Question"],
            "answer": row["Answer"]
        })

    return render_template("mathproblems.html", problems=problems, feedback=None, enumerate=enumerate)


@app.route("/geometrydash")
def geometry_dash():
    return render_template("geometrydash.html")

if __name__ == "__main__":
    app.run(debug=True)
