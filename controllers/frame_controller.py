import json
from app import app
from flask import request

from controllers.request import Request


@app.route("/", methods=["POST"])
def create_frame():
    data = request.json
    request_obj = Request(data)
