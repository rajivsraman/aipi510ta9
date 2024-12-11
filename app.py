from flask import Flask, render_template, request
import pandas as pd
import random
import requests

app = Flask(__name__)

# Load the CSV file containing the math problems
DATA_FILE = "static/AIME_Dataset_1983_2024.csv"
data = pd.read_csv(DATA_FILE)

@app.route("/")
def home():
    '''Generates the home page of the website.'''
    return render_template("index.html")

@app.route("/mathproblems", methods=["GET", "POST"])
def math_problems():
    '''Selects three random AIME problems of varying difficulty.'''
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
        1: data[(data["Problem Number"] >= 1) & (data["Problem Number"] <= 3)], # criteria for Level 1 problems
        2: data[(data["Problem Number"] >= 4) & (data["Problem Number"] <= 10)], # criteria for Level 2 problems
        3: data[(data["Problem Number"] >= 11) & (data["Problem Number"] <= 15)], # criteria for Level 3 problems
    }

    for level, df in levels.items():
        row = df.sample(1).iloc[0]
        problems.append({
            "level": f"Level {level}",
            "problem": row["Question"],
            "answer": row["Answer"]
        })

    return render_template("mathproblems.html", problems=problems, feedback=None, enumerate=enumerate)

API_KEY = "AIzaSyCVYcQDvQSTTJZLsXJscbRSa5WUG5aCpY4"
PLAYLIST_ID = "PL3Oc1oiGnlKRZZKKWifYjNzrGJkox6_Ia"

def get_video_ids():
    '''Pulls the list of video IDs from the playlist ID specified above.'''
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={PLAYLIST_ID}&maxResults=500&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return [item['contentDetails']['videoId'] for item in data.get('items', [])]

@app.route("/geometrydash")
def geometry_dash():
    '''Renders a randomly selected video from the specified playlist in HTML for site display.'''
    video_ids = get_video_ids()
    random_video = random.choice(video_ids) if video_ids else None
    return render_template("geometrydash.html", video_id=random_video)

if __name__ == "__main__":
    app.run(debug=True)
