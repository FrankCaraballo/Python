#find the possition of a particular color object in the screen and sends its value to serial port so it can be read by a microcontroler 
import cv2
import numpy as np
import serial

cntprev =1

ser = serial.Serial('COM9', 9600)

def nothing(x):
    pass

cap = cv2.VideoCapture(1)

# Make a window for the video feed  
cv2.namedWindow('frame',cv2.CV_WINDOW_AUTOSIZE)
# Make the trackbar used for HSV masking    
cv2.createTrackbar('H','frame',0,255,nothing)
cv2.createTrackbar('S','frame',0,255,nothing)
cv2.createTrackbar('V','frame',0,255,nothing)
cv2.createTrackbar('Hm','frame',0,255,nothing)
cv2.createTrackbar('Sm','frame',0,255,nothing)
cv2.createTrackbar('Vm','frame',0,255,nothing)

while(1):
    
    ret, frame = cap.read()
    
    # Take each frame
    _, frame = cap.read()
    j = cv2.getTrackbarPos('HSV','image')
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h =cv2.getTrackbarPos('H','frame')
    s=cv2.getTrackbarPos('S','frame')
    v=cv2.getTrackbarPos('V','frame')
    hm=cv2.getTrackbarPos('Hm','frame')
    sm=cv2.getTrackbarPos('Sm','frame')
    vm=cv2.getTrackbarPos('Vm','frame')
    
    # define range of blue color in HSV
    
    lower = np.array([h,s,v])
    upper = np.array([hm,sm,vm])
    
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)  

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    #erode morphological transform
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 4)
    #dilate morphological transform
    dilation = cv2.dilate(erosion,kernel,iterations = 4)
    #finding the countours
    
    ret,thresh = cv2.threshold(dilation,127,255,2)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #finding the momenths

    length =len(contours)
    print length

    if len(contours) ==0:
        cnt = cntprev
    else:
        cnt = contours[0]

    cntprev = cnt
    
    M = cv2.moments(cnt)
    if(M['m00']!=0):
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    #getting the info

    #print cx
    #print cy
    #print contours  
    cv2.circle(dilation,(cx,cy), 63, (125,125,255), 2)

    #titulo del proyecto
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(dilation,'RoboHockey',(10,30), font, 1,(255,255,255),2,cv2.CV_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'RoboHockey',(10,30), font, 1,(255,255,255),2,cv2.CV_AA)

    #infor de possicion
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(dilation,'Coordenada en X '+ str(cx),(10,470), font, 1,(255,255,255),2,cv2.CV_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Coordenada en X '+ str(cx),(10,470), font, 1,(255,255,255),2,cv2.CV_AA)
    #infor de possicion
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(dilation,'Coordenada en Y '+ str(cy),(10,430), font, 1,(255,255,255),2,cv2.CV_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,'Coordenada en Y '+ str(cy),(10,430), font, 1,(255,255,255),2,cv2.CV_AA)
  
  
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('HSV',hsv)
    cv2.imshow('erosion',erosion)
    cv2.imshow('dilation',dilation)
  
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    #serial Comunication
    if cy >0 and cy<68:
        ser.write('1')
    elif cy >68 and cy<136:
        ser.write('2')
    elif cy >136 and cy<204:
        ser.write('3')
    elif cy >204 and cy<272:
        ser.write('4')
    elif cy >272 and cy<340:
        ser.write('5')
    elif cy >340 and cy<408:
        ser.write('6')
    elif cy >408 and cy<476:
        ser.write('7')
    

cv2.destroyAllWindows()
