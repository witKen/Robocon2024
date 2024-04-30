import cv2
import numpy as np
import pyrealsense2 as rs

class Detection:

    def findBalls(contours):
        minArea = 600
        ballsFound = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > minArea: 
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
                if len(approx) < 3 or len(approx) > 6:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area) / hull_area
                    if circularity > 0.7 or solidity > 0.9:
                        print("circular: ", circularity)
                        print("solidity: ", solidity)
                        ballsFound.append(contour)
        return ballsFound

    pipeline = rs.pipeline()
    config = rs.config()

    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)

    lower_red1 = np.array([0, 70, 50]) #0, 70, 50
    upper_red1 = np.array([2, 255, 255])


    lower_red2 = np.array([170, 70, 50]) #170, 70, 50
    upper_red2 = np.array([180, 255, 255])


    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])


    while True:

        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        hsv_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

        red1_mask = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        red2_mask = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        red_mask = cv2.bitwise_or(red1_mask, red2_mask)

        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        red_found = findBalls(red_contours)
        blue_found = findBalls(blue_contours)

        for redBallOne in red_found:
            red_moments = cv2.moments(redBallOne)
            red_cX = int(red_moments["m10"] / red_moments["m00"])
            red_cY = int(red_moments["m01"] / red_moments["m00"])
            red_x, red_y, red_w, red_h = cv2.boundingRect(redBallOne)
            cv2.rectangle(color_image, (red_x, red_y), (red_x + red_w, red_y + red_h), (0, 0, 255), 2)
            cv2.circle(color_image, (red_cX, red_cY), 10, (0, 0, 255), -1)

        for blueBall in blue_found:
            blue_moments = cv2.moments(blueBall)
            blue_cX = int(blue_moments["m10"] / blue_moments["m00"])
            blue_cY = int(blue_moments["m01"] / blue_moments["m00"])
            blue_x, blue_y, blue_w, blue_h = cv2.boundingRect(blueBall)
            cv2.rectangle(color_image, (blue_x, blue_y), (blue_x + blue_w, blue_y + blue_h), (255, 0, 0), 2)
            cv2.circle(color_image, (blue_cX, blue_cY), 10, (255, 0, 0), -1)

        cv2.imshow('frame', color_image)
        cv2.imshow('Red Mask', red_mask)
        cv2.imshow('Blue Mask', blue_mask)
        
        # if cv2.waitKey(delay) & 0xFF == ord('d'):
        #     break
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break

    cv2.destroyAllWindows()