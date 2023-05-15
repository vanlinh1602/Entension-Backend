import base64
import lib.image as IMG
import cv2
import numpy as np
import io
import easyocr
from PIL import Image
from lib.text import findBubbleText
from gingerit.gingerit import GingerIt

def handleUploadImage(data):
    base64Data = data['image']

    imgBase64 = base64.b64decode(base64Data)
    img = np.array(Image.open(io.BytesIO(imgBase64)))

    reader = easyocr.Reader(['en'])
    results = reader.readtext(img)
    groupText = findBubbleText(results)

    parser = GingerIt()    
    for key, group in groupText.items():
        resultCorr = parser.parse(group['text'])
        print(resultCorr["result"])
      
    img = IMG.drawBubble(img, groupText)
    
    retval, buffer = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    response = {'image': encoded_image}
    return response