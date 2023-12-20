import json
import sqlite3
from time import time

from flask import request

from load import app, frame_table, session_table, session_predictions
from models import Session
from models.ride_mode import get_ride_mode_by_key
from parsers import frame_json_to_model, session_json_to_model, reorder_frames
from prediction import get_prediction

previous_data = str()


@app.route("/", methods=["GET"])
def echo():
    return previous_data


@app.route("/GetFramesCount", methods=["POST"])
def get_frames_count():
    global previous_data
    previous_data = data = request.json
    session_id = data.get("SessionID")
    user_id = data.get("UserID")
    try:
        session = session_table.get_session_by_session_id_and_user_id(session_id, user_id)
    except IndexError:
        return "0"
    frames = frame_table.get_frames_by_session(session)
    return f"{len(frames)}"


@app.route("/StartSession", methods=["POST"])
def start_session():
    global previous_data
    previous_data = data = request.json
    return json.dumps({"SessionID": session_table.add_session(Session(data.get("SessionID"), data.get("UserID"),
                                                                      get_ride_mode_by_key(data.get("RideMode"))))})


@app.route("/SaveSession", methods=["POST"])
def save_session_data():
    global previous_data
    previous_data = data = request.json

    session = session_json_to_model(data.get("Session"))
    try:
        session.session_db_id = session_table.add_session(session)
    except sqlite3.IntegrityError:
        session = session_table.get_session_by_session_id_and_user_id(session.session_id, session.user_id)
    start_time = time()
    frames = list()
    for frame_data in data.get("Frames"):
        frame = frame_json_to_model(frame_data)
        frames.append(frame)
    frame_table.add_frames(frames, session)
    print("--- %s seconds ---" % (time() - start_time))
    return "200"


@app.route("/Predict", methods=["POST"])
def predict():
    global previous_data
    previous_data = data = request.json

    session = session_json_to_model(data)
    try:
        session = session_table.get_session_by_session_id_and_user_id(session.session_id, session.user_id)
    except IndexError as err:
        return f"400\n{err}"
    frames = frame_table.get_frames_by_session(session)
    frames = reorder_frames(frames)
    prediction = get_prediction(frames, session)
    session_predictions.append((session.session_id, prediction))
    return str(prediction)
