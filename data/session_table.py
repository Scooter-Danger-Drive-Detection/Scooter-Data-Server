import sqlite3 as sql

from models import Session, get_ride_mode_by_key


def make_session_by_row(row):
    session = Session(row[1], row[2], get_ride_mode_by_key(row[3]), row[0])
    return session


class SessionTable:
    def __init__(self, db_name: str):
        self.db_name = db_name

        db = sql.connect(db_name)

        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS session("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "user_id INTEGER, "
                    "session_id INTEGER, "
                    "ride_mode INTEGER, "
                    "CONSTRAINT id_constraint UNIQUE(user_id, session_id))")
        db.commit()
        db.close()

    def add_session(self, session: Session) -> int:
        db = sql.connect(self.db_name)

        cur = db.cursor()
        cur.execute("INSERT INTO session VALUES(?, ?, ?, ?)",
                    (
                        None,
                        session.user_id,
                        session.session_id,
                        session.ride_mode.key
                    ))
        session_id = cur.lastrowid
        db.commit()
        db.close()
        return session_id

    def get_all_sessions(self) -> list:
        db = sql.connect(self.db_name)

        cur = db.cursor()
        cur.execute("SELECT * FROM session")
        rows = cur.fetchall()

        db.close()

        sessions = list()
        for row in rows:
            sessions.append(make_session_by_row(row))
        return sessions

    def get_session_by_session_id_and_user_id(self, session_id: int, user_id: int) -> Session:
        db = sql.connect(self.db_name)

        cur = db.cursor()
        cur.execute("SELECT * FROM session WHERE session_id=? AND user_id=?", (session_id, user_id))
        rows = cur.fetchall()

        db.close()

        return make_session_by_row(rows[0])
