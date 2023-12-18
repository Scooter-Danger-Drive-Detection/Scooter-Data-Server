import sqlite3 as sql

from models import Frame


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
                    "rotation_delta_matrix_0 REAL, "
                    "rotation_delta_matrix_1 REAL, "
                    "rotation_delta_matrix_2 REAL, "
                    "rotation_delta_matrix_3 REAL, "
                    "rotation_delta_matrix_4 REAL, "
                    "rotation_delta_matrix_5 REAL, "
                    "rotation_delta_matrix_6 REAL, "
                    "rotation_delta_matrix_7 REAL, "
                    "rotation_delta_matrix_8 REAL) ")
        db.commit()
        db.close()

    def add_frame(self, frame: Frame) -> int:
        db = sql.connect(self.db_name)
        cur = db.cursor()

        cur.execute("INSERT INTO frame VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                        *frame.gyroscope.rotation_delta_matrix
                    ))
        frame_id = cur.lastrowid
        db.commit()
        db.close()
        return frame_id
