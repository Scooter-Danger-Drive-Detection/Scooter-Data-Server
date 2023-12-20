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
{" ".join('<p>' + str(session.session_id) + ' ||| ' + str(-1 if session.ride_mode is None else session.ride_mode.key) + " ||| " + str(prediction) + '</p >' for session, prediction in session_predictions)}
</body>
</html>
"""
