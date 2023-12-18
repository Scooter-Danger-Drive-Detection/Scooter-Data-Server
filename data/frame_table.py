import sqlite3 as sql

from models import Frame, Session


def make_frame_by_row(row):
    gps = Frame.GPS(*row[4:7])

    accelerometer = Frame.Accelerometer(*row[7:13])

    gyroscope = Frame.Gyroscope(row[13:22], *row[22:25])

    frame = Frame(row[0], row[1], row[2], row[3],
                  gps, accelerometer, gyroscope)

    return frame


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
                    "angle_speed_z REAL, "
                    "PRIMARY KEY(frame_id, session_id))")
        db.commit()
        db.close()

    def add_frame(self, frame: Frame, session: Session):
        db = sql.connect(self.db_name)
        cur = db.cursor()

        cur.execute("INSERT INTO frame "
                    f"VALUES({ ', '.join(['?'] * 25) })",
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
            for row in cur.fetchall():
                frames.append(make_frame_by_row(row))

        db.close()

        return frames

    def get_frames_by_session(self, session: Session) -> list[Frame]:
        db = sql.connect(self.db_name)

        cur = db.cursor()
        cur.execute("SELECT * FROM frame WHERE session_id=?", (session.session_db_id,))
        rows = cur.fetchall()
        db.close()

        frames = list()
        for row in rows:
            frames.append(make_frame_by_row(row))
        return frames
