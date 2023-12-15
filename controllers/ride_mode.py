class RideMode:
    pass


class SafeRideMode(RideMode):
    pass


class UnsafeRideMode(RideMode):
    def __init__(self, alone: bool):
        self.alone = alone
