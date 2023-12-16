class Frame:
    class ID:
        def __init__(self, data):
            self.frame = data.get("FrameID")
            self.session = data.get("SessionID")
            self.last_frame = data.get("LastFrameID")

    class GPS:
        def __init__(self, data):
            self.speed = data.get("Speed")
            self.longitude = data.get("Longitude")
            self.latitude = data.get("Latitude")

    class Accelerometer:
        def __init__(self, data):
            self.acceleration_x = data.get("AccelerationX")
            self.acceleration_y = data.get("AccelerationY")
            self.acceleration_z = data.get("AccelerationZ")

            self.gravity_x = data.get("GravityX")
            self.gravity_y = data.get("GravityY")
            self.gravity_z = data.get("GravityZ")

    class Gyroscope:
        def __init__(self, data):
            self.rotation_delta_x = data.get("RotationDeltaX")
            self.rotation_delta_y = data.get("RotationDeltaY")
            self.rotation_delta_z = data.get("RotationDeltaZ")

    def __init__(self, data):
        self.id = Frame.ID(data.get("ID"))
        self.time = data.get("Time")
        self.gps = Frame.GPS(data.get("GPS"))
        self.accelerometer = Frame.Accelerometer(data.get("Accelerometer"))
        self.gyroscope = Frame.Gyroscope(data.get("Gyroscope"))
