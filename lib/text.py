import numpy as np
import textwrap
import cv2
from lib.utils import *
from PIL import Image, ImageDraw, ImageFont
from translate import Translator


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

def findBubbleText (data):
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

def insertText (img, text, position, font_size, max_width, font):
    font_path = "./fonts/{}-Regular.ttf".format(font)
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype(font_path, font_size)

    x, y = position[0]
    x_bubble_locate = position[0][0]
    bubble_width = position[1][0] - position[0][0]

    # bubble_hight = position[1][1] - position[2][1]
    # max_height = bubble_hight - 10  

    wrapped_text = textwrap.wrap(text, width=max_width)

    for line in wrapped_text:
        line_width, line_height = font.getsize(line)
        x = x_bubble_locate + (bubble_width - line_width) // 2

        # Check if the line exceeds the maximum height
        # if y + line_height > max_height:
        #     break
        
        draw.text((x, y), line, font=font, fill="black")
        y += line_height
    return np.array(img)

def translate_text(text, target_language='vi'):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation