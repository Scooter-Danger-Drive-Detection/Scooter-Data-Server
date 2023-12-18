class Frame:
    class GPS:
        def __init__(self, speed: float, longitude: float, latitude: float):
            self.speed = speed
            self.longitude = longitude
            self.latitude = latitude

    class Accelerometer:
        def __init__(self, acceleration_x: float, acceleration_y: float, acceleration_z: float,
                     gravity_x: float, gravity_y: float, gravity_z: float):
            self.acceleration_x = acceleration_x
            self.acceleration_y = acceleration_y
            self.acceleration_z = acceleration_z

            self.gravity_x = gravity_x
            self.gravity_y = gravity_y
            self.gravity_z = gravity_z

    class Gyroscope:
        def __init__(self, rotation_delta_matrix: list,
                     angle_speed_x: float, angle_speed_y: float, angle_speed_z: float):
            self.rotation_delta_matrix = rotation_delta_matrix
            self.angle_speed_x = angle_speed_x
            self.angle_speed_y = angle_speed_y
            self.angle_speed_z = angle_speed_z

    def __init__(self, frame_id: int, session_id: int, previous_frame_id: int,
                 time, gps: GPS, accelerometer: Accelerometer, gyroscope: Gyroscope):
        self.frame_id = frame_id
        self.session_id = session_id
        self.previous_frame_id = previous_frame_id
        self.time = time
        self.gps = gps
        self.accelerometer = accelerometer
        self.gyroscope = gyroscope
