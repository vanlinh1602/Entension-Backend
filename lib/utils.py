import math

def midPoint(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    x_mid = int((x1 + x2)/2)
    y_mid = int((y1 + y2)/2)
    return (x_mid, y_mid)

def calculateDistance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance