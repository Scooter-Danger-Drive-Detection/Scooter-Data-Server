import json

from flask import request

from load import app, frame_table, session_table
from models import Session, Frame
from models.ride_mode import get_ride_mode_by_key


@app.route("/StartSession", methods=["POST"])
def start_session():
    data = request.json
    return json.dumps({"SessionID": session_table.add_session(Session(data))})


@app.route("/SaveSession", methods=["POST"])
def save_session_data():
    data = request.json

    for session_data in data.get("Sessions"):
        session = Session(session_data.get("SessionID"), session_data.get("UserID"),
                          get_ride_mode_by_key(session_data.get("RideMode")))
        session.session_db_id = session_table.add_session(session)

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
        frame_table.add_frame(frame)
