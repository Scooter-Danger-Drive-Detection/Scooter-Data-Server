import json

from load import app, session_table, frame_table


@app.route("/GetUserID", methods=["GET"])
def create_frame():
    # TODO: implement normal GetUserID handler
    return json.dumps({"UserID": 1})


@app.route("/GetAll", methods=["GET"])
def get_all():
    sessions = session_table.get_all_sessions()
    frames = frame_table.get_all_frames()

    return {
        "Sessions": [
            session.to_dict()
            for session in sessions
        ],
        "Frames": [
            frame.to_dict()
            for frame in frames
        ]
    }
