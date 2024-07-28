import cv2
import numpy as np
import pyrealsense2 as rs
 
# Use for finding color

def onTrack1(val):
    global hueLow
    hueLow=val
    print('Hue Low',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    print('Hue High',hueHigh)
def onTrack3(val):
    global satLow
    satLow=val
    print('Sat Low',satLow)
def onTrack4(val):
    global satHigh
    satHigh=val
    print('Sat High',satHigh)
def onTrack5(val):
    global valLow
    valLow=val
    print('Val Low',valLow)
def onTrack6(val):
    global valHigh
    valHigh=val
    print('Val High',valHigh)
 
pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

width=640
height=360
 
cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',width,0)
 
hueLow=10
hueHigh=20
satLow=10
satHigh=250
valLow=10
valHigh=250
 
cv2.createTrackbar('Hue Low','myTracker',110,180,onTrack1)
cv2.createTrackbar('Hue High','myTracker',130,180,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',50,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',250,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',50,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',250,255,onTrack6)

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
                    if circularity > 0.7:
                        print("circular: ", circularity)
                        ballsFound.append(contour)
        return ballsFound
 
while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    frameHSV=cv2.cvtColor(color_image,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    contours, _ = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #myMask=cv2.bitwise_not(myMask)

    ballsFound = findBalls(contours)

    for redBallOne in ballsFound:
        red_moments = cv2.moments(redBallOne)
        red_cX = int(red_moments["m10"] / red_moments["m00"])
        red_cY = int(red_moments["m01"] / red_moments["m00"])
        red_x, red_y, red_w, red_h = cv2.boundingRect(redBallOne)
        cv2.rectangle(color_image, (red_x, red_y), (red_x + red_w, red_y + red_h), (0, 0, 255), 2)
        cv2.circle(color_image, (red_cX, red_cY), 10, (0, 0, 255), -1)

    myObject=cv2.bitwise_and(color_image,color_image,mask=myMask)
    myObjectSmall=cv2.resize(myObject,(int(width/2),int(height/2)))
    cv2.imshow('My Object',myObjectSmall)
    cv2.moveWindow('My Object',int(width/2),int(height))
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('My Mask',myMaskSmall)
    cv2.moveWindow('My Mask',0,height)
    cv2.imshow('my WEBcam', color_image)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break