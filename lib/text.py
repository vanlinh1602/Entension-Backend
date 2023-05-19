from lib.utils import *
import numpy as np

def centerTextLocate(locate):
    topLeft, topRight, bottomRight, bottomLeft = locate
    topMid = midPoint(topLeft, topRight)
    bottomMid = midPoint(bottomLeft, bottomRight)
    center = midPoint(topMid, bottomMid)
    return center

def getTextHeight(locate):
    pos1 = locate[0][1]
    pos2 = locate[2][1]
    return pos2 - pos1 

def isNearBubble (lastBubbleLocate, textLocate):
    lastTextBubbleMid = centerTextLocate(lastBubbleLocate)
    textMid = centerTextLocate(textLocate)
    textHeight = getTextHeight(textLocate) * 1.2
    distance = calculateDistance(lastTextBubbleMid, textMid)
    if (distance <= textHeight):
        return True
    else:
        return False
    
def getNewBubbleLocate(oldLocate, locate):
    oldTopLeft, oldTopRight, oldBottomRight, oldBottomLeft = oldLocate
    topLeft, topRight, bottomRight, bottomLeft = locate

    newTopLeft = oldTopLeft
    if (topLeft[0] < oldTopLeft[0]):
        newTopLeft = [topLeft[0], oldTopLeft[1]]
    
    newTopRight = oldTopRight
    if (topRight[0] > oldTopRight[0]):
        newTopRight = [topRight[0], oldTopRight[1]]

    newBottomRight = bottomRight
    if (oldBottomRight[0] > bottomRight[0]):
        newBottomRight = [oldBottomRight[0], bottomRight[1]]

    newBottomLeft = bottomLeft
    if (oldBottomLeft[0] < bottomLeft[0]):
        newBottomLeft = [oldBottomLeft[0], bottomLeft[1]]

    return [newTopLeft, newTopRight, newBottomRight, newBottomLeft]

def findBubbleText (data: list | list[dict[str, any]] | list[str] | list[list]):
    groupText: dict[str, any] = {}
    for textData in data:
        locate = np.array(textData[0]).tolist()
        text = str(textData[1]).lower()
        if (len(groupText) > 0):
            flag = False
            for key, groupValue in dict(groupText).items():
                lastGroupLocate = groupValue['lastText']
                nearBubble = isNearBubble(lastGroupLocate, locate)
                if (nearBubble):
                    groupText[key]['text'] += " " + text
                    groupText[key]['lastText'] = locate

                    oldLocate = groupValue['locate']
                    newLocate = getNewBubbleLocate(oldLocate, locate)
                    groupText[key]['locate'] = newLocate
                    flag = True
                    break
            if (not flag):
                key = 'group' + str(len(groupText) + 1)
                groupText[key] = {
                    'text': text,
                    'locate': locate,
                    'lastText': locate
                }
        else:
            groupText['group1'] = {
                'text': text,
                'locate': locate,
                'lastText': locate
            }
    return groupText