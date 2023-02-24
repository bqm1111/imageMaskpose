import numpy as np
import glob
import cv2

out = cv2.VideoWriter('test.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 15, (112, 112))
 
for i in range(200):
    img = cv2.imread("example1.jpg")
    out.write(img)
out.release()