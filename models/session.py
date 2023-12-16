from models import SafeRideMode, UnsafeRideMode


class Session:
    def __init__(self, data):
        self.session_id = data.get("ID")
        self.user_id = data.get("UserID")
        self.ride_mode = None
        ride_mode_id = data.get("RideMode")
        if ride_mode_id == 0:
            self.ride_mode = SafeRideMode()
        if ride_mode_id == 1:
            self.ride_mode = UnsafeRideMode(alone=True)
        if ride_mode_id == 2:
            self.ride_mode = UnsafeRideMode(alone=False)
