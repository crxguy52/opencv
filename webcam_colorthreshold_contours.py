from __future__ import print_function
import cv2
import numpy as np
import time

'''
http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html#converting-colorspaces

Make sure to use the docs from version 3.1!!
http://docs.opencv.org/3.1.0/d4/d73/tutorial_py_contours_begin.html#gsc.tab=0
'''

cap = cv2.VideoCapture(0)

deltatsum = 0
n = 0
last_time = time.time()

while(1):

    # Take each frame
    _, frame = cap.read()

    
    #blur the frame to get rid of noise. the kernel should be ODD
    frame = cv2.GaussianBlur(frame,(21,21),0)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    lower_limit = np.array([0,150,150])
    upper_limit = np.array([10,255,255])

    # Threshold the HSV image to get only the thresholded colors
    # mask is a binary image
    mask = cv2.inRange(hsv, lower_limit, upper_limit)

    # The dimensions of the kernel must be odd!
    kernel = np.ones((3,3),np.uint8)
    kernel_lg = np.ones((15,15),np.uint8)
    
    # erosion followed by dilation is called an opening
    #http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # erode the mask to get rid of noise
    mask = cv2.erode(mask,kernel,iterations = 1)

    # dialate it back to regain some lost area
    mask = cv2.dilate(mask,kernel_lg,iterations = 1)    
    
    # Bitwise-AND the mask and grayscale image so we end up with our areas of interest and black everywhere else
    result = cv2.bitwise_and(frame,frame, mask= mask)
    
    # threshold the image to convert our image with areas of interest a binary image
    # note that this only works on black and white images!
    #
    # this isn't necessary for this example, since our mask is already a binary image
    #ret,thresh = cv2.threshold(result,30,255,0)
    
    thresh = mask
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    # define a minimum area for a contour - if it's below this, ignore it 
    min_area = 1000
    cont_filtered = []    
    
    # filter out all contours below a min_area
    for cont in contours:
        if cv2.contourArea(cont) > min_area:
            cont_filtered.append(cont)
            #print(cv2.contourArea(cont))

    # just take the first contour (we're assuming we only have one here)
    # the try\except is necessary, since the program will crash if it tries to access 
    # contours[0] and there aren't any
    try:
        cnt = cont_filtered[0]
        
        # draw the rectangle surrounding the filtered contour
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
        
        rows,cols = thresh.shape[:2]
        [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
        lefty = int((-x*vy/vx) + y)
        righty = int(((cols-x)*vy/vx)+y)
        cv2.line(frame,(cols-1,righty),(0,lefty),(0,255,0),2)        
        
        # this would draw all the contours on the image, not just the ones from cont_filtered
        #cv2.drawContours(frame, cont_filtered, -1, (0,255,0), 3)

        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
        print('x= ', cx, '  y= ', cy, ' angle = ', round(rect[2],2))
        #print(contours)
        #print('there are contours')
    except:
        print('no contours')

        
    cv2.imshow('frame',frame)
    #cv2.imshow('mask', mask)
    #cv2.imshow('thresh',thresh)
    #cv2.imshow('im2', im2)
    cv2.imshow('result', result)
    
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
		
    deltat = time.time() - last_time
    last_time = time.time()    
    deltatsum += deltat
    n += 1
    freq = round(1/(deltatsum/n), 2)
    #print('Updating at ' + str(freq) + ' FPS\r', end='')

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
