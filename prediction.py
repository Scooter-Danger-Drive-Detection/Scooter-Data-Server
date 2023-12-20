from data import get_model
from load import model_name
from models import Frame, Session
from parsers import unite_frames_to_frame_batches, frame_batches_to_dataframe

parameters = ["average_acceleration", "min_acceleration", "max_acceleration", "average_angle_speed", "min_angle_speed", "max_angle_speed"]
target = "ride_mode"
batch_size = 100


def get_prediction(frames: list[Frame], session: Session):
    model = get_model(model_name)
    batches = unite_frames_to_frame_batches(frames, session, batch_size)
    df = frame_batches_to_dataframe(batches)
    predicts = model.predict(df[parameters])
    return sum(predicts) / len(predicts)
