from data.functions import connect_db, close_connection
from models import Session, get_ride_mode_by_key
from parsers import session_row_to_model


class SessionTable:
    def __init__(self, db_name: str):
        self.db_name = db_name
        db = connect_db(db_name)
        try:
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS session("
                        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                        "session_id INTEGER, "
                        "user_id INTEGER, "
                        "ride_mode INTEGER, "
                        "CONSTRAINT id_constraint UNIQUE(user_id, session_id))")
            db.commit()
        except Exception as err:
            close_connection(db)
            raise err
        close_connection(db)

    def add_session(self, session: Session) -> int:
        db = connect_db(self.db_name)
        try:
            cur = db.cursor()
            cur.execute("INSERT INTO session VALUES(?, ?, ?, ?)",
                        (
                            None,
                            session.session_id,
                            session.user_id,
                            session.ride_mode.key
                        ))
            session_id = cur.lastrowid
            db.commit()
        except Exception as err:
            close_connection(db)
            raise err
        close_connection(db)
        return session_id

    def get_all_sessions(self) -> list:
        db = connect_db(self.db_name)
        try:
            cur = db.cursor()
            cur.execute("SELECT * FROM session")
            rows = cur.fetchall()
        except Exception as err:
            close_connection(db)
            raise err
        close_connection(db)

        sessions = list()
        for row in rows:
            sessions.append(session_row_to_model(row))
        return sessions

    def get_session_by_session_id_and_user_id(self, session_id: int, user_id: int) -> Session:
        db = connect_db(self.db_name)
        try:
            cur = db.cursor()
            cur.execute("SELECT * FROM session WHERE session_id=? AND user_id=?", (session_id, user_id))
            rows = cur.fetchall()
        except Exception as err:
            close_connection(db)
            raise err
        close_connection(db)

        return session_row_to_model(rows[0])
