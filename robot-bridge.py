import cv2

vid = cv2.VideoCapture(0)

if vid.isOpened():
    rval, frame = vid.read()
else:
    rval = False
while rval:
    # cv2image = cv2.cvtColor(vid.read()[1], cv2.COLOR_BGR2RGB)
    hsv_frame = cv2.cvtColor(vid.read()[1], cv2.COLOR_BGR2HSV)
        
    gaussBlurImg = cv2.GaussianBlur(vid.read()[1], (9, 9), cv2.BORDER_DEFAULT)
    HSVResult = cv2.cvtColor(gaussBlurImg, cv2.COLOR_BGR2HSV)

    cv2.imshow('vid read', vid.read()[1])
    cv2.imshow('hsv frame', hsv_frame)
    cv2.imshow('gauss blur img', gaussBlurImg)
    cv2.imshow('HSV result', HSVResult)
    
    # if cv2.waitKey(delay) & 0xFF == ord('d'):
    #     break
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

vid.release()
cv2.destroyAllWindows()