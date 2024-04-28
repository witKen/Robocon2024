import cv2
import numpy as np
import pyrealsense2 as rs

green_lower = np.array([35, 50, 50])
green_upper = np.array([90, 255, 255])

# Initialize Kalman filter
kalman = cv2.KalmanFilter(4, 2)
kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = 1e-4 * np.eye(4, dtype=np.float32)
kalman.measurementNoiseCov = 1e-2 * np.eye(2, dtype=np.float32)

pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    hsv_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, green_lower, green_upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)

            # Update Kalman filter with measurements
            measurements = np.array([[x + w/2], [y + h/2]], dtype=np.float32)
            kalman.correct(measurements)

            # Get estimated state from Kalman filter
            state = kalman.predict()

            # Draw bounding rectangle using estimated state
            cv2.rectangle(color_image, (int(state[0] - w/2), int(state[1] - h/2)),
                          (int(state[0] + w/2), int(state[1] + h/2)), (0, 255, 0), 2)

    cv2.imshow("depth frame", depth_image)
    cv2.imshow("Color frame", color_image)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

pipeline.release()
cv2.destroyAllWindows()