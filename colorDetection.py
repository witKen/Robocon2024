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

# lower_red = np.array([0,70,50])
# upper_red = np.array([10,255,255])

# #blue range
# lower_blue = np.array([110,50,50])
# upper_blue = np.array([130,255,255])

# # #Red range
# # lower_red = np.array([0,31,255])
# # upper_red = np.array([176,255,255])

# ballWidth = 190

# cap = cv2.VideoCapture(0)

# while True:
#     re, frame = cap.read()

#     hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

#     mask = cv2.inRange(hsv_frame, lower_red, upper_red)

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

import cv2
import numpy as np

def findLargestContour(contours):
    maxArea = 0
    minArea = 500
    largestContour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxArea and area > minArea: 
            maxArea = area
            largestContour = contour
    return largestContour

lower_red = np.array([0,70,50])
upper_red = np.array([10,255,255])

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_largestContour = findLargestContour(red_contours)
    blue_largestContour = findLargestContour(blue_contours)

    if red_largestContour is not None:
        red_moments = cv2.moments(red_largestContour)
        red_cX = int(red_moments["m10"] / red_moments["m00"])
        red_cY = int(red_moments["m01"] / red_moments["m00"])
        red_x, red_y, red_w, red_h = cv2.boundingRect(red_largestContour)
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

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cap.release()
cv2.destroyAllWindows()