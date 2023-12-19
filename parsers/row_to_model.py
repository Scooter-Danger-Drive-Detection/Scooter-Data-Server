from models import Session, get_ride_mode_by_key, Frame


def session_row_to_model(row):
    session = Session(row[1], row[2], get_ride_mode_by_key(row[3]), row[0])
    return session


def frame_row_to_model(row, session_id: int):
    gps = Frame.GPS(*row[4:7])

    accelerometer = Frame.Accelerometer(*row[7:13])

    gyroscope = Frame.Gyroscope(row[13:22], *row[22:25])

    frame = Frame(row[0], session_id, row[2], row[3],
                  gps, accelerometer, gyroscope)

    return frame
