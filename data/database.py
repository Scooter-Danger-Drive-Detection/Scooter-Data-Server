import sqlite3 as sql

from models import Request, Session, Frame
from models.ride_mode import SafeRideMode


class DataBase:
    def __init__(self):
        self.db = sql.connect("data/database.db")
        self.frame_table = FrameTable(self)
        self.session_table = SessionTable(self)

    def cursor(self):
        return self.db.cursor()

    def commit(self):
        self.db.commit()

    def add_request(self, request: Request):
        for frame in request.frames:
            self.frame_table.add_frame(frame)
        self.session_table.add_session(request.session)


class FrameTable:
    def __int__(self, db: DataBase):
        self.db = db

        cur = self.db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS user("
                    "frame_id INTEGER, "
                    "session_id INTEGER, "
                    "last_frame_id INTEGER, "
                    "time: INTEGER, "
                    "speed: REAL, "
                    "longitude: REAL, "
                    "latitude: REAL, "
                    "accelerometer_x: REAL, "
                    "accelerometer_y: REAL, "
                    "accelerometer_z: REAL, "
                    "gravity_x: REAL, "
                    "gravity_y: REAL, "
                    "gravity_z: REAL, "
                    "rotation_delta_x: REAL, "
                    "rotation_delta_y: REAL, "
                    "rotation_delta_z: REAL) ")
        self.db.commit()

    def add_frame(self, frame: Frame):
        cur = self.db.cursor()

        cur.execute("INSERT INTO user VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
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
        self.db.commit()


class SessionTable:
    def __int__(self, db: DataBase):
        self.db = db.db

        cur = self.db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS session("
                    "session_id: INTEGER, "
                    "user_id: INTEGER, "
                    "ride_mode: INTEGER",)
        self.db.commit()

    def add_session(self, session: Session):
        cur = self.db.cursor()

        cur.execute("INSERT INTO session VALUES(?, ?, ?)",
                    (
                        session.session_id,
                        session.user_id,
                        0 if session.ride_mode is SafeRideMode else 1 if session.ride_mode.alone else 2,
                    ))
        self.db.commit()
