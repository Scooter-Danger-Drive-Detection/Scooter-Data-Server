import json

from flask import request

from data.functions import connect_db, close_connection
from load import app, session_table, frame_table, db_name


@app.route("/GetUserID", methods=["GET"])
def create_frame():
    # TODO: implement normal GetUserID handler
    return json.dumps({"UserID": 1})


@app.route("/GetAll", methods=["GET"])
def get_all():
    sessions = session_table.get_all_sessions()
    frames = frame_table.get_all_frames(sessions)

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


@app.route("/ExecuteSQL", methods=["GET"])
def execute_sql():
    query = request.args.get("query", default=None, type=str)
    if query is None:
        return "400"
    try:
        db = connect_db(db_name)
        cur = db.cursor()
        cur.execute(query)
        response = cur.fetchall()
        close_connection(db)
    except Exception as err:
        close_connection(db)
        return str(err)
    else:
        return response

