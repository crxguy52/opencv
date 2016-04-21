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

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #apply the background subtraction
    edges = cv2.Canny(frame,100,200)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    cv2.imshow('edges',edges)
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
