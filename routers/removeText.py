import base64
import lib.image as IMG
import cv2
import numpy as np
import io
from PIL import Image


def handleRemoveText (data):
    image = data['image']
    location = data['location']

    imgBase64 = base64.b64decode(image)
    img = np.array(Image.open(io.BytesIO(imgBase64)))

    img = IMG.inpaint_text(img, location)

    retval, buffer = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    return {'image': encoded_image}