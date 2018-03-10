import cv2
import numpy as np
#from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
ret,frame = cap.read()
img = frame
#convert to hsv
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#lower, upper values of hsv
lower_blue= np.array([50,0,00])
upper_blue = np.array([190,255,255])

#mask of blue
mask = cv2.inRange(hsv,lower_blue,upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(frame,frame, mask= mask)

cv2.imshow('frame',frame)
cv2.imshow('mask',mask)
cv2.imshow('res',res)

#slice
#imask = mask>0 
#blue = np.zeros_like(img, np.uint8) 
#blue[imask] = img[imask]

cv2.waitKey(0)