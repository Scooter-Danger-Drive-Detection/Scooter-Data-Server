import sqlite3 as sql

from load import session_table
from models import Frame, Session


class FrameTable:
    def __init__(self, db_name: str):
        self.db_name = db_name

        db = sql.connect(db_name)

        cur = db.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS frame("
                    "frame_id INTEGER, "
                    "session_id INTEGER, "
                    "previous_frame_id INTEGER, "
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
                    "rotation_delta_matrix_8 REAL, "
                    "angle_speed_x REAL, "
                    "angle_speed_y REAL, "
                    "angle_speed_z REAL "
                    "PRIMARY KEY(frame_id, session_id))")
        db.commit()
        db.close()

    def add_frame(self, frame: Frame, session: Session):
        db = sql.connect(self.db_name)
        cur = db.cursor()

        cur.execute("INSERT INTO frame "
                    f"VALUES({ '. '.join(['?'] * 25) })",
                    (
                        frame.frame_id,
                        session.session_db_id,
                        frame.previous_frame_id,
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
                        *frame.gyroscope.rotation_delta_matrix,
                        frame.gyroscope.angle_speed_x,
                        frame.gyroscope.angle_speed_y,
                        frame.gyroscope.angle_speed_z
                    ))
        db.commit()
        db.close()

    def get_all_frames(self, sessions: list[Session]) -> list:
        db = sql.connect(self.db_name)

        cur = db.cursor()

        frames = list()

        for session in sessions:
            cur.execute("SELECT * FROM frame WHERE session_id=?", (session.session_db_id,))
            for frame_data in cur.fetchall():
                gps = Frame.GPS(*frame_data[4:7])

                accelerometer = Frame.Accelerometer(*frame_data[7:13])

                gyroscope = Frame.Gyroscope(frame_data[13:22], *frame_data[22:25])

                frame = Frame(frame_data[0], frame_data[1], frame_data[2], frame_data[3],
                              gps, accelerometer, gyroscope)

                frames.append(frame)

        db.close()

        return frames
