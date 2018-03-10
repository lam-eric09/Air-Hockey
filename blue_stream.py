import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# take first frame of the video
ret,frame = cap.read()
 

while(1):
    ret ,frame = cap.read()

    if ret == True:
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        #lower, upper values of hsv
        lower_blue= np.array([50,0,00])
        upper_blue = np.array([190,255,255])

        #mask of blue
        mask = cv2.inRange(hsv,lower_blue,upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)

        cv2.imshow('res',res)


        k = cv2.waitKey(60) & 0xff
        if k == 27:
            break
        else:
            cv2.imwrite(chr(k)+".jpg",res)

    else:
        break

cv2.destroyAllWindows()
cap.release()