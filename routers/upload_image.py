import base64
import lib.image as IMG
import cv2

def handleUploadImage(data):
    base64Data = data['image']

    img = base64.b64decode(base64Data)
    img = IMG.inpaint_text(img)
      
    retval, buffer = cv2.imencode('.jpg', img)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    response = {'image': encoded_image}
    return response