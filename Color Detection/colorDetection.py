# Color Detection With Normal Camera
# Use Shape Filteration to Detect Ball
# Use Noise Filteration

import cv2
import numpy as np
import imutils

class Detection:

    def findBalls(contours):
        minArea = 600
        ballsFound = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > minArea: 
                # Shape Fileration
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

    lower_red1 = np.array([0, 100, 100]) #0, 70, 50
    upper_red1 = np.array([8, 255, 255])
    lower_red2 = np.array([170, 70, 50]) #170, 70, 50
    upper_red2 = np.array([180, 255, 255])

    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    lower_purple = np.array([130, 0, 0])
    upper_purple = np.array([160, 255, 255])

    cap = cv2.VideoCapture(0)

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)  # Delay corresponding to video's frame rate

    while True:
        ret, frame = cap.read()

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        gaussBlurImg = cv2.GaussianBlur(frame, (9, 9), cv2.BORDER_DEFAULT)
        HSVResult = cv2.cvtColor(gaussBlurImg, cv2.COLOR_BGR2HSV)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        red1_mask = cv2.inRange(HSVResult, lower_red1, upper_red1)
        red2_mask = cv2.inRange(HSVResult, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red1_mask, red2_mask)

        filterErodeRed = cv2.erode(red_mask, kernel, iterations=3)
        filterDilateRed = cv2.dilate(filterErodeRed, kernel, iterations=2)

        blue_mask = cv2.inRange(HSVResult, lower_blue, upper_blue)
        filterErodeBlue = cv2.erode(blue_mask, kernel, iterations=3)
        filterDilateBlue = cv2.dilate(filterErodeBlue, kernel, iterations=2)

        red_contours = cv2.findContours(filterDilateRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        red_contours = imutils.grab_contours(red_contours)

        blue_contours = cv2.findContours(filterDilateBlue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours = imutils.grab_contours(blue_contours)

        purple_mask = cv2.inRange(HSVResult, lower_purple, upper_purple)
        filterErodePurple = cv2.erode(purple_mask, kernel, iterations=3)
        filterDilatePurple = cv2.dilate(filterErodePurple, kernel, iterations=2)

        purple_contours = cv2.findContours(filterDilatePurple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        purple_contours = imutils.grab_contours(purple_contours)

        red_found = findBalls(red_contours)
        blue_found = findBalls(blue_contours)
        purple_found = findBalls(purple_contours)

        for redBallOne in red_found:
            red_moments = cv2.moments(redBallOne)
            red_cX = int(red_moments["m10"] / red_moments["m00"])
            red_cY = int(red_moments["m01"] / red_moments["m00"])
            red_x, red_y, red_w, red_h = cv2.boundingRect(redBallOne)
            cv2.rectangle(frame, (red_x, red_y), (red_x + red_w, red_y + red_h), (0, 0, 255), 2)
            cv2.circle(frame, (red_cX, red_cY), 10, (0, 0, 255), -1)

        for blueBall in blue_found:
            blue_moments = cv2.moments(blueBall)
            blue_cX = int(blue_moments["m10"] / blue_moments["m00"])
            blue_cY = int(blue_moments["m01"] / blue_moments["m00"])
            blue_x, blue_y, blue_w, blue_h = cv2.boundingRect(blueBall)
            cv2.rectangle(frame, (blue_x, blue_y), (blue_x + blue_w, blue_y + blue_h), (255, 0, 0), 2)
            cv2.circle(frame, (blue_cX, blue_cY), 10, (255, 0, 0), -1)
        
        for purpleBall in purple_found:
            purple_moments = cv2.moments(purpleBall)
            purple_cX = int(purple_moments["m10"] / purple_moments["m00"])
            purple_cY = int(purple_moments["m01"] / purple_moments["m00"])
            purple_x, purple_y, purple_w, purple_h = cv2.boundingRect(purpleBall)
            cv2.rectangle(frame, (purple_x, purple_y), (purple_x + purple_w, purple_y + purple_h), (255, 0, 0), 2)
            cv2.circle(frame, (purple_cX, purple_cY), 10, (255, 0, 0), -1)


        cv2.imshow('frame', frame)
        cv2.imshow('Red Mask', red_mask)
        cv2.imshow('Blue Mask', blue_mask)
        cv2.imshow('Purple Mask', purple_mask)
        
        # if cv2.waitKey(delay) & 0xFF == ord('d'):
        #     break
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break

    cap.release()
    cv2.destroyAllWindows()