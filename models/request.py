from models import Frame, Session


class Request:
    def __init__(self, data):
        self.frames = [Frame(frame_data) for frame_data in data.get("Frames")]
        self.session = Session(data.get("Session"))
