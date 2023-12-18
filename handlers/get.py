import json

from flask import request

from load import app, session_table
from models import Session


@app.route("/GetUserID", methods=["GET"])
def create_frame():
    # TODO: implement normal GetUserID handler
    return json.dumps({"UserID": 1})
