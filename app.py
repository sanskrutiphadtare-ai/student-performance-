from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    hours = float(request.form['Hours_Studied'])
    attendance = float(request.form['Attendance'])
    previous = float(request.form['Previous_Scores'])

    # Dummy Prediction Logic
    score = round(
        (hours * 3) +
        (attendance * 0.3) +
        (previous * 0.4)
    )

    if score > 100:
        score = 100

    recommendations = []

    if score < 50:
        recommendations.append("Increase study hours.")
        recommendations.append("Improve attendance.")
        recommendations.append("Revise previous topics regularly.")

    elif score < 75:
        recommendations.append("Maintain consistency.")
        recommendations.append("Practice mock tests.")
        recommendations.append("Focus on weak subjects.")

    else:
        recommendations.append("Excellent performance.")
        recommendations.append("Keep up current study habits.")
        recommendations.append("Aim for competitive exams.")

    return render_template(
        'result.html',
        score=score,
        recommendations=recommendations
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
