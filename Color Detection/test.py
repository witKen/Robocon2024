import cv2
import pyrealsense2 as rs
import time
import numpy as np

# Create a pipeline
pipeline = rs.pipeline()

# Create a configuration
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

webcam2 = cv2.VideoCapture(1)
webcam_cap = cv2.VideoCapture(0)

while True:
    # Get a frame from the pipeline
    frames = pipeline.wait_for_frames()

    # Get the depth and color frames
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    ret, webcam_frame = webcam_cap.read()
    ret, web = webcam2.read()
    if depth_frame and color_frame:
        # Convert the frames to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Display the frames
        cv2.imshow('Depth Image', depth_image)
        cv2.imshow('Color Image', color_image)
        cv2.imshow('Webcam', webcam_frame)
        cv2.imshow('web', web)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the pipeline and close the windows
pipeline.stop()
cv2.destroyAllWindows()