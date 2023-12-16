from flask import request

from load import app, database
from models import Request


@app.route("/SaveSessionData", methods=["POST"])
def save_session_data():
    data = request.json
    request_obj = Request(data)
    database.add_request(request_obj)
    return "200"
