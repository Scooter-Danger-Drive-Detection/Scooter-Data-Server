from flask import request

from load import app, database
from models import Session


@app.route("/GetUserID", methods=["GET"])
def create_frame():
    return "{\n" \
           "\t\"UserID\" = 1\n" \
           "}"


@app.route("/StartSession", methods=["GET"])
def start_session():
    data = request.json
    return "{\n\t\"SessionID\" = " + str(database.session_table.add_session(Session(data))) + "\n}"
