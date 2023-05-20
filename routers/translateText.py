import base64
import lib.image as IMG
import cv2
import numpy as np
import io
from PIL import Image
from lib.text import insertText

def handleTranslateText (data):
    base64Data = data['image']
    dataTrans = data['dataTrans']
    imgBase64 = base64.b64decode(base64Data)
    img = np.array(Image.open(io.BytesIO(imgBase64)))

    for group in dataTrans:
        location = group['location']
        text = group['textTrans']
        img = IMG.inpaint_text(img, location)
        img = insertText(img, text, location, 15)

    retval, buffer = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return {'image' : encoded_image}