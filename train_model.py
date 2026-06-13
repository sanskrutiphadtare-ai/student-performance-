```python
from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load model and columns
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    form = request.form

    # User Input
    data = {
        "Hours_Studied": int(form["Hours_Studied"]),
        "Attendance": int(form["Attendance"]),
        "Previous_Scores": int(form["Previous_Scores"]),
        "Tutoring_Sessions": int(form["Tutoring_Sessions"]),
        "Sleep_Hours": int(form["Sleep_Hours"]),
        "Physical_Activity": int(form["Physical_Activity"]),
        "Internet_Access": form["Internet_Access"],
        "Access_to_Resources": form["Access_to_Resources"],
        "Parental_Involvement": form["Parental_Involvement"],
        "Peer_Influence": form["Peer_Influence"],
        "Family_Income": form["Family_Income"],
        "Gender": form["Gender"]
    }

    # Create DataFrame
    input_df = pd.DataFrame([data])

    # Convert categorical features
    input_df = pd.get_dummies(input_df)

    # Add missing columns
    for col in columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Arrange columns exactly as training data
    input_df = input_df[columns]

    # Predict
    predicted_score = round(float(model.predict(input_df)[0]))

    # AI Recommendations
    recommendations = []

    if data["Attendance"] < 80:
        recommendations.append(
            "Improve attendance above 80%."
        )

    if data["Hours_Studied"] < 4:
        recommendations.append(
            "Increase study hours to at least 4-5 hours daily."
        )

    if data["Sleep_Hours"] < 7:
        recommendations.append(
            "Maintain 7-8 hours of sleep for better concentration."
        )

    if data["Tutoring_Sessions"] < 2:
        recommendations.append(
            "Attend more tutoring sessions."
        )

    if data["Physical_Activity"] < 3:
        recommendations.append(
            "Increase physical activity to improve productivity."
        )

    if predicted_score >= 85:
        recommendations.append(
            "Excellent performance. Keep up the good work!"
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Your study habits are balanced. Continue the same routine."
        )

    return render_template(
        "result.html",
        score=predicted_score,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)
```
