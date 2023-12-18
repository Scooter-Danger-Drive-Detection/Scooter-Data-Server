import sqlite3 as sql

from models import Session


class SessionTable:
    def __init__(self, db_name: str):
        self.db_name = db_name

        db = sql.connect(db_name)

        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS session("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "user_id INTEGER, "
                    "session_id INTEGER, "
                    "ride_mode INTEGER)")
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
        for session_data in rows:
            session = Session(*session_data[1:], session_data[0])
            sessions.append(session)
        return sessions
