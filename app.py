from flask import Flask, jsonify, request
from lib.image import *
from routers.modules import *

app = Flask(__name__)

@app.route('/get-image', methods=['POST'])
def image():
    req = request.get_json()
    res = handleGetImage(data=req)
    return jsonify(res)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    req = request.get_json()
    res = handleUploadImage(req)
    return jsonify(res)

if __name__ == '__main__':
    app.run(port=8000)