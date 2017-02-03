#Isolates an objet within an color range and fints it relative possition 
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    #canny edge detection
    img = res
    edges = cv2.Canny(img,100,200)
        
    #contours finding
    im = edges
    ret,thresh = cv2.threshold(im,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cordinates finding
    cnt = contours[-1]
    #hull = cv2.convexHull(cnt)
    M = cv2.moments(cnt)
    #cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])
    
    #print hull
    #cx0=np.average(hull, axis=0)
    #cy0=np.average(hull, axis=1)
       
    #cx=np.average(cx0)
    #cy=np.average(cy0)
    #print cx[0][0]
    #center,radius=cv2.minEnclosingCircle(contours)
    #contours drawing
    cv2.drawContours(thresh,contours,-1,(255,255,255),3)

    #cv2.circle(edges,(int(cx),int(cy)),30,(255,255,255),1)
    #print(contours)
    cv2.imshow('contours',thresh)
    cv2.imshow('edges',edges)
    
cv2.destroyAllWindows()
