import cv2
import numpy as np
from lib.utils import *

def drawBubble(img: np.ndarray[any], groupText: dict):
    for key, text in groupText.items():
        locate = text['locate']
        [x1, y1], [x2, y2], [x3, y3], [x4, y4] = locate
        contour = np.array([[[x1, y1]], [[x2, y2]], [[x3, y3]], [[x4, y4]]], dtype=np.int32)
        cv2.drawContours(img, [contour], -1, (0, 0, 255), thickness=1)
    return img

def inpaint_text(img: np.ndarray[any], groupText: dict):
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for key, group in groupText.items():
        locate = group['locate']
        topLeft, topRight, bottomRight, bottomLeft = locate

        x_mid0, y_mid0 = midPoint(topLeft, topRight)
        x_mid1, y_mi1 = midPoint(bottomLeft, bottomRight)
        
        thickness = int(calculateDistance(topLeft, topRight)/2)
        
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255,    
        thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    return(img)

def exportImage(img, name: str):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'{name}.jpg',img_rgb)
