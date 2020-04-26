import cv2
import numpy as np


img = cv2.imread('friends.jpg')
cv2.rectangle(img,(0,0),(100,100),(255,0,0),2)
def onmouse(event, x, y, flags, param):
    if(event == 4):
        print(str(x)+" , "+str(y))
        print(flags)
        print(param)





cv2.imshow("vase", img)
cv2.setMouseCallback("vase", onmouse)
cv2.waitKey(0)
