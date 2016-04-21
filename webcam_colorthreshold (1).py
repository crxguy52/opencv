from __future__ import print_function
import cv2
import numpy as np
import time

'''
http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces
'''

cap = cv2.VideoCapture(0)

deltatsum = 0
n = 0
last_time = time.time()

while(1):

    # Take each frame
    _, frame = cap.read()

    '''
    #blur the frame to get rid of noise. the kernel should be ODD
    frame = cv2.GaussianBlur(frame,(7,7),0)
    '''

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([0,100,100])
    upper_blue = np.array([10,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((3,3),np.uint8)
    kernel_lg = np.ones((7,7),np.uint8)
    #erosion followed by dilation is called an opening
    #http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    #erode the mask to get rid of noise
    mask = cv2.erode(mask,kernel,iterations = 1)

    #dialate it back to regain some lost area
    mask = cv2.dilate(mask,kernel_lg,iterations = 1)    

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
	
    x,y,w,h = cv2.boundingRect(mask)
    cv2.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)	

    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
		
    deltat = time.time() - last_time
    last_time = time.time()    
    deltatsum += deltat
    n += 1
    freq = round(1/(deltatsum/n), 2)
    print('Updating at ' + str(freq) + ' FPS\r', end='')

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
