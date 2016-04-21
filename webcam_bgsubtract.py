from __future__ import print_function
import numpy as np
import cv2
import time



cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

deltatsum = 0
n = 0
last_time = time.time()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #blur the frame to get rid of noise. the kernel should be ODD
    #frame = cv2.GaussianBlur(frame,(7,7),0)	

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #apply the background subtraction
    fgmask = fgbg.apply(frame)

    kernel = np.ones((3,3),np.uint8)
    kernel_lg = np.ones((7,7),np.uint8)
    #erosion followed by dilation is called an opening
    #http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
	
	#erode the mask to get rid of noise
    fgmask = cv2.erode(fgmask,kernel,iterations = 1)

    #dialate it back to regain some lost area
    fgmask = cv2.dilate(fgmask,kernel_lg,iterations = 1) 

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.imshow('bgsubtract',fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
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
