import sqlite3 as sql

from models import Request, Session, Frame
from models.ride_mode import SafeRideMode


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.frame_table = FrameTable(db_name)
        self.session_table = SessionTable(db_name)

    def add_request(self, request: Request):
        for frame in request.frames:
            self.frame_table.add_frame(frame)
        self.session_table.add_session(request.session)


class FrameTable:
    def __init__(self, db_name: str):
        self.db_name = db_name

        db = sql.connect(db_name)

        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS frame("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "frame_id INTEGER, "
                    "session_id INTEGER, "
                    "last_frame_id INTEGER, "
                    "time INTEGER, "
                    "speed REAL, "
                    "longitude REAL, "
                    "latitude REAL, "
                    "accelerometer_x REAL, "
                    "accelerometer_y REAL, "
                    "accelerometer_z REAL, "
                    "gravity_x REAL, "
                    "gravity_y REAL, "
                    "gravity_z REAL, "
                    "rotation_delta_x REAL, "
                    "rotation_delta_y REAL, "
                    "rotation_delta_z REAL) ")
        db.commit()
        db.close()

    def add_frame(self, frame: Frame) -> int:
        db = sql.connect(self.db_name)
        cur = db.cursor()

        cur.execute("INSERT INTO frame VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        None,
                        frame.id.frame,
                        frame.id.session,
                        frame.id.last_frame,
                        frame.time,
                        frame.gps.speed,
                        frame.gps.longitude,
                        frame.gps.latitude,
                        frame.accelerometer.acceleration_x,
                        frame.accelerometer.acceleration_y,
                        frame.accelerometer.acceleration_z,
                        frame.accelerometer.gravity_x,
                        frame.accelerometer.gravity_y,
                        frame.accelerometer.gravity_z,
                        frame.gyroscope.rotation_delta_x,
                        frame.gyroscope.rotation_delta_y,
                        frame.gyroscope.rotation_delta_z,
                    ))
        frame_id = cur.lastrowid
        db.commit()
        db.close()
        return frame_id


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
