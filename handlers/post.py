import json
import sqlite3
from time import time

from flask import request

from load import app, frame_table, session_table
from models import Session, Frame
from models.ride_mode import get_ride_mode_by_key


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

    session_data = data.get("Session")
    session = Session(session_data.get("SessionID"), session_data.get("UserID"),
                      get_ride_mode_by_key(session_data.get("RideMode")))
    try:
        session.session_db_id = session_table.add_session(session)
    except sqlite3.IntegrityError:
        session = session_table.get_session_by_session_id_and_user_id(session.session_id, session.user_id)
    start_time = time()
    frames = list()
    for frame_data in data.get("Frames"):
        gps_data = frame_data.get("GPS")
        gps = Frame.GPS(gps_data.get("Speed"), gps_data.get("Longitude"), gps_data.get("Latitude"))

        accelerometer_data = frame_data.get("Accelerometer")
        accelerometer = Frame.Accelerometer(accelerometer_data.get("AccelerationX"),
                                            accelerometer_data.get("AccelerationY"),
                                            accelerometer_data.get("AccelerationZ"),
                                            accelerometer_data.get("GravityX"),
                                            accelerometer_data.get("GravityY"),
                                            accelerometer_data.get("GravityZ"))

        gyroscope_data = frame_data.get("Gyroscope")
        gyroscope = Frame.Gyroscope(gyroscope_data.get("RotationDeltaMatrix"),
                                    gyroscope_data.get("AngleSpeedX"),
                                    gyroscope_data.get("AngleSpeedY"),
                                    gyroscope_data.get("AngleSpeedZ"))

        frame = Frame(frame_data.get("FrameID"), frame_data.get("SessionID"), frame_data.get("PreviousFrameID"),
                      frame_data.get("Time"), gps, accelerometer, gyroscope)
        frames.append(frame)
    frame_table.add_frames(frames, session)
    print("--- %s seconds ---" % (time() - start_time))
    return "200"
