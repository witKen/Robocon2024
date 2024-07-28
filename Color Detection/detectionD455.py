# import cv2
# import numpy as np
# import pyrealsense2 as rs

# class Detection:
#     def findBalls(contours):
#         minArea = 600
#         ballsFound = []
#         for contour in contours:
#             area = cv2.contourArea(contour)
#             if area > minArea: 
#                 perimeter = cv2.arcLength(contour, True)
#                 approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
#                 if len(approx) < 3 or len(approx) > 6:
#                     circularity = 4 * np.pi * area / (perimeter * perimeter)
#                     hull = cv2.convexHull(contour)
#                     hull_area = cv2.contourArea(hull)
#                     solidity = float(area) / hull_area
#                     if circularity > 0.7 and solidity > 0.9 and len(approx) > 5:
#                         print("circular: ", circularity)
#                         print("solidity: ", solidity)
#                         ballsFound.append(contour)
#         return ballsFound

#     pipeline = rs.pipeline()
#     config = rs.config()

#     pipeline_wrapper = rs.pipeline_wrapper(pipeline)
#     pipeline_profile = config.resolve(pipeline_wrapper)
#     device = pipeline_profile.get_device()
#     device_product_line = str(device.get_info(rs.camera_info.product_line))

#     config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
#     config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

#     pipeline.start(config)

#     lower_red1 = np.array([0, 0, 0]) #0, 70, 50
#     upper_red1 = np.array([10, 255, 255])


#     lower_red2 = np.array([170, 0, 0]) #170, 70, 50
#     upper_red2 = np.array([180, 255, 255])

#     lower_blue = np.array([100, 50, 50])
#     upper_blue = np.array([130, 255, 255])

#     lower_white = np.array([0,0,200])
#     upper_white = np.array([180,30,255])

#     lower_black = np.array([0,0,0])
#     upper_black = np.array([180,255,30])

#     while True:

#         frames = pipeline.wait_for_frames()
#         depth_frame = frames.get_depth_frame()
#         color_frame = frames.get_color_frame()

#         depth_image = np.asanyarray(depth_frame.get_data())
#         color_image = np.asanyarray(color_frame.get_data())

#         hsv_frame = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)

#         red1_mask = cv2.inRange(hsv_frame, lower_red1, upper_red1)
#         red2_mask = cv2.inRange(hsv_frame, lower_red2, upper_red2)
#         blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
#         white_mask = cv2.inRange(hsv_frame, lower_white, upper_white)
#         black_mask = cv2.inRange(hsv_frame, lower_black, upper_black)

#         red_mask = cv2.bitwise_or(red1_mask, red2_mask)
#         red_mask = cv2.bitwise_or(red_mask, white_mask)
#         red_mask = cv2.bitwise_or(red_mask, black_mask)

#         blue_mask = cv2.bitwise_or(blue_mask, white_mask)
#         blue_mask = cv2.bitwise_or(blue_mask, black_mask)

#         red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         red_found = findBalls(red_contours)
#         blue_found = findBalls(blue_contours)

#         for redBallOne in red_found:
#             red_moments = cv2.moments(redBallOne)
#             red_cX = int(red_moments["m10"] / red_moments["m00"])
#             red_cY = int(red_moments["m01"] / red_moments["m00"])
#             red_x, red_y, red_w, red_h = cv2.boundingRect(redBallOne)
#             ((x, y), r) = cv2.minEnclosingCircle(redBallOne)
#             cv2.circle(color_image, (int(x), int(y)), int(r), (36, 255, 12), 2)
#             cv2.circle(color_image, (red_cX, red_cY), 10, (0, 0, 255), -1)

#         for blueBall in blue_found:
#             blue_moments = cv2.moments(blueBall)
#             blue_cX = int(blue_moments["m10"] / blue_moments["m00"])
#             blue_cY = int(blue_moments["m01"] / blue_moments["m00"])
#             blue_x, blue_y, blue_w, blue_h = cv2.boundingRect(blueBall)
#             ((x, y), r) = cv2.minEnclosingCircle(blueBall)
#             cv2.circle(color_image, (blue_cX, blue_cY), 10, (255, 0, 0), -1)

#         cv2.imshow('frame', color_image)
#         cv2.imshow('Red Mask', red_mask)
#         cv2.imshow('Blue Mask', blue_mask)
        
#         # if cv2.waitKey(delay) & 0xFF == ord('d'):
#         #     break
#         if cv2.waitKey(1) & 0xFF == ord('d'):
#             break

#     cv2.destroyAllWindows()

# import cv2
# import imutils
# import pygame
# import pyrealsense2 as rs
# import numpy as np

# pygame.init()

# pipeline = rs.pipeline()
# config = rs.config()

# pipeline_wrapper = rs.pipeline_wrapper(pipeline)
# pipeline_profile = config.resolve(pipeline_wrapper)
# device = pipeline_profile.get_device()
# device_product_line = str(device.get_info(rs.camera_info.product_line))

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
# config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# pipeline.start(config)

# ballColorLower = (100, 50, 50)
# ballColorUpper = (130, 255, 255)

# while True:
#     coreX = None
#     coreY = None
#     core2X = None
#     core2Y = None

#     #Grab values from cameras
#     frames = pipeline.wait_for_frames()
#     depth_frame = frames.get_depth_frame()
#     color_frame = frames.get_color_frame()

#     depth_image = np.asanyarray(depth_frame.get_data())
#     color_image = np.asanyarray(color_frame.get_data())

#     #Get dimensions of images and black out certain pixels
#     width = color_image.shape[0]
#     height = color_image.shape[1]
#     for i in range(width):
#         for j in range(height):
#             if i < 60:
#                 color_image[i][j] = (0,0,0)

#     #Resize Image
#     color_image = imutils.resize(color_image, width=550)

#     #Blur and convert to hsv C1
#     gaussBlurImg = cv2.GaussianBlur(color_image, (9, 9), cv2.BORDER_DEFAULT)
#     HSVResult = cv2.cvtColor(gaussBlurImg, cv2.COLOR_BGR2HSV)

#     #Process data to reduce noise
#     #Camera 1
#     filter = cv2.inRange(HSVResult, ballColorLower, ballColorUpper)
#     filterErode = cv2.erode(filter, None, iterations=3)
#     filterDilate = cv2.dilate(filterErode, None, iterations=2)

#     # processing = cv2.vconcat([image, mask])
#     extractedContours = cv2.findContours(filterDilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     extractedContours = imutils.grab_contours(extractedContours)

#     if len(extractedContours) > 0:
#         proposedBall1 = max(extractedContours, key=cv2.contourArea)
#         ((x1, y1), r) = cv2.minEnclosingCircle(proposedBall1)
#         cam1Moments = cv2.moments(proposedBall1)
#         coreX = int(cam1Moments["m10"] / cam1Moments["m00"])
#         coreY = int(cam1Moments["m01"] / cam1Moments["m00"])
        
#         #perhaps modify this if its picking up too much trash
#         if r > 3:
#             cv2.circle(color_image, (int(x1), int(y1)), int(r), (50, 205, 50), 1)
#             cv2.circle(color_image, (coreX, coreY), 5, (255, 165, 0), -1)
#         triggeredSound = False

#     processing = cv2.hconcat([color_image])
#     cv2.imshow('Video Stream', processing)

#     #If you hit escape, the program will halt
#     if cv2.waitKey(1) == 27:
#     	break

# #Close program and release cameras  
# cv2.destroyAllWindows()

import cv2
import imutils
import pyrealsense2 as rs
import numpy as np

class Detection:
    def findBalls(contours):
        minArea = 800
        ballsFound = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > minArea:
                perimeter = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
                if len(approx) < 3 or len(approx) > 6: #3,6
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    hull = cv2.convexHull(contour)
                    hull_area = cv2.contourArea(hull)
                    solidity = float(area) / hull_area
                    if circularity > 0.7 and solidity > 0.9: #0.7, 0.9
                        # print("circular: ", circularity)
                        # print("solidity: ", solidity)
                        # print("len(approx): ",len(approx))
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

    lower_red1 = np.array([0, 70,50]) #0, 70, 50
    upper_red1 = np.array([7, 255, 255])


    lower_red2 = np.array([170, 70, 50]) #170, 70, 50
    upper_red2 = np.array([180, 255, 255])

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    while True:

        #Grab values from cameras
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        #Get dimensions of images and black out certain pixels
        width = color_image.shape[0]
        height = color_image.shape[1]
        for i in range(width):
            for j in range(height):
                if i < 60:
                    color_image[i][j] = (0,0,0)

        #Resize Image
        color_image = imutils.resize(color_image, width=550)

        #Blur and convert to hsv C1
        gaussBlurImg = cv2.GaussianBlur(color_image, (9, 9), cv2.BORDER_DEFAULT)
        HSVResult = cv2.cvtColor(gaussBlurImg, cv2.COLOR_BGR2HSV)

        #Process data to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        red1_mask = cv2.inRange(HSVResult, lower_red1, upper_red1)
        red2_mask = cv2.inRange(HSVResult, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red1_mask, red2_mask)

        filterErodeRed = cv2.erode(red_mask, kernel, iterations=3)
        filterDilateRed = cv2.dilate(filterErodeRed, kernel, iterations=2)

        blue_mask = cv2.inRange(HSVResult, lower_blue, upper_blue)
        filterErodeBlue = cv2.erode(blue_mask, kernel, iterations=3)
        filterDilateBlue = cv2.dilate(filterErodeBlue, kernel, iterations=2)

        # processing = cv2.vconcat([image, mask])   
        red_contours = cv2.findContours(filterDilateRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_contours = imutils.grab_contours(red_contours)

        blue_contours = cv2.findContours(filterDilateBlue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours = imutils.grab_contours(blue_contours)

        red_found = findBalls(red_contours)
        blue_found = findBalls(blue_contours)
        
        # ballPosition = []

        for redBall in red_found:
            red_moments = cv2.moments(redBall)
            coreX = int(red_moments["m10"] / red_moments["m00"])
            coreY = int(red_moments["m01"] / red_moments["m00"])
            ((x1, y1), r) = cv2.minEnclosingCircle(redBall)

            if r > 15:
                cv2.circle(color_image, (int(x1), int(y1)), int(r), (0, 0, 255), 2)
                cv2.circle(color_image, (coreX, coreY), 10, (0, 0, 255), -1)
                
                

        for blueBall in blue_found:
            blue_moments = cv2.moments(blueBall)
            coreX = int(blue_moments["m10"] / blue_moments["m00"])
            coreY = int(blue_moments["m01"] / blue_moments["m00"])
            ((x1, y1), r) = cv2.minEnclosingCircle(blueBall)
            
            if r > 15:
                cv2.circle(color_image, (int(x1), int(y1)), int(r), (255, 0, 0), 2)
                cv2.circle(color_image, (coreX, coreY), 10, (255, 0, 0), -1)


                processing = cv2.hconcat([color_image])
        cv2.imshow('Video Stream', processing)
        cv2.imshow('Blue', filterDilateBlue)
        cv2.imshow('Dilate Red', filterDilateRed)

        #If you hit escape, the program will halt
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break

    #Close program and release cameras  
    cv2.destroyAllWindows()
