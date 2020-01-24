import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread(r'images\aex-7.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(r'images\empty-slot-bottom.png', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.90
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)###
x = loc[1][0] + w//2
y = loc[0][0] + h//2
cv2.rectangle(img_rgb, (loc[1][0],loc[0][0]), (x,y), (0, 0, 255), 2)
print(x)
print(y)

cv2.imwrite('res.png',img_rgb)
cv2.imshow('img',img_rgb)











