import pyrealsense2 as rs
import math as m
import numpy as np
import cv2 as cv

class Camera:
    def __init__(self):
        try:
            # Create a pipeline for each camera
            self.pipeline1 = rs.pipeline()  # T265
            self.pipeline2 = rs.pipeline()  # D455

            # Create a config and configure it for each camera
            self.config1 = rs.config()
            self.config2 = rs.config()

            self.config1.enable_device('948422110347')  # Replace with your T265 serial number
            self.config2.enable_device('039222250173')  # Replace with your D455 serial number

            self.config1.enable_stream(rs.stream.pose)
            self.config2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
            self.config2.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

            # Start the pipeline for each camera
            self.pipeline1.start(self.config1)
            self.pipeline2.start(self.config2)
        except RuntimeError as e:
            print(f"Failed to start pipeline: {e}")
            self.pipeline1 = None
            self.pipeline2 = None

    def get_position_data(self):
        if not self.pipeline1:
            print("Pipeline for T265 is not initialized.")
            return
        try:
            frame = self.pipeline1.wait_for_frames()
            pose = frame.get_pose_frame()
            if pose:
                return pose
        except RuntimeError as e:
            print(f"Failed to get position data: {e}")

    def get_position(self):
        if not self.pipeline1:
            print("Pipeline for T265 is not initialized.")
            return
        try:
            frames = self.pipeline1.wait_for_frames()
            pose_frame = frames.get_pose_frame()
            if pose_frame:
                pose_data = pose_frame.get_pose_data()
                pos_data = {
                    "Frame Number": pose_frame.get_frame_number(),
                    "Angular velocity": pose_data.angular_velocity,
                    "Velocity": pose_data.velocity,
                    "Acceleration": pose_data.acceleration,
                    "Position": pose_data.translation,
                    "Tracker confidence": pose_data.tracker_confidence,
                    "Mapper confidence": pose_data.mapper_confidence,
                    "Timestamp": pose_frame.timestamp
                }
                print(pos_data)
        except RuntimeError as e:
            print(f"Failed to get position: {e}")

    def get_rotation(self):
        if not self.pipeline1:
            print("Pipeline for T265 is not initialized.")
            return
        try:
            frames = self.pipeline1.wait_for_frames()
            pose = frames.get_pose_frame()
            if pose:
                data = pose.get_pose_data()
                w, x, y, z = data.rotation.w, -data.rotation.z, data.rotation.x, -data.rotation.y

                pitch = -m.asin(2.0 * (x * z - w * y)) * 180.0 / m.pi
                roll = m.atan2(2.0 * (w * x + y * z), w * w - x * x - y * y + z * z) * 180.0 / m.pi
                yaw = m.atan2(2.0 * (w * z + x * y), w * w + x * x - y * y - z * z) * 180.0 / m.pi
                
                print(f"Frame #{pose.get_frame_number()}")
                print(f"RPY [deg]: Roll: {roll:.7f}, Pitch: {pitch:.7f}, Yaw: {yaw:.7f}")
        except RuntimeError as e:
            print(f"Failed to get rotation: {e}")


    def get_frame(self):
        if not self.pipeline2:
            print("Pipeline for D455 is not initialized.")
            return False, None, None
        try:
            frames = self.pipeline2.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                return False, None, None

            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            return True, depth_image, color_image
        except RuntimeError as e:
            print(f"Failed to get frame: {e}")
            return False, None, None

    def get_distance(self, xyxy):
        _, depth_frame, _ = self.get_frame()
        if depth_frame is None:
            return None

        try:
            # Get the depth value at a specific pixel (e.g., pixel at row=240, col=320)
            depth_value = depth_frame[240, 320]

            # Convert depth value to distance in meters using camera's depth scale
            depth_scale = self.pipeline2.get_active_profile().get_device().first_depth_sensor().get_depth_scale()
            distance_in_meters = depth_value * depth_scale
            return distance_in_meters
        except Exception as e:
            print(f"Failed to get distance: {e}")
            return None

    def close(self):
        if self.pipeline1:
            self.pipeline1.stop()
        if self.pipeline2:
            self.pipeline2.stop()

# Uncomment the method you want to test
# camera.get_position_data()
# camera.get_position()
# camera.get_rotation()
# camera.display()
# print(camera.get_distance((240, 320)))

# =============================================================================
    