# import cv2
# import numpy as np

# def findLargestContour(contours):
#     maxArea = 0
#     minArea = 400
#     largestContour = None
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area > maxArea and area > minArea: 
#             # moments = cv2.moments(contour)
#             # cX = int(moments["m10"] / moments["m00"])
#             # cY = int(moments["m01"] / moments["m00"])

#             # if iLastX >= 0 and iLastY >= 0 and cX >= 0 and cY >= 0:
#             #     cv2.line(frame, (cX, cY), (iLastX, iLastY), (0, 0, 255), 2)

#             # iLastX = cX
#             # iLastY = cY

#             maxArea = area
#             largestContour = contour
#     return largestContour
# #     if largestContour is not None:
# #        approx = cv2.approxPolyDP(largestContour, 0.01 * cv2.arcLength(largestContour, True), True)
# #        if len(approx) >= 9:
# #            print("is Ball")
# #            return largestContour
# #    return None

# iLastX = -1
# iLastY = -1

# lower_red1 = np.array([0,70,50])
# upper_red1 = np.array([10,255,255])

# #blue range
# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])

# # #Red range
# # lower_red1 = np.array([0,31,255])
# # upper_red1 = np.array([176,255,255])

# ballWidth = 190

# cap = cv2.VideoCapture(0)

# while True:
#     re, frame = cap.read()

#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     mask = cv2.inRange(hsv_frame, lower_red1, upper_red1)

#     # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
#     # mask = cv2.erode(mask, kernel, iterations=1)
#     # mask = cv2.dilate(mask, kernel, iterations=1)
#     # mask = cv2.dilate(mask, kernel, iterations=1)
#     # mask = cv2.erode(mask, kernel, iterations=1)

#     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     largestContour = findLargestContour(contours)

#     if largestContour is not None:
#         x, y, w, h = cv2.boundingRect(largestContour)
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

#     # cv2.imshow('mask', mask)
#     # mask = cv2.add(mask, np.zeros_like(mask, dtype=np.uint8))
#     cv2.imshow('frame', frame)

#     if cv2.waitKey(1) & 0xFF == ord('d'):
#         break
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import numpy as np

# def findLargestContour(contours):
#     maxArea = 0
#     minArea = 500
#     largestContour = None
#     for contour in contours:
#         area = cv2.contourArea(contour)
#         if area > maxArea and area > minArea: 
#             maxArea = area
#             largestContour = contour
#     return largestContour

# lower_red1 = np.array([0,70,50])
# upper_red1 = np.array([10,255,255])

# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()

#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     red_mask = cv2.inRange(hsv_frame, lower_red1, upper_red1)
#     blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

#     red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     red_largestContour = findLargestContour(red_contours)
#     blue_largestContour = findLargestContour(blue_contours)

#     if red_largestContour is not None:
#         red_moments = cv2.moments(red_largestContour)
#         red_cX = int(red_moments["m10"] / red_moments["m00"])
#         red_cY = int(red_moments["m01"] / red_moments["m00"])
#         red_x, red_y, red_w, red_h = cv2.boundingRect(red_largestContour)
#         cv2.rectangle(frame, (red_x, red_y), (red_x + red_w, red_y + red_h), (0, 0, 255), 2)
#         cv2.circle(frame, (red_cX, red_cY), 10, (0, 0, 255), -1)

#     if blue_largestContour is not None:
#         blue_moments = cv2.moments(blue_largestContour)
#         blue_cX = int(blue_moments["m10"] / blue_moments["m00"])
#         blue_cY = int(blue_moments["m01"] / blue_moments["m00"])
#         blue_x, blue_y, blue_w, blue_h = cv2.boundingRect(blue_largestContour)
#         cv2.rectangle(frame, (blue_x, blue_y), (blue_x + blue_w, blue_y + blue_h), (255, 0, 0), 2)
#         cv2.circle(frame, (blue_cX, blue_cY), 10, (255, 0, 0), -1)

#     cv2.imshow('frame', frame)
#     cv2.imshow('Red Mask', red_mask)
    

#     if cv2.waitKey(1) & 0xFF == ord('d'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

class Detection:
    
    def findLargestContour(contours):
        maxArea = 0
        minArea = 600
        largestContour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > maxArea and area > minArea: 
                perimeter = cv2.arcLength(contour, True)
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                solidity = float(area) / hull_area
                if circularity > 0.7 or solidity > 0.8:
                    maxArea = area
                    largestContour = contour
        return largestContour

    # def isBallShape(contour):
    #     perimeter = cv2.arcLength(contour, True)
    #     area = cv2.contourArea(contour)
    #     circularity = 4 * np.pi * area / (perimeter * perimeter)
    #     if circularity > 0.4:  # Adjust the circularity threshold as needed, 0.7
    #         return True
    #     return False

    lower_red1 = np.array([0, 100, 100]) #0, 70, 50
    upper_red1 = np.array([8, 255, 255])

    # lower_red1 = np.array([0, 70, 50]) #0, 70, 50
    # upper_red1 = np.array([15, 255, 255])

    lower_red2 = np.array([170, 70, 50]) #170, 70, 50
    upper_red2 = np.array([180, 255, 255])

    # lower_red2 = np.array([160, 70, 50]) #0, 70, 50
    # upper_red2 = np.array([180, 255, 255])

    lower_blue = np.array([110, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # lower_blue = np.array([100, 50, 50])
    # upper_blue = np.array([140, 255, 255])

    video_path = '2.mp4'  # Replace with the actual path to your video file
    cap = cv2.VideoCapture(video_path)
    # cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)  # Delay corresponding to video's frame rate

    while True:
        ret, frame = cap.read()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red1_mask = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        red2_mask = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        red1_contours, _ = cv2.findContours(red1_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red2_contours, _ = cv2.findContours(red2_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        red1_largestContour = findLargestContour(red1_contours)
        red2_largestContour = findLargestContour(red2_contours)
        blue_largestContour = findLargestContour(blue_contours)

        if red1_largestContour is not None:
            red_moments = cv2.moments(red1_largestContour)
            red_cX = int(red_moments["m10"] / red_moments["m00"])
            red_cY = int(red_moments["m01"] / red_moments["m00"])
            red_x, red_y, red_w, red_h = cv2.boundingRect(red1_largestContour)
            cv2.rectangle(frame, (red_x, red_y), (red_x + red_w, red_y + red_h), (0, 0, 255), 2)
            cv2.circle(frame, (red_cX, red_cY), 10, (0, 0, 255), -1)
        elif red2_largestContour is not None:
            red_moments = cv2.moments(red2_largestContour)
            red_cX = int(red_moments["m10"] / red_moments["m00"])
            red_cY = int(red_moments["m01"] / red_moments["m00"])
            red_x, red_y, red_w, red_h = cv2.boundingRect(red2_largestContour)
            cv2.rectangle(frame, (red_x, red_y), (red_x + red_w, red_y + red_h), (0, 0, 255), 2)
            cv2.circle(frame, (red_cX, red_cY), 10, (0, 0, 255), -1)

        if blue_largestContour is not None:
            blue_moments = cv2.moments(blue_largestContour)
            blue_cX = int(blue_moments["m10"] / blue_moments["m00"])
            blue_cY = int(blue_moments["m01"] / blue_moments["m00"])
            blue_x, blue_y, blue_w, blue_h = cv2.boundingRect(blue_largestContour)
            cv2.rectangle(frame, (blue_x, blue_y), (blue_x + blue_w, blue_y + blue_h), (255, 0, 0), 2)
            cv2.circle(frame, (blue_cX, blue_cY), 10, (255, 0, 0), -1)

        cv2.imshow('frame', frame)
        cv2.imshow('Red Mask 1', red1_mask)
        cv2.imshow('Red Mask 2', red2_mask)
        cv2.imshow('Blue Mask', blue_mask)
        
        # if cv2.waitKey(delay) & 0xFF == ord('d'):
        #     break
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break

    cap.release()
    cv2.destroyAllWindows()