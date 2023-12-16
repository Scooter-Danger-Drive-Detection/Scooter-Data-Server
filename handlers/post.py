from flask import request

from load import app, frame_table, session_table
from models import Request


@app.route("/SaveSessionData", methods=["POST"])
def save_session_data():
    data = request.json
    request_obj = Request(data)
    for frame in request_obj.frames:
        frame_table.add_frame(frame)
    session_table.add_session(request_obj.session)
    return "200"
