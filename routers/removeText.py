import base64
import lib.image as IMG
from lib.text import insertText
import cv2
import numpy as np
import io
from PIL import Image


def handleRemoveText (data):
    image = data['image']
    location: dict = data['location']
    translated: dict = data['translated']

    imgBase64 = base64.b64decode(image)
    img = np.array(Image.open(io.BytesIO(imgBase64)))

    for group_locate in location.values():
        img = IMG.inpaint_text(img, group_locate)

    for key, group in translated.items():
        text= group['text']
        locationText= group['location']
        font= group['font']
        fontSize= group['fontSize']
        textInLine= group['textInLine']
        
        img = IMG.inpaint_text(img, locationText)
        img = insertText(img, text, locationText, fontSize, textInLine, font)

    retval, buffer = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    return {'image': encoded_image}