# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

camera = cv2.VideoCapture(0)
#type in the terminal, to make picamra accessible from VideoCapture
#sudo modprobe bcm2835-v4l2

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

pts = deque(maxlen=args["buffer"])

# take first frame of the video
ret,frame = camera.read()
 
while(1):
    ret ,frame = camera.read()

    if ret == True:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_blue = np.array([90,50,50])
        upper_blue = np.array([160,255,255])

        # resize the frame, blur it, and convert it to the HSV
	    # color space
        # frame = imutils.resize(frame, width=600)
	    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
	    # construct a mask for the color "green", then perform
    	# a series of dilations and erosions to remove any small
	    # blobs left in the mask

        #mask of blue
        mask = cv2.inRange(hsv,lower_blue,upper_blue)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)


    	# find contours in the mask and initialize the current
    	# (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
 
    	# only proceed if at least one contour was found
        if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
	    	# only proceed if the radius meets a minimum size
            if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        
    	# update the points queue
        pts.appendleft(center)
       
    	# loop over the set of tracked points
        for i in range(1, len(pts)):
	    	# if either of the tracked points are None, ignore
	    	# them
            if pts[i - 1] is None or pts[i] is None:
                continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)

    	# show the frame to our screen
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1) & 0xFF
 
        #ADD draw in additional window
        
        cv2.imshow("Mask", mask)

    	# if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()