from flask import render_template

from load import app, session_predictions


@app.route("/GetPredictionHistory", methods=["GET"])
def get_prediction_history():
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h1>Session prediction history</h1>
{" ".join('<p>' + str(session_id) + " " + str(prediction) + '</p >' for session_id, prediction in session_predictions)}
</body>
</html>
"""
