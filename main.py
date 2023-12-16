from load import app, database
from flask import request, make_response

from models import Request


@app.route("/", methods=["POST"])
def create_frame():
    data = request.json
    request_obj = Request(data)
    database.add_request(request_obj)
    return "200"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
