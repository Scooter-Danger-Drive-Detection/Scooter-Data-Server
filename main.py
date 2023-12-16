from load import app, database
from flask import request

from models import Request


@app.route("/", methods=["POST"])
def create_frame():
    data = request.json
    request_obj = Request(data)
    database.add_request(request_obj)
