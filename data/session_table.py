import sqlite3 as sql

from models import Session
from models.ride_mode import SafeRideMode


class SessionTable:
    def __init__(self, db_name: str):
        self.db_name = db_name

        db = sql.connect(db_name)

        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS session("
                    "session_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "user_id INTEGER, "
                    "ride_mode INTEGER)",)
        db.commit()
        db.close()

    def add_session(self, session: Session) -> int:
        db = sql.connect(self.db_name)

        cur = db.cursor()
        cur.execute("INSERT INTO session VALUES(?, ?, ?)",
                    (
                        session.session_id,
                        session.user_id,
                        0 if isinstance(session.ride_mode, SafeRideMode) else (1 if session.ride_mode.alone else 2),
                    ))
        session_id = cur.lastrowid
        db.commit()
        db.close()
        return session_id
