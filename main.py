from data import db_session
from load import app
import handlers

if __name__ == "__main__":
    db_session.global_init("database.db")
    db_session.create_session()
    app.run(host="127.0.0.1", port=8080)
